# pico2w-blink

A simple Rust firmware for the Raspberry Pi Pico 2 W (RP2350) that toggles a GPIO pin: 5 seconds on, 5 seconds off. Built with the [Embassy](https://embassy.dev/) async embedded framework.

## Hardware

- Raspberry Pi Pico 2 W
- An LED + ~220–330Ω resistor wired to a GPIO pin (default: `PIN_25`) and ground

> **Note:** On the Pico 2 W, the onboard LED is wired through the CYW43 wireless chip, not a plain GPIO. So `PIN_25` in this code drives an *external* LED, not the onboard one. Controlling the onboard LED requires initializing the CYW43 driver, which is out of scope for this basic example.

## Project structure

```
pico2w-blink/
├── Cargo.toml
├── build.rs
├── memory.x
├── .cargo/
│   └── config.toml
└── src/
    └── main.rs
```

### Cargo.toml

```toml
[package]
name = "pico2w-blink"
version = "0.1.0"
edition = "2021"

[dependencies]
embassy-executor = { version = "0.9", features = ["arch-cortex-m", "executor-thread"] }
embassy-time = "0.5"
embassy-rp = { version = "0.9", features = ["rp235xa", "time-driver", "critical-section-impl"] }
cortex-m = "0.7"
cortex-m-rt = "0.7"
panic-halt = "0.2"

[profile.release]
debug = 2
lto = true
opt-level = "s"
```

### src/main.rs

```rust
#![no_std]
#![no_main]

use embassy_executor::Spawner;
use embassy_rp::block::ImageDef;
use embassy_rp::gpio::{Level, Output};
use embassy_time::{Duration, Timer};
use panic_halt as _;

// RP2350 requires a valid Image Definition to boot (replaces the old boot2 approach)
#[unsafe(link_section = ".start_block")]
#[used]
pub static IMAGE_DEF: ImageDef = ImageDef::secure_exe();

#[embassy_executor::main]
async fn main(_spawner: Spawner) {
    let p = embassy_rp::init(Default::default());

    // Change PIN_25 to whichever GPIO you're actually using
    let mut pin = Output::new(p.PIN_25, Level::Low);

    loop {
        pin.set_high();
        Timer::after(Duration::from_secs(5)).await;

        pin.set_low();
        Timer::after(Duration::from_secs(5)).await;
    }
}
```

### memory.x

```
MEMORY {
    FLASH : ORIGIN = 0x10000000, LENGTH = 2048K
    RAM   : ORIGIN = 0x20000000, LENGTH = 512K
}
```

### build.rs

Exposes `memory.x` to the linker (required for `cortex-m-rt` to find `_start` and wire up the entry point):

```rust
use std::env;
use std::fs::File;
use std::io::Write;
use std::path::PathBuf;

fn main() {
    let out = &PathBuf::from(env::var_os("OUT_DIR").unwrap());
    File::create(out.join("memory.x"))
        .unwrap()
        .write_all(include_bytes!("memory.x"))
        .unwrap();
    println!("cargo:rustc-link-search={}", out.display());
    println!("cargo:rerun-if-changed=memory.x");
    println!("cargo:rerun-if-changed=build.rs");
}
```

### .cargo/config.toml

```toml
[build]
target = "thumbv8m.main-none-eabihf"

[target.'cfg(all(target_arch = "arm", target_os = "none"))']
runner = "elf2uf2-rs -d"
rustflags = [
  "-C", "link-arg=-Tlink.x",
  "-C", "link-arg=--nmagic",
]
```

## Setup

1. Install the `elf2uf2-rs` flashing tool:
   ```
   cargo install elf2uf2-rs --locked
   ```
2. Confirm it's on your PATH:
   ```
   where elf2uf2-rs
   ```
   It should resolve to something like `C:\Users\<you>\.cargo\bin\elf2uf2-rs.exe`. If not found, add `C:\Users\<you>\.cargo\bin` to your PATH and restart your terminal.

## Build

```
cargo build --release
```

## Flash

1. Put the Pico 2 W into **BOOTSEL mode**:
   - Unplug it from USB.
   - Hold down the **BOOTSEL** button.
   - While still holding it, plug the USB cable back in.
   - Release BOOTSEL after a second — a removable drive (e.g. `RP2350`) should appear in File Explorer.
2. Flash and run:
   ```
   cargo run --release
   ```
   This builds, converts the ELF to UF2, and copies it onto the mounted Pico drive. On success you'll see a progress bar and `Transfering program to pico`. The Pico then reboots automatically and starts running the firmware — the drive will disappear, which is expected.

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `cannot find entry symbol _start` | Linker isn't picking up the `cortex-m-rt` linker script | Add `build.rs` and the `-Tlink.x` / `--nmagic` rustflags shown above |
| `program not found` when running `elf2uf2-rs` | Tool not installed or not on PATH | `cargo install elf2uf2-rs --locked`, then verify with `where elf2uf2-rs` |
| `Unable to find mounted pico` | Pico isn't in BOOTSEL mode | Hold BOOTSEL while plugging in USB, wait for the drive to mount, then re-run |
| `embassy-rp does not have that feature` (e.g. `rp235xa` missing) | embassy-rp version too old | Use `embassy-rp = "0.9"` or newer with the `rp235xa` feature enabled |

## Notes

- Target architecture is `thumbv8m.main-none-eabihf` (Cortex-M33) — different from the original Pico's `thumbv6m-none-eabi` (Cortex-M0+), because RP2350 uses a different core.
- RP2350 replaced the old `.boot2` bootloader blob with an "Image Definition" block (`ImageDef::secure_exe()` in `main.rs`), so `memory.x` no longer needs a `.boot2` section.

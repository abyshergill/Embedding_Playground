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
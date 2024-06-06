use crate::server;
use core::panic;
use rand::Rng;
use rppal::gpio::Gpio;
use rppal::uart::{Parity, Uart};
use std::sync::Arc;
use std::time::{Instant, SystemTime, UNIX_EPOCH};
use tokio::sync::Mutex;
use tokio::time::{error, sleep, Duration};

pub async fn start_randomizer(my_float: Arc<Mutex<f32>>) {
    let my_float_clone = Arc::clone(&my_float);
    let mut rng = rand::thread_rng();
    loop {
        let mut num = my_float_clone.lock().await;
        *num = rng.gen();
        sleep(Duration::from_secs(1)).await;
    }
}

pub async fn start_gpio_reader() {
    let gpio = Gpio::new().unwrap();
    let pin = gpio.get(23).unwrap().into_input_pullup(); // Replace with your GPIO pin number

    let mut start_time: Option<Instant> = None;
    println!("Entering loop checking sensor");
    loop {
        let value = pin.is_high() as u8 as f32; // Convert boolean to f32

        // If the value is False and start_time is None, record the start time
        if value == 0.0 && start_time.is_none() {
            start_time = Some(Instant::now());
        }
        // If the value is True and start_time is not None, calculate the duration and reset start_time
        else if value != 0.0 && start_time.is_some() {
            let duration = start_time.unwrap().elapsed();
            println!(
                "The signal stayed at False for {} seconds",
                duration.as_micros()
            );

            let micros: u128 = duration.as_micros();
            match server::send_ball_time(
                SystemTime::now()
                    .duration_since(UNIX_EPOCH)
                    .expect("Time went backwards"),
                micros,
            )
            .await
            {
                Ok(_) => {}
                Err(e) => eprintln!("Failed to send ball time: {:?}", e),
            }
            start_time = None;
        }
        // sleep(Duration::from_secs(1)).await;
    }
}
// pub async read_from_uart() -> Result<String, Box<dyn std::error::Error>> {
pub fn read_from_uart() -> Result<u16, Box<dyn std::error::Error>> {
    let mut uart = Uart::new(9600, Parity::None, 8, 1)?;
    uart.set_read_mode(1, Duration::default())?;
    let mut buffer = [0u8; 4]; // Buffer size is now 4
    println!("Entering loop");

    // Fill the buffer variable with any incoming data.
    if uart.read(&mut buffer)? > 0 {
        // Print each byte in the buffer
        let value = u16::from(buffer[1]) << 8 | u16::from(buffer[2]);
        println!("Value: {}", value);
        Ok(value)
    } else {
        panic!("No data");
    }

    // let mut buf: Vec<u8> = vec![0; 100];
    // let len = uart.read(&mut buf)?;
    // let data = String::from_utf8(buf[..len].to_vec())?;
    // Ok(data)
}
//
// pub async fn start_gpio_reader(my_float: Arc<Mutex<f32>>) {
//     let gpio = Gpio::new().unwrap();
//     let pin = gpio.get(23).unwrap().into_input_pullup(); // Replace with your GPIO pin number

//     loop {
//         let value = pin.is_high() as u8 as f32; // Convert boolean to f32
//         let mut num = my_float.lock().await;
//         *num = value;
//         println!("Value: {}", value);
//         sleep(Duration::from_secs(1)).await;
//     }
// }

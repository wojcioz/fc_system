use std::sync::Arc;
// use std::thread;
// use std::time::Duration;

use tokio::fs;
use tokio::sync::Mutex;
mod config;
mod generator;
mod i2c_sensor;
mod server;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let my_float = Arc::new(Mutex::new(0.0f32));

    // println!("Starting video stream");

    // println!("Starting reading gpio pin");
    // if let Err(err) = tokio::spawn(generator::start_gpio_reader()).await {
    //     eprintln!("Error starting GPIO reader: {}", err);
    // }
    // tokio::spawn(i2c_sensor::read_sensor());
    // println!("Starting reading i2c sensor");
    // i2c_sensor::read_sensor();
    print!("Running server");
    server::run_server(my_float).await

    // let data = generator::read_from_uart();
    // println!("Data from UART: {}", data);
    // Ok(())
}

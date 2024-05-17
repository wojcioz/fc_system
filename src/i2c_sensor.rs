extern crate vl53l1x;
use vl53l1x::{Vl53l1xError, Vl53l1xSample};

pub fn read_sensor() -> Result<vl53l1x::Vl53l1xSample, vl53l1x::Vl53l1xError> {
    println!("creating sensor object");
    let mut vl = vl53l1x::Vl53l1x::new(1, None)?;
    println!("init sensor");
    vl.init()?;
    println!("start ranging");
    vl.start_ranging(vl53l1x::DistanceMode::Long)?;
    println!("reading sample");
    let sample = vl.read_sample().unwrap(); // Use ? instead of unwrap()
    println!("Sample: {:?}", sample);
    Ok(sample)
}

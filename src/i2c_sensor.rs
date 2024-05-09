extern crate vl53l1x;

pub fn print_sensor() {
    println!("creating sensor object");
    let mut vl = vl53l1x::Vl53l1x::new(1, None).unwrap();
    println!("init sensor");
    vl.init().unwrap();
    println!("start ranging");
    vl.start_ranging(vl53l1x::DistanceMode::Long).unwrap();
    loop {
        println!("Sample: {:?}", vl.read_sample());
    }
}

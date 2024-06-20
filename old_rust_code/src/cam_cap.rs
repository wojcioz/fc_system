use opencv::{prelude::*, videoio::VideoCapture, videoio::CAP_ANY};
use warp::Filter;
use std::convert::Infallible;
use warp::http::Response;
use warp::hyper::Body;

struct Camera {
    capture: VideoCapture,
}

impl Camera {
    fn new() -> opencv::Result<Self> {
        let capture = VideoCapture::new(CAP_ANY, -1)?;
        Ok(Self { capture })
    }

    fn get_frame(&mut self) -> opencv::Result<Vec<u8>> {
        let mut frame = Mat::default()?;
        self.capture.read(&mut frame)?;
        let mut buf = Vec::new();
        opencv::imgcodecs::imencode(".jpg", &frame, &mut buf, &Default::default())?;
        Ok(buf)
    }
}

async fn video_feed(camera: Camera) -> Result<impl warp::Reply, Infallible> {
    let mut camera = camera;
    let frame = camera.get_frame().unwrap();
    let body = Body::from(frame);
    let response = Response::builder()
        .header("Content-Type", "multipart/x-mixed-replace; boundary=frame")
        .body(body)
        .unwrap();
    Ok(response)
}



#[tokio::main]
async fn main() {
    let camera = Camera::new().unwrap();
    let video_feed = warp::path("video_feed")
        .map(move || video_feed(camera.clone()));

    warp::serve(video_feed)
        .run(([0, 0, 0, 0], 5000))
        .await;
}
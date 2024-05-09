// use gstreamer::prelude::*;
// use gstreamer::{Caps, ElementFactory, Pipeline};
// use gstreamer_app::{AppSink, AppSrc};
// use gstreamer_video::VideoFormat;
// use rascam::SimpleCamera;
// use std::error::Error;
// use tokio::task;

// async fn capture_and_stream() -> Result<(), Box<dyn Error>> {
//     // Initialize GStreamer
//     gstreamer::init()?;

//     // Create a new camera instance
//     let camera = SimpleCamera::new(0)?;

//     // Start capturing video
//     let info = camera.info()?;
//     let width = info.width;
//     let height = info.height;
//     let format = match info.format {
//         rascam::Format::RGB3 => VideoFormat::Rgb,
//         rascam::Format::BGR3 => VideoFormat::Bgr,
//         // Add more formats as needed
//         _ => return Err("Unsupported format".into()),
//     };

//     // Create a new GStreamer pipeline
//     let pipeline = Pipeline::new(None);

//     // Create an AppSrc element to feed the video frames into the pipeline
//     let appsrc = ElementFactory::make("appsrc", None)?;
//     let appsrc = appsrc.downcast::<AppSrc>().unwrap();
//     appsrc.set_caps(Some(&Caps::new_simple(
//         "video/x-raw",
//         &[
//             ("format", &format.to_string()),
//             ("width", &width),
//             ("height", &height),
//             ("framerate", &(30i32, 1i32)),
//         ],
//     )));

//     // Create an AppSink element to get the video frames from the pipeline
//     let appsink = ElementFactory::make("appsink", None)?;
//     let appsink = appsink.downcast::<AppSink>().unwrap();

//     // Add the elements to the pipeline
//     pipeline.add_many(&[&appsrc, &appsink])?;
//     appsrc.link(&appsink)?;

//     // Start the pipeline
//     pipeline.set_state(gstreamer::State::Playing)?;

//     // Start a new Tokio task to feed the video frames into the AppSrc element
//     task::spawn(async move {
//         while let Ok(frame) = camera.capture() {
//             let buffer = gstreamer::Buffer::from_mut_slice(frame);
//             appsrc.push_buffer(buffer).unwrap();
//         }
//     });

//     Ok(())
// }

use crate::config;
use crate::generator;
use actix_files::Files;
use actix_files::NamedFile;
use actix_web::body::BodyStream;
use actix_web::http::header::ContentType;
use actix_web::web::Bytes;
use actix_web::web::Data;
use actix_web::{web, App, Error, HttpRequest, HttpResponse, HttpServer, Responder};
use futures_util::stream::StreamExt;
use hyper::body::Body;
use serde_json::json;
use std::fs;
use std::io;
use std::path::Path;
use std::path::PathBuf;
use std::sync::Arc;
use std::time::Duration;
use tokio::fs::File;
use tokio::sync::Mutex;
use tokio_util::codec::{BytesCodec, FramedRead};

use crate::i2c_sensor;

pub async fn index() -> impl Responder {
    HttpResponse::Ok().body(
        r#"
        <html>
            <body>
                <p id="value"></p>
                <script src="/static/main.js"></script>
            </body>
        </html>
    "#,
    )
}

pub async fn value(data: web::Data<Arc<Mutex<f32>>>) -> impl Responder {
    //test line
    i2c_sensor::read_sensor();
    //
    let start = std::time::Instant::now();
    let my_float = data.lock().await;
    // TODO: https://doc.rust-lang.org/std/sync/mpsc/
    let duration: Duration = start.elapsed();
    println!("Time elapsed in value function is: {:?}", duration);
    HttpResponse::Ok().body(format!("{}", my_float))
}
pub async fn distance(data: web::Data<Arc<Mutex<f32>>>) -> impl Responder {
    // Your logic here
    match generator::read_from_uart() {
        Ok(data) => HttpResponse::Ok().body(format!("Distance to object: {}", data)),
        Err(e) => HttpResponse::InternalServerError().body(format!("Error: {:?}", e)),
    }
}
pub async fn run_server(my_float: Arc<Mutex<f32>>) -> std::io::Result<()> {
    println!("Starting server at http://[::]:8080");
    let config = config::read_config().await.unwrap();
    HttpServer::new(move || {
        App::new()
            .app_data(Data::new(my_float.clone()))
            .service(Files::new("/static", &config.video_folder).prefer_utf8(true))
            .route("/", web::get().to(index))
            .route("/value", web::get().to(value))
            .route("/distance", web::get().to(distance)) // New route for /distance
            .route("/get_dir_contents", web::get().to(get_dir_contents)) // New route for /distance
            // .route("/send_video", web::get().to(send_video)) // New route for /distance
            .service(actix_files::Files::new("/static", "./static"))
    })
    .bind("[::]:8080")?
    .run()
    .await
}

pub async fn get_dir_contents() -> impl Responder {
    let config = match config::read_config().await {
        Ok(config) => config,
        Err(_) => return HttpResponse::InternalServerError().finish(),
    };

    let path = &config.video_folder;
    let entries = match fs::read_dir(path) {
        Ok(entries) => entries,
        Err(_) => return HttpResponse::InternalServerError().finish(),
    };

    let entries = entries
        .map(|res| res.map(|e| e.path().display().to_string()))
        .collect::<Result<Vec<_>, io::Error>>();

    match entries {
        Ok(contents) => HttpResponse::Ok().json(contents),
        Err(_) => HttpResponse::InternalServerError().finish(),
    }
}

// pub async fn send_video(path: web::Query<PathBuf>) -> Result<HttpResponse, Error> {
//     let config = match config::read_config().await {
//         Ok(config) => config,
//         Err(_) => {
//             return Err(actix_web::error::ErrorInternalServerError(
//                 "Error reading config",
//             ))
//         }
//     };
//     let file_path = Path::new(&config.video_folder).join(path.into_inner());
//     if !file_path.exists() {
//         return Err(actix_web::error::ErrorNotFound("File not found"));
//     }

//     let file = File::open(file_path).await?;
//     let stream = FramedRead::new(file, BytesCodec::new()).then(|res| async {
//         match res {
//             Ok(bytes_mut) => Ok::<_, Error>(Bytes::copy_from_slice(bytes_mut.as_ref())),
//             Err(e) => Err(actix_web::error::ErrorInternalServerError(e)),
//         }
//     });
//     let body = BodyStream::new(stream);
//     let body = Body::wrap_stream(body);

//     Ok(HttpResponse::Ok().streaming(body))
// }

pub async fn get_stream_file(req: HttpRequest, filename: web::Path<String>) -> HttpResponse {
    // Not tested yet
    let config = config::read_config().await.unwrap();
    let file_path = std::path::PathBuf::from(env!("HOME"))
        .as_path()
        .join(&config.video_folder)
        .join(&filename.into_inner());

    let file = actix_files::NamedFile::open_async(file_path).await.unwrap();

    file.into_response(&req)
}
pub async fn send_ball_time(
    timestamp: Duration,
    value: u128,
) -> Result<(), Box<dyn std::error::Error>> {
    let config = config::read_config().await?;
    println!("Sending to url: {}", config.url);
    let client = reqwest::Client::new();
    let res = client
        .post(&config.url)
        .json(&json!({"timestamp": timestamp, "value": value}))
        .send()
        .await?;

    println!(
        "Json to send: {:?}",
        &json!({"timestamp": timestamp, "value": value})
    );
    println!("Response: {}", res.status());

    Ok(())
}

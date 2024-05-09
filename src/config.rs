use serde::Deserialize;
use tokio::fs;

#[derive(Deserialize)]
pub struct Config {
    pub url: String,
    pub video_folder: String,
}
pub async fn read_config() -> Result<Config, Box<dyn std::error::Error>> {
    let config_file = fs::read_to_string("config.json").await?;
    let config: Config = serde_json::from_str(&config_file)?;
    Ok(config)
}

use tch::{CModule, Device};
use anyhow::Result;

pub fn load_teacher(config: &crate::config::Config, device: Device) -> Result<CModule> {
    let model = CModule::load_on_device(&config.teacher_path, device)?;
    Ok(model)
}

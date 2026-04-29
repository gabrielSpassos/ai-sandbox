mod config;
mod data;
mod models;
mod training;
mod eval;
mod utils;

use anyhow::Result;


fn main() -> Result<()> {
    println!("Knowledge Distillation!");

    env_logger::init();

    let config = config::Config::default();

    let device = utils::device::get_device();

    let dataset = data::dataset::load_dataset(&config)?;
    let dataloader = data::dataloader::DataLoader {
        images: dataset.images,
        labels: dataset.labels,
        batch_size: config.batch_size as i64,
        index: 0,
    };

    let teacher = models::teacher::load_teacher(&config, device)?;
    let mut student = models::student::build_student(&config, device);

    training::trainer::train(
        &config,
        &teacher,
        &mut student,
        dataloader,
    )?;

    eval::metrics::evaluate(&student, &config)?;

    Ok(())
}
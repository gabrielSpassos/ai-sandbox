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
    let dataloader = data::dataloader::create_dataloader(dataset, &config);

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
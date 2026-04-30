use tch::nn::{self, OptimizerConfig};
use anyhow::Result;

pub fn train(
    config: &crate::config::Config,
    teacher: &tch::CModule,
    student: &mut crate::models::student::Student,
    mut dataloader: crate::data::dataloader::DataLoader,
) -> Result<()> {

    let mut opt = nn::Adam::default().build(&student.vs, config.learning_rate)?;

    for epoch in 0..config.epochs {
        println!("Epoch {}", epoch);

        // pseudo-loop (you'll implement iterator)
        // for batch in dataloader {
        // }

        // placeholder
    }

    Ok(())
}

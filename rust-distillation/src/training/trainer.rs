use anyhow::Result;
use tch::{nn, nn::OptimizerConfig, Kind};

pub fn train(
    config: &crate::config::Config,
    teacher: &tch::CModule,
    student: &mut crate::models::student::Student,
    mut dataloader: crate::data::dataloader::DataLoader,
) -> Result<()> {

    let mut opt = nn::Adam::default().build(&student.vs, config.learning_rate)?;

    for epoch in 0..config.epochs {
        println!("Epoch {}", epoch);

        dataloader.reset();

        let mut total_loss = 0.0;
        let mut batches = 0;

        let mut total_correct = 0.0;
        let mut total_samples = 0.0;

        while let Some((images, labels)) = dataloader.next_batch() {

            let images = images.view([-1, 28 * 28]);

            let student_logits = student.net.forward(&images);
            let teacher_logits = teacher.forward_ts(&[images.copy()])?;

            let loss = crate::training::loss::distillation_loss(
                &student_logits,
                &teacher_logits,
                &labels,
                config.temperature,
                config.alpha,
            );

            total_loss += loss.double_value(&[]);
            batches += 1;

            // Accuracy calculation
            let preds = student_logits.argmax(-1, false);
            let correct = preds
                .eq_tensor(&labels)
                .to_kind(Kind::Float)
                .sum(Kind::Float);

            total_correct += correct.double_value(&[]);
            total_samples += labels.size()[0] as f64;

            opt.backward_step(&loss);
        }

        println!(
            "Epoch {} avg loss: {:.4} | accuracy: {:.2}%",
            epoch,
            total_loss / batches as f64,
            100.0 * total_correct / total_samples
        );
    }

    Ok(())
}
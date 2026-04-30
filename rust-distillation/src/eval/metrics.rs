use tch::{Tensor, Kind};

pub fn evaluate(
    student: &crate::models::student::Student,
    images: &Tensor,
    labels: &Tensor,
) {
    let images = images.view([-1, 28 * 28]);

    let logits = student.net.forward(&images);
    let preds = logits.argmax(-1, false);

    let correct = preds
        .eq_tensor(labels)
        .to_kind(Kind::Float)
        .sum(Kind::Float);

    let acc = correct.double_value(&[]) / labels.size()[0] as f64;

    println!("Test accuracy: {:.2}%", acc * 100.0);
}
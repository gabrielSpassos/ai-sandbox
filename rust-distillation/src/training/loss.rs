use tch::{Tensor, Kind};

pub fn distillation_loss(
    student_logits: &Tensor,
    teacher_logits: &Tensor,
    labels: &Tensor,
    temperature: f64,
    alpha: f64,
) -> Tensor {
    let t = temperature;

    let student_log_probs = (student_logits / t).log_softmax(-1, Kind::Float);
    let teacher_probs = (teacher_logits / t).softmax(-1, Kind::Float);

    let kl = -(teacher_probs * student_log_probs)
        .sum_dim_intlist([-1].as_ref(), false, Kind::Float)
        .mean(Kind::Float);

    let ce = student_logits.cross_entropy_for_logits(labels);

    alpha * ce + (1.0 - alpha) * kl * (t * t)
}
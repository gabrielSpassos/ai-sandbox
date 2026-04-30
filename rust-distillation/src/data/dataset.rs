use anyhow::Result;
use tch::{Tensor, vision::mnist};

pub struct Dataset {
    pub train_images: Tensor,
    pub train_labels: Tensor,
    pub test_images: Tensor,
    pub test_labels: Tensor,
}

pub fn load_dataset() -> Result<Dataset> {
    let mnist = mnist::load_dir("data")?;

    Ok(Dataset {
        train_images: mnist.train_images.view([-1, 1, 28, 28]),
        train_labels: mnist.train_labels,
        test_images: mnist.test_images.view([-1, 1, 28, 28]),
        test_labels: mnist.test_labels,
    })
}
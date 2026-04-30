use tch::{Tensor, vision::mnist};
use anyhow::Result;

pub struct Dataset {
    pub images: Tensor,
    pub labels: Tensor,
}

pub fn load_dataset(_config: &crate::config::Config) -> Result<Dataset> {
    let mnist = mnist::load_dir("data")?;

    Ok(Dataset {
        images: mnist.train_images,
        labels: mnist.train_labels,
    })
}

use tch::Tensor;

pub struct DataLoader {
    images: Tensor,
    labels: Tensor,
    batch_size: i64,
    index: i64,
}

pub fn create_dataloader(dataset: super::dataset::Dataset, config: &crate::config::Config) -> DataLoader {
    DataLoader {
        images: dataset.images,
        labels: dataset.labels,
        batch_size: config.batch_size as i64,
        index: 0,
    }
}

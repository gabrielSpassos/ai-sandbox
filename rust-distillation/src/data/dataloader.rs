use tch::Tensor;

pub struct DataLoader {
    pub images: Tensor,
    pub labels: Tensor,
    pub batch_size: i64,
    pub index: i64,
}

impl DataLoader {
    pub fn next_batch(&mut self) -> Option<(Tensor, Tensor)> {
        let total = self.images.size()[0];

        if self.index >= total {
            return None;
        }

        let end = (self.index + self.batch_size).min(total);

        let imgs = self.images.narrow(0, self.index, end - self.index);
        let lbls = self.labels.narrow(0, self.index, end - self.index);

        self.index = end;

        Some((imgs, lbls))
    }

    pub fn reset(&mut self) {
        self.index = 0;
    }
}

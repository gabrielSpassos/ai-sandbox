pub struct Config {
    pub batch_size: usize,
    pub epochs: usize,
    pub learning_rate: f64,
    pub temperature: f64,
    pub alpha: f64,
    pub teacher_path: String,
}

impl Default for Config {
    fn default() -> Self {
        Self {
            batch_size: 64,
            epochs: 5,
            learning_rate: 1e-3,
            temperature: 3.0,
            alpha: 1.0,
            teacher_path: "models/teacher.pt".into(),
        }
    }
}

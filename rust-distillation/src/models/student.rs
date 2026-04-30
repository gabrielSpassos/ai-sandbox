use tch::{nn, Device};

pub struct Student {
    pub vs: nn::VarStore,
    pub net: Box<dyn nn::Module>,
}

pub fn build_student(_config: &crate::config::Config, device: Device) -> Student {
    let vs = nn::VarStore::new(device);
    let root = &vs.root();

    let net = nn::seq()
        .add(nn::linear(root, 784, 128, Default::default()))
        .add_fn(|x| x.relu())
        .add(nn::linear(root, 128, 10, Default::default()));

    Student {
        vs,
        net: Box::new(net),
    }
}

mod clustering;
mod data;
mod loan_contract;
mod normalization;
mod visualization;

use std::collections::HashMap;

use clustering::cluster_contracts;
use data::sample_contracts;
use visualization::create_cluster_plot;

fn main() {
    let contracts = sample_contracts();

    let (labels, dataset) = cluster_contracts(&contracts, 4,);

    let mut grouped: HashMap<usize, Vec<_>> = HashMap::new();

    for (contract, label) in contracts.iter().zip(labels.iter()) {
        grouped
            .entry(*label)
            .or_default()
            .push(contract);
    }

    create_cluster_plot(dataset, &labels,).unwrap();
}

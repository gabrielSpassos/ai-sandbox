use linfa::prelude::*;
use linfa_clustering::KMeans;
use ndarray::Array2;

use crate::loan_contract::LoanContract;

pub fn cluster_contracts(
    contracts: &[LoanContract],
    n_clusters: usize,
) -> Vec<usize> {

    let features: Vec<f64> = contracts
        .iter()
        .flat_map(|contract| {
            vec![
                contract.amount,
                contract.days_remaining as f64,
            ]
        })
        .collect();

    let dataset = Array2::from_shape_vec(
        (contracts.len(), 2),
        features,
    )
    .unwrap();

    let dataset = DatasetBase::from(dataset);

    let model = KMeans::params(n_clusters)
        .max_n_iterations(100)
        .fit(&dataset)
        .unwrap();

    model.predict(&dataset).to_vec()
}

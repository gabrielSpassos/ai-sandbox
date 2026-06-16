use crate::loan_contract::LoanContract;
use crate::normalization::min_max_scale;

use linfa::prelude::*;
use linfa_clustering::KMeans;
use ndarray::Array2;

pub fn cluster_contracts(
    contracts: &[LoanContract],
    n_clusters: usize,
) -> (Vec<usize>, Array2<f64>) {

    let dataset =
        build_feature_matrix(contracts);

    let ds =
        DatasetBase::from(dataset.clone());

    let model = KMeans::params(n_clusters)
        .max_n_iterations(100)
        .fit(&ds)
        .unwrap();

    let labels =
        model.predict(&ds).to_vec();

    (labels, dataset)
}

pub fn build_feature_matrix(
    contracts: &[LoanContract],
) -> Array2<f64> {

    let features: Vec<f64> = contracts
        .iter()
        .flat_map(|c| {
            vec![
                c.amount,
                c.interest_rate,
                c.monthly_payment,
                c.days_remaining as f64,
                c.loan_term_months as f64,
            ]
        })
        .collect();

    let mut dataset =
        Array2::from_shape_vec(
            (contracts.len(), 5),
            features,
        )
        .unwrap();

    min_max_scale(&mut dataset);

    dataset
}
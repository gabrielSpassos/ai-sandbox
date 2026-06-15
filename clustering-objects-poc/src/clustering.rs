use crate::loan_contract::LoanContract;
use crate::normalization::min_max_scale;

use linfa::prelude::*;
use linfa_clustering::KMeans;
use ndarray::Array2;

pub fn cluster_contracts(
    contracts: &[LoanContract],
    n_clusters: usize,
) -> Vec<usize> {

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

    let mut dataset = Array2::from_shape_vec(
        (contracts.len(), 5),
        features,
    )
    .unwrap();

    min_max_scale(&mut dataset);

    let dataset = DatasetBase::from(dataset);

    let model = KMeans::params(n_clusters)
        .max_n_iterations(100)
        .fit(&dataset)
        .unwrap();

    model.predict(&dataset).to_vec()
}
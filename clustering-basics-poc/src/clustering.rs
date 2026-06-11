use linfa::prelude::*;
use linfa_clustering::KMeans;
use ndarray::Array2;

pub fn cluster_embeddings(
    embeddings: Vec<Vec<f32>>,
    n_clusters: usize,
) -> Vec<usize> {

    let rows = embeddings.len();
    let cols = embeddings[0].len();

    let flattened: Vec<f32> =
        embeddings.into_iter().flatten().collect();

    let array = Array2::from_shape_vec((rows, cols), flattened).unwrap();

    let dataset = DatasetBase::from(array);

    let model = KMeans::params(n_clusters)
        .max_n_iterations(100)
        .fit(&dataset)
        .unwrap();

    model.predict(&dataset).to_vec()
}
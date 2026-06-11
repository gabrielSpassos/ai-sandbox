use fastembed::{EmbeddingModel, InitOptions, TextEmbedding};

pub fn generate_embeddings(
    texts: Vec<String>,
) -> Result<Vec<Vec<f32>>, anyhow::Error> {

    let model = TextEmbedding::try_new(
        InitOptions::new(EmbeddingModel::AllMiniLML6V2)
    )?;

    // ? means to return an error if the model fails to generate embeddings
    let embeddings = model.embed(texts, None)?;

    Ok(embeddings)
}

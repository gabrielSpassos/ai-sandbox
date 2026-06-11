mod embedding;
mod clustering;

use anyhow::Result;

#[tokio::main]
async fn main() -> Result<()> {

    let texts = vec![
        "Italian food".to_string(),
        "Java developer".to_string(),
        "Pizza restaurant".to_string(),
        "Senior backend engineer".to_string(),
        "Spring Boot developer".to_string(),
        "Sushi place".to_string(),
        "Burger delivery".to_string(),
        "Full stack developer".to_string(),
    ];

    let embeddings =
        embedding::generate_embeddings(texts.clone())?;

    let labels =
        clustering::cluster_embeddings(
            embeddings,
            2
        );

    for (text, label) in texts.iter().zip(labels.iter()) {
        println!("Cluster {} -> {}", label, text);
    }

    Ok(())
}
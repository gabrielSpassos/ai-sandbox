mod embedding;
mod clustering;

use anyhow::Result;
use std::collections::HashMap;

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
        "Pasta recipe".to_string(),
    ];

    let embeddings =
        embedding::generate_embeddings(texts.clone())?;

    let labels =
        clustering::cluster_embeddings(
            embeddings,
            2
        );

    println!("Clustered texts:\n");
    for (text, label) in texts.iter().zip(labels.iter()) {
        println!("Cluster {} -> {}", label, text);
    }

    println!("\nGrouped clusters:");
    let mut grouped: HashMap<usize, Vec<String>> = HashMap::new();
    for (text, label) in texts.iter().zip(labels.iter()) {
        grouped
            .entry(*label)
            .or_insert_with(Vec::new)
            .push(text.clone());
    }

    for (cluster, items) in grouped.iter() {
        println!("\nCluster {}:", cluster);

        for item in items {
            println!("- {}", item);
        }
    }

    Ok(())
}
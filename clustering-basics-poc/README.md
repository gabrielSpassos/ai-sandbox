# Clustering Basics POC

## What is clustering

Clustering is an unsupervised machine learning technique that automatically groups similar data points together based on patterns or semantic similarity.
In AI systems, data is usually converted into vectors (embeddings), and clustering algorithms group nearby vectors into meaningful categories.

## Use Cases

recommendation systems, document organization, anomaly detection, and semantic search.

## Inputs
```
"Italian food"
"Java developer"
"Pizza restaurant"
"Senior backend engineer"
"Spring Boot developer"
"Sushi place"
"Burger delivery"
"Full stack developer"
```

## Output
```
Cluster 1 -> Italian food
Cluster 0 -> Java developer
Cluster 1 -> Pizza restaurant
Cluster 0 -> Senior backend engineer
Cluster 0 -> Spring Boot developer
Cluster 1 -> Sushi place
Cluster 1 -> Burger delivery
Cluster 0 -> Full stack developer
```

### Usage

* cargo clean
* cargo build
* cargo run
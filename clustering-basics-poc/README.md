# Clustering Basics POC

> Have working code and do a demo - explain the concepts

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
"Pasta recipe"
```

## Output
```
Clustered texts:

Cluster 0 -> Italian food
Cluster 1 -> Java developer
Cluster 0 -> Pizza restaurant
Cluster 1 -> Senior backend engineer
Cluster 1 -> Spring Boot developer
Cluster 0 -> Sushi place
Cluster 0 -> Burger delivery
Cluster 1 -> Full stack developer
Cluster 0 -> Pasta recipe

Grouped clusters:

Cluster 0:
- Italian food
- Pizza restaurant
- Sushi place
- Burger delivery
- Pasta recipe

Cluster 1:
- Java developer
- Senior backend engineer
- Spring Boot developer
- Full stack developer
```

### Usage

* cargo clean
* cargo build
* cargo run
# Semantic Text Clustering POC

This proof of concept demonstrates how to group texts by semantic similarity using embeddings, clustering, and automatic topic detection. The goal is to turn unstructured text such as support tickets, feedback, comments, or emails into interpretable topic groups.

## Objective

The solution identifies groups of semantically similar documents and generates a view of recurring topics. It also highlights outlier texts to help discover noise, rare cases, or potential incidents.

## Problem this POC solves

In many environments, teams receive large volumes of unstructured text. Reading everything manually is slow and does not scale well. With this POC, it becomes possible to automatically discover dominant subjects, track trends, and find outliers much faster.

## Solution proposal

The POC uses embeddings to capture the meaning of texts, applies dimensionality reduction for easier visualization, and runs clustering to find coherent groups. Then, the solution extracts representative words to name the topics and make the clusters interpretable.

## How it works

1. Texts enter the pipeline.
2. An embedding model converts each text into a semantic vector.
3. UMAP reduces dimensionality for clustering and visualization.
4. HDBSCAN identifies dense groups and marks points as noise when needed.
5. The system extracts the most representative words for each group and creates topic labels.
6. The results can be displayed in tables, charts, and dashboards.

## Main components

- **Embeddings**: Sentence Transformers to represent the meaning of texts.
- **Dimensionality reduction**: UMAP for compression and visualization.
- **Clustering**: HDBSCAN to discover variable-sized clusters and detect noise.
- **Topic labeling**: BERTopic or c-TF-IDF-based logic to name topics.
- **Interface**: FastAPI for an API and Streamlit for visualization, if needed.

## Use cases

- Support tickets.
- Product reviews.
- User feedback.
- Internal messages or emails.
- Incident reports.
- Customer complaints.

## POC deliverables

- List of discovered topics.
- Number of documents per topic.
- Representative examples per cluster.
- Outliers or off-topic texts.
- 2D visualization of clusters.
- Automatic summary of the most relevant themes.

## Success criteria

- The clusters must make semantic sense.
- Topics must be understandable by humans.
- The solution should identify noise or anomalous texts.
- The pipeline should run with acceptable performance on batches of text.
- The output should be easy to present in a demo.

## Scope of the first version

The first version should focus on batch processing. This reduces complexity and makes the value proposition easier to validate. Later, the solution can evolve into an API, scheduled jobs, or an interactive dashboard.

## Proposed architecture

The initial architecture can be organized into three layers:

- **Data ingestion**: reading from CSV, JSON, database, or API.
- **NLP pipeline**: cleaning, embeddings, dimensionality reduction, clustering, and labeling.
- **Presentation**: exporting results and visualizing them in a dashboard.

## Useful metrics

- **Silhouette score** to evaluate separation between groups.
- **Davies-Bouldin score** to measure compactness and distance between clusters.
- **Cluster size distribution** to understand how the data is grouped.
- **Outlier percentage** to measure noise.
- **Human topic coherence** to validate real-world usefulness.

## Usage

Create the virtual environment and install the dependencies with the commands below.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install --upgrade pip
./run-dependency.sh
./run-test.sh
```

## APIS

* http://127.0.0.1:8000/health
* http://127.0.0.1:8000/topics
* http://127.0.0.1:8000/documents
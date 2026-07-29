from dataclasses import dataclass

@dataclass
class Config:
    input_path: str = "data/sample.csv"
    text_column: str = "text"
    output_dir: str = "output"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    umap_n_neighbors: int = 15
    umap_n_components: int = 5
    umap_min_dist: float = 0.0
    umap_metric: str = "cosine"
    min_cluster_size: int = 15
    min_samples: int = 5
    top_n_words: int = 10
    random_state: int = 42

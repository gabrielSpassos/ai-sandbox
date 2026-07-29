import pandas as pd
from pathlib import Path
from src.config import Config
from src.pipeline import run_pipeline

class FakeEmbeddingModel:
    def encode(self, texts, show_progress_bar=False):
        return [[0.1, 0.2, 0.3] for _ in texts]

def test_pipeline_runs(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    output_dir = tmp_path / "output"
    data_dir.mkdir()
    output_dir.mkdir()

    sample = pd.DataFrame(
        {
            "text": [
                "The app crashes when I upload a file.",
                "Great customer service experience.",
                "Payment failed during checkout.",
                "The dashboard is fast and intuitive.",
            ]
        }
    )
    sample_path = data_dir / "sample.csv"
    sample.to_csv(sample_path, index=False)

    fake_config = Config(
        input_path=str(sample_path),
        text_column="text",
        output_dir=str(output_dir),
        embedding_model="fake-model",
        min_cluster_size=2,
        min_samples=1,
        umap_n_neighbors=2,
        umap_n_components=2,
        top_n_words=5,
    )

    monkeypatch.setattr("src.pipeline.Config", lambda: fake_config)
    monkeypatch.setattr("src.pipeline.build_embedding_model", lambda model_name: FakeEmbeddingModel())
    monkeypatch.setattr("src.pipeline.generate_embeddings", lambda model, texts: model.encode(texts))

    result = run_pipeline()

    assert result["documents"] == 4
    assert Path(output_dir / "clustered_documents.csv").exists()
    assert Path(output_dir / "topic_info.csv").exists()
    assert Path(output_dir / "document_info.csv").exists()

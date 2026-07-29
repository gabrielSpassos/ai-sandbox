from pathlib import Path
from src.config import Config
from src.data_loader import load_data
from src.preprocessing import preprocess_texts
from src.embeddings import build_embedding_model, generate_embeddings
from src.topic_model import build_topic_model, fit_topics
from src.visualization import save_topic_info, save_document_info
from src.utils import ensure_output_dir

def run_pipeline():
    config = Config()
    ensure_output_dir(config.output_dir)

    df = load_data(config.input_path, config.text_column)
    texts = preprocess_texts(df[config.text_column].tolist())

    embedding_model = build_embedding_model(config.embedding_model)
    embeddings = generate_embeddings(embedding_model, texts)

    topic_model = build_topic_model(config)
    topics, probs = fit_topics(topic_model, texts, embeddings)

    df_out = df.copy()
    df_out["clean_text"] = texts
    df_out["topic"] = topics
    df_out.to_csv(Path(config.output_dir) / "clustered_documents.csv", index=False)

    save_topic_info(topic_model, config.output_dir)
    save_document_info(topic_model, texts, config.output_dir)

    topic_model.save(Path(config.output_dir) / "bertopic_model")

    return {
        "documents": len(df_out),
        "topics": len(set(topics)),
        "output_dir": config.output_dir,
    }

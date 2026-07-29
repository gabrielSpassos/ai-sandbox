from pathlib import Path
import pandas as pd

def save_topic_info(topic_model, output_dir: str):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    topic_info = topic_model.get_topic_info()
    topic_info.to_csv(Path(output_dir) / "topic_info.csv", index=False)
    return topic_info

def save_document_info(topic_model, texts, output_dir: str):
    doc_info = topic_model.get_document_info(texts)
    doc_info.to_csv(Path(output_dir) / "document_info.csv", index=False)
    return doc_info

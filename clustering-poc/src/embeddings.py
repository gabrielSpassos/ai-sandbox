from sentence_transformers import SentenceTransformer

def build_embedding_model(model_name: str, device: str = "cpu"):
    return SentenceTransformer(model_name, device=device)

def generate_embeddings(model, texts):
    return model.encode(texts, show_progress_bar=False)

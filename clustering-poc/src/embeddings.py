from sentence_transformers import SentenceTransformer

def build_embedding_model(model_name: str):
    return SentenceTransformer(model_name)

def generate_embeddings(model, texts):
    return model.encode(texts, show_progress_bar=True)

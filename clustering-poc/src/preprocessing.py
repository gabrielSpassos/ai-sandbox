import re

def clean_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def preprocess_texts(texts):
    return [clean_text(t) for t in texts]

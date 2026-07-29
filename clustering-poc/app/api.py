from fastapi import FastAPI
from pathlib import Path
import pandas as pd

app = FastAPI(title="Semantic Text Clustering API")

OUTPUT_DIR = Path("output")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/topics")
def topics():
    path = OUTPUT_DIR / "topic_info.csv"
    if not path.exists():
        return {"error": "topic_info.csv not found"}
    df = pd.read_csv(path)
    return df.to_dict(orient="records")

@app.get("/documents")
def documents():
    path = OUTPUT_DIR / "document_info.csv"
    if not path.exists():
        return {"error": "document_info.csv not found"}
    df = pd.read_csv(path)
    return df.to_dict(orient="records")

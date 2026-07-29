import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Semantic Text Clustering", layout="wide")
st.title("Semantic Text Clustering POC")

output_dir = Path("output")
topic_path = output_dir / "topic_info.csv"
doc_path = output_dir / "document_info.csv"

if topic_path.exists():
    st.subheader("Topics")
    topics_df = pd.read_csv(topic_path)
    st.dataframe(topics_df, use_container_width=True)
else:
    st.warning("topic_info.csv not found. Run the pipeline first.")

if doc_path.exists():
    st.subheader("Documents")
    docs_df = pd.read_csv(doc_path)
    st.dataframe(docs_df, use_container_width=True)
else:
    st.warning("document_info.csv not found. Run the pipeline first.")

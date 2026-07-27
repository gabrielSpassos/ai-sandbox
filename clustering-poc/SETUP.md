# Project Setup

This document explains how to prepare the environment to run the semantic text clustering POC in Python.

## Prerequisites

- Python 3.11 or later.
- An up-to-date `pip`.
- Isolated virtual environment.
- Optional: GPU with CUDA to speed up embeddings.

## Stack overview

The solution uses well-known Python NLP and clustering libraries. BERTopic combines embeddings, clustering, and c-TF-IDF to generate interpretable topics, while HDBSCAN is used to discover dense groups and handle noise [web:21][web:14][web:47][web:41].

## Suggested structure

```text
project/
├─ app/
├─ data/
├─ notebooks/
├─ output/
├─ README.md
├─ SETUP.md
└─ requirements.txt
```

## Main dependencies

The solution can use the following libraries:

- `bertopic`
- `sentence-transformers`
- `umap-learn`
- `hdbscan`
- `scikit-learn`
- `pandas`
- `numpy`
- `plotly`
- `fastapi`
- `uvicorn`
- `streamlit`

## Installation

Create the virtual environment and install the dependencies with the commands below.

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install bertopic sentence-transformers umap-learn hdbscan scikit-learn pandas numpy plotly fastapi uvicorn streamlit
```

If you prefer, you can move these dependencies into a `requirements.txt` file to make the environment easier to reproduce.

## Step-by-step setup

1. Create the virtual environment.
2. Activate the environment.
3. Install the dependencies.
4. Download or prepare the text dataset.
5. Run the clustering pipeline.
6. Review the topics and visualizations.

## Installation check

After installing, validate that the packages load correctly with a small Python script.

```python
import bertopic
import sentence_transformers
import umap
import hdbscan
import sklearn
import pandas
import numpy
```

If no error appears, the environment is ready for the POC.

## Execution notes

Without a GPU, the pipeline is still fully usable, but embedding generation may be slower. For a POC, that is usually fine. If the data volume grows, consider batch processing, embedding caching, and asynchronous execution.

## Future execution model

When implementation starts, the architecture can be split into three parts:

- text processing pipeline,
- API for topic queries,
- simple visual frontend.

## Suggested next files

After the setup, the most useful files to add are:

- `requirements.txt`
- `main.py` or `pipeline.py`
- `app/api.py`
- `app/dashboard.py`
- `data/sample.csv`

## Next steps

1. Define the data source.
2. Implement the embeddings and clustering pipeline.
3. Build topic extraction and cluster summarization.
4. Add visualization and evaluation.
5. Publish a simple demo.
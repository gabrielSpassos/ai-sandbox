from umap import UMAP
from hdbscan import HDBSCAN
from bertopic import BERTopic

def build_topic_model(config):
    umap_model = UMAP(
        n_neighbors=config.umap_n_neighbors,
        n_components=config.umap_n_components,
        min_dist=config.umap_min_dist,
        metric=config.umap_metric,
        random_state=config.random_state,
        n_jobs=1,
    )

    hdbscan_model = HDBSCAN(
        min_cluster_size=config.min_cluster_size,
        min_samples=config.min_samples,
        metric="euclidean",
        cluster_selection_method="eom",
        prediction_data=True,
    )

    return BERTopic(
        embedding_model=None,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        top_n_words=config.top_n_words,
        calculate_probabilities=True,
        verbose=True,
    )

def fit_topics(topic_model, texts, embeddings=None):
    return topic_model.fit_transform(texts, embeddings=embeddings)

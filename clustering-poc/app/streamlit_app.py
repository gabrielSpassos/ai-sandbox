import streamlit as st
import requests
import pandas as pd

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="Semantic Clustering POC", layout="wide")
st.title("Semantic Text Clustering POC")

# Health check
try:
    health = requests.get(f"{API_BASE}/health", timeout=2)
    if health.status_code == 200:
        st.success("API is up")
    else:
        st.error("API returned non-200 status for /health")
except Exception:
    st.error("Cannot reach API. Make sure it is running on http://127.0.0.1:8000")

# --- Topics ---
st.header("Topics")

try:
    resp = requests.get(f"{API_BASE}/topics", timeout=5)
    if resp.status_code == 200:
        topics_data = resp.json()
        if topics_data:
            topics_df = pd.DataFrame(topics_data)

            # Summary metrics
            n_topics = len(topics_df)
            n_docs_total = int(topics_df["Count"].sum()) if "Count" in topics_df.columns else None

            cols = st.columns(2)
            cols[0].metric("Total topics", n_topics)
            if n_docs_total is not None:
                cols[1].metric("Total documents (sum of counts)", n_docs_total)

            # Show topic list as a nice table
            st.subheader("Topic list")
            st.dataframe(
                topics_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Topic": st.column_config.NumberColumn("Topic", format="%d"),
                },
            )
        else:
            st.info("No topics found.")
    else:
        st.error(f"/topics returned {resp.status_code}")
except Exception as e:
    st.error(f"Error calling /topics: {e}")

# --- Documents ---
st.header("Documents")

try:
    resp = requests.get(f"{API_BASE}/documents", timeout=5)
    if resp.status_code == 200:
        docs_data = resp.json()
        if docs_data:
            docs_df = pd.DataFrame(docs_data)

            # Filters
            st.subheader("Filters")
            col1, col2 = st.columns([1, 2])

            with col1:
                topic_options = ["All"] + sorted(docs_df["Topic"].dropna().unique().tolist())
                selected_topic = st.selectbox(
                    "Filter by topic",
                    options=topic_options,
                    index=0,
                    placeholder="All topics",
                )

            with col2:
                search_text = st.text_input(
                    "Search in text",
                    value="",
                    placeholder="Type to filter documents...",
                )

            # Apply filters
            filtered_df = docs_df.copy()
            if selected_topic != "All":
                filtered_df = filtered_df[filtered_df["Topic"] == selected_topic]
            if search_text.strip():
                filtered_df = filtered_df[
                    filtered_df["text"].str.contains(search_text, case=False, na=False)
                ]

            # Summary
            n_docs = len(filtered_df)
            n_topics_in_view = filtered_df["Topic"].nunique()
            st.metric("Documents shown", n_docs, delta=f"Topics in view: {n_topics_in_view}")

            # Show documents
            st.subheader("Document list")
            # Try to show most relevant columns first if they exist
            display_cols = []
            for c in ["text", "Topic", "Name", "Probability"]:
                if c in filtered_df.columns:
                    display_cols.append(c)
            display_cols += [c for c in filtered_df.columns if c not in display_cols]

            st.dataframe(
                filtered_df[display_cols],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Topic": st.column_config.NumberColumn("Topic", format="%d"),
                },
            )
        else:
            st.info("No documents found.")
    else:
        st.error(f"/documents returned {resp.status_code}")
except Exception as e:
    st.error(f"Error calling /documents: {e}")
import os
import json
import pickle

import faiss
import numpy as np

from embedder import Embedder


CHUNKS_DIR = "data/processed_chunks/chunks"
FAISS_INDEX_PATH = "data/faiss_index/research_papers.index"
CHUNK_METADATA_PATH = "data/faiss_index/chunk_metadata.pkl"


def load_all_chunks():
    all_texts = []
    all_metadata = []

    for topic in os.listdir(CHUNKS_DIR):
        topic_path = os.path.join(CHUNKS_DIR, topic)

        if not os.path.isdir(topic_path):
            continue

        for file_name in os.listdir(topic_path):
            if not file_name.endswith(".json"):
                continue

            file_path = os.path.join(topic_path, file_name)

            with open(file_path, "r", encoding="utf-8") as f:
                chunk_records = json.load(f)

            for record in chunk_records:
                all_texts.append(record["text"])

                all_metadata.append({
                    "chunk_id": record["chunk_id"],
                    "topic": record["topic"],
                    "source_pdf": record["source_pdf"],
                    "chunk_index": record["chunk_index"],
                    "text": record["text"],
                })

    return all_texts, all_metadata


def build_faiss_index():
    print("Loading chunks...")
    texts, metadata = load_all_chunks()

    print(f"Total chunks loaded: {len(texts)}")

    embedder = Embedder()

    print("Generating embeddings...")
    embeddings = embedder.embed_texts(texts)

    embeddings = np.array(embeddings).astype("float32")

    embedding_dim = embeddings.shape[1]
    print(f"Embedding dimension: {embedding_dim}")

    index = faiss.IndexFlatIP(embedding_dim)
    index.add(embeddings)

    os.makedirs(os.path.dirname(FAISS_INDEX_PATH), exist_ok=True)

    faiss.write_index(index, FAISS_INDEX_PATH)

    with open(CHUNK_METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)

    print("\nFAISS index created successfully.")
    print(f"Total vectors indexed: {index.ntotal}")
    print(f"Index saved to: {FAISS_INDEX_PATH}")
    print(f"Metadata saved to: {CHUNK_METADATA_PATH}")


if __name__ == "__main__":
    build_faiss_index()
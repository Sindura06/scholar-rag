import pickle

import faiss
import numpy as np

from backend.embedder import Embedder
FAISS_INDEX_PATH = "data/faiss_index/research_papers.index"
CHUNK_METADATA_PATH = "data/faiss_index/chunk_metadata.pkl"


class Retriever:
    def __init__(self):
        print("Loading FAISS index...")
        self.index = faiss.read_index(FAISS_INDEX_PATH)

        print("Loading chunk metadata...")
        with open(CHUNK_METADATA_PATH, "rb") as f:
            self.metadata = pickle.load(f)

        self.embedder = Embedder()

    def search(self, query: str, top_k: int = 5):
        query_embedding = self.embedder.embed_texts([query])
        query_embedding = np.array(query_embedding).astype("float32")

        scores, indices = self.index.search(query_embedding, top_k)

        results = []

        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue

            chunk = self.metadata[idx]

            results.append({
                "score": float(score),
                "chunk_id": chunk["chunk_id"],
                "topic": chunk["topic"],
                "source_pdf": chunk["source_pdf"],
                "chunk_index": chunk["chunk_index"],
                "text": chunk["text"],
            })

        return results


if __name__ == "__main__":
    retriever = Retriever()

    question = "What is retrieval augmented generation?"
    results = retriever.search(question, top_k=5)

    print(f"\nQuestion: {question}")
    print("\nTop retrieved chunks:")

    for i, result in enumerate(results, start=1):
        print("\n" + "=" * 80)
        print(f"Result {i}")
        print(f"Score: {result['score']}")
        print(f"Topic: {result['topic']}")
        print(f"Source: {result['source_pdf']}")
        print(f"Chunk index: {result['chunk_index']}")
        print("-" * 80)
        print(result["text"][:1000])
import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1:8b"


def build_prompt(question: str, retrieved_chunks: list) -> str:
    context_blocks = []

    for i, chunk in enumerate(retrieved_chunks, start=1):
        context_blocks.append(
            f"""
Source [{i}]
Topic: {chunk["topic"]}
Source PDF: {chunk["source_pdf"]}
Chunk Index: {chunk["chunk_index"]}

Text:
{chunk["text"]}
"""
        )

    context = "\n\n".join(context_blocks)

    prompt = f"""
You are a research assistant answering questions using only the provided research paper excerpts.

Rules:
1. Answer only from the provided context.
2. If the context is not enough, say: "The provided papers do not contain enough information to answer this fully."
3. Use clear academic language.
4. Include source references like [1], [2], or [3] in the answer.
5. Do not invent papers, claims, methods, numbers, or citations.

Context:
{context}

Question:
{question}

Answer:
"""
    return prompt


def generate_answer(question: str, retrieved_chunks: list) -> str:
    prompt = build_prompt(question, retrieved_chunks)

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=120)
    response.raise_for_status()

    result = response.json()
    return result["response"]


if __name__ == "__main__":
    from backend.retriever import Retriever

    retriever = Retriever()

    question = "What is retrieval augmented generation?"
    retrieved_chunks = retriever.search(question, top_k=5)

    answer = generate_answer(question, retrieved_chunks)

    print("\nQuestion:")
    print(question)

    print("\nAnswer:")
    print(answer)

    print("\nSources:")
    for i, chunk in enumerate(retrieved_chunks, start=1):
        print(f"[{i}] {chunk['source_pdf']} | chunk {chunk['chunk_index']}")
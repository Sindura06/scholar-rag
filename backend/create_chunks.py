import os
import json
from chunker import chunk_text


EXTRACTED_TEXT_DIR = "data/processed_chunks/extracted_text"
CHUNKS_DIR = "data/processed_chunks/chunks"


def create_chunks_from_papers():
    os.makedirs(CHUNKS_DIR, exist_ok=True)

    total_papers = 0
    total_chunks = 0

    for topic in os.listdir(EXTRACTED_TEXT_DIR):
        topic_path = os.path.join(EXTRACTED_TEXT_DIR, topic)

        if not os.path.isdir(topic_path):
            continue

        output_topic_dir = os.path.join(CHUNKS_DIR, topic)
        os.makedirs(output_topic_dir, exist_ok=True)

        for file_name in os.listdir(topic_path):
            if not file_name.endswith(".json"):
                continue

            input_path = os.path.join(topic_path, file_name)
            output_path = os.path.join(output_topic_dir, file_name)

            with open(input_path, "r", encoding="utf-8") as f:
                paper_data = json.load(f)

            text = paper_data.get("text", "")
            chunks = chunk_text(text)

            chunk_records = []

            for i, chunk in enumerate(chunks):
                chunk_records.append({
                    "chunk_id": f"{file_name.replace('.json', '')}_chunk_{i}",
                    "topic": paper_data.get("topic"),
                    "source_pdf": paper_data.get("source_pdf"),
                    "chunk_index": i,
                    "text": chunk
                })

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(chunk_records, f, ensure_ascii=False, indent=2)

            total_papers += 1
            total_chunks += len(chunk_records)

            print(f"Chunked: {file_name} | chunks: {len(chunk_records)}")

    print("\nChunking complete.")
    print(f"Total papers chunked: {total_papers}")
    print(f"Total chunks created: {total_chunks}")


if __name__ == "__main__":
    create_chunks_from_papers()
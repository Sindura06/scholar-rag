import os
import json
from pdf_loader import extract_text_from_pdf


RAW_PAPERS_DIR = "data/raw_papers"
PROCESSED_DIR = "data/processed_chunks/extracted_text"


def process_all_papers():
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    processed_count = 0
    failed_count = 0

    for topic in os.listdir(RAW_PAPERS_DIR):
        topic_path = os.path.join(RAW_PAPERS_DIR, topic)

        if not os.path.isdir(topic_path):
            continue

        output_topic_dir = os.path.join(PROCESSED_DIR, topic)
        os.makedirs(output_topic_dir, exist_ok=True)

        for file_name in os.listdir(topic_path):
            if not file_name.endswith(".pdf"):
                continue

            pdf_path = os.path.join(topic_path, file_name)
            output_file_name = file_name.replace(".pdf", ".json")
            output_path = os.path.join(output_topic_dir, output_file_name)

            if os.path.exists(output_path):
                print(f"Already processed: {file_name}")
                continue

            try:
                text = extract_text_from_pdf(pdf_path)

                paper_data = {
                    "topic": topic,
                    "source_pdf": pdf_path,
                    "text": text,
                }

                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(paper_data, f, ensure_ascii=False, indent=2)

                processed_count += 1
                print(f"Processed: {file_name}")

            except Exception as e:
                failed_count += 1
                print(f"Failed: {file_name} | Error: {e}")

    print("\nExtraction complete.")
    print(f"Processed papers: {processed_count}")
    print(f"Failed papers: {failed_count}")


if __name__ == "__main__":
    process_all_papers()
    
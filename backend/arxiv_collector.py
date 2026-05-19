import os
import csv
import arxiv
import requests


TOPIC_QUERIES = {
    "llm": 'cat:cs.CL AND ("large language models" OR "instruction tuning")',
    "rag": 'cat:cs.CL AND ("retrieval augmented generation" OR "retrieval-augmented generation")',
    "nlp": 'cat:cs.CL AND ("summarization" OR "text classification")',
    "machine_learning": 'cat:cs.LG AND ("machine learning" OR "model evaluation")',
    "data_analysis": 'cat:stat.ML AND ("tabular data" OR "data mining")',
    "information_retrieval": 'cat:cs.IR AND ("dense retrieval" OR "information retrieval")',
    "databases": 'cat:cs.DB AND ("vector database" OR "similarity search")',
}


BASE_DIR = "data/raw_papers"
METADATA_PATH = "data/metadata/arxiv_metadata.csv"


def safe_filename(text: str) -> str:
    text = text.replace("/", "_").replace("\\", "_").replace(":", "_")
    text = text.replace("?", "").replace("*", "").replace('"', "")
    return text[:120]


def download_pdf(pdf_url: str, save_path: str) -> bool:
    try:
        response = requests.get(pdf_url, timeout=30)

        if response.status_code == 200:
            with open(save_path, "wb") as file:
                file.write(response.content)
            return True

        print(f"Failed to download: {pdf_url}")
        return False

    except Exception as e:
        print(f"Error downloading {pdf_url}: {e}")
        return False


def collect_papers(topic: str, query: str, max_results: int = 5):
    print(f"\nCollecting papers for topic: {topic}")

    topic_dir = os.path.join(BASE_DIR, topic)
    os.makedirs(topic_dir, exist_ok=True)

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )

    client = arxiv.Client()
    rows = []

    for paper in client.results(search):
        arxiv_id = paper.get_short_id()
        title = paper.title.strip()
        authors = ", ".join(author.name for author in paper.authors)
        published_date = paper.published.strftime("%Y-%m-%d")
        pdf_url = paper.pdf_url

        file_name = safe_filename(f"{arxiv_id}_{title}") + ".pdf"
        local_pdf_path = os.path.join(topic_dir, file_name)

        if not os.path.exists(local_pdf_path):
            downloaded = download_pdf(pdf_url, local_pdf_path)
        else:
            downloaded = True
            print(f"Already exists: {file_name}")

        if downloaded:
            print(f"Downloaded: {title}")

            rows.append({
                "topic": topic,
                "arxiv_id": arxiv_id,
                "title": title,
                "authors": authors,
                "published_date": published_date,
                "abstract": paper.summary.replace("\n", " "),
                "pdf_url": pdf_url,
                "local_pdf_path": local_pdf_path,
            })

    return rows


def save_metadata(all_rows):
    file_exists = os.path.exists(METADATA_PATH)

    with open(METADATA_PATH, "a", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "topic",
            "arxiv_id",
            "title",
            "authors",
            "published_date",
            "abstract",
            "pdf_url",
            "local_pdf_path",
        ]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerows(all_rows)


if __name__ == "__main__":
    all_rows = []

    for topic, query in TOPIC_QUERIES.items():
        rows = collect_papers(topic, query, max_results=30)
        all_rows.extend(rows)

    save_metadata(all_rows)

    print(f"\nDone. Saved metadata for {len(all_rows)} papers.")
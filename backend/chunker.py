def chunk_text(text: str, chunk_size: int = 1200, overlap: int = 200):
    """
    Split long text into overlapping chunks.

    chunk_size = max characters per chunk
    overlap = repeated characters between chunks
    """
    chunks = []

    if not text:
        return chunks

    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks
import re
from typing import List, Dict

SENTENCE_SPLIT_RE = re.compile(
    r'(?<!\w\.\w\.)'           
    r'(?<![A-Z][a-z]\.)'        
    r'(?<=["\.\?\!])\s+'        
    r'(?=[A-Z0-9"\'\(\[])'      
)

def dedupe_chunks(chunks: List[str]) -> List[str]:
    seen = set()
    unique = []
    for c in chunks:
        text = c.strip()
        if text not in seen:
            seen.add(text)
            unique.append(text)
    return unique


def split_into_paragraphs(text: str) -> List[str]:
    if not text:
        return []

    parts = [p.strip() for p in re.split(r'\n{1,}', text) if p.strip()]

    cleaned = []
    for p in parts:
        p = re.sub(r'\s{2,}', ' ', p)
        cleaned.append(p)

    return cleaned

def split_paragraph_into_sentences(paragraph: str) -> List[str]:
    if not paragraph:
        return []

    sentences = SENTENCE_SPLIT_RE.split(paragraph)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences

def semantic_chunk(
    paragraphs: List[str],
    max_words: int = 100,
    min_words: int = 40
) -> List[Dict]:

    raw_chunks = []
    current_chunk = ""

    for para in paragraphs:
        sentences = split_paragraph_into_sentences(para)

        for sentence in sentences:
            words = sentence.split()

            if len(words) > max_words:
                for i in range(0, len(words), max_words):
                    part = " ".join(words[i:i + max_words])
                    if current_chunk:
                        raw_chunks.append(current_chunk.strip())
                        current_chunk = ""
                    raw_chunks.append(part.strip())
                continue

            if not current_chunk:
                current_chunk = sentence
                continue

            combined = f"{current_chunk.rstrip()} {sentence.lstrip()}"

            if len(combined.split()) > max_words:
                raw_chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk = combined

    if current_chunk:
        raw_chunks.append(current_chunk.strip())

    final_chunks = []
    buffer = ""

    for r in raw_chunks:
        wc = len(r.split())

        if wc < min_words:
            if not buffer:
                buffer = r
            else:
                combined = f"{buffer} {r}"
                if len(combined.split()) <= max_words:
                    buffer = combined
                else:
                    final_chunks.append(buffer.strip())
                    buffer = r
        else:
            if buffer:
                final_chunks.append(buffer.strip())
                buffer = ""
            final_chunks.append(r)

    if buffer:
        final_chunks.append(buffer.strip())

    final_chunks = dedupe_chunks(final_chunks)


    return [
        {"text": c, "page": None, "chunk_id": i}
        for i, c in enumerate(final_chunks)
    ]


def chunk_text(text: str, max_words: int = 100, min_words: int = 40) -> List[Dict]:
    paragraphs = split_into_paragraphs(text)
    if not paragraphs:
        paragraphs = [text]

    return semantic_chunk(paragraphs, max_words=max_words, min_words=min_words)
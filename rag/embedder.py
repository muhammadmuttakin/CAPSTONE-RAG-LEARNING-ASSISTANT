import re
import threading
import numpy as np
from typing import List, Union
from sentence_transformers import SentenceTransformer

_model = None
_model_lock = threading.Lock()


def clean_text(text: str) -> str:
    if not text:
        return ""

    text = re.sub(r"&nbsp;?", " ", text)
    text = re.sub(r"<br\s*/?>", " ", text, flags=re.I)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


def get_model(name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
    global _model
    if _model is None:
        with _model_lock:
            if _model is None:
                _model = SentenceTransformer(name)
    return _model

def embed(
    texts: Union[str, List[str]],
    model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
) -> np.ndarray:

    model = get_model(model_name)

    single = False
    if isinstance(texts, str):
        texts = [texts]
        single = True

    cleaned = [clean_text(t) for t in texts]

    vectors = model.encode(
        cleaned,
        convert_to_numpy=True,
        normalize_embeddings=True,   
        show_progress_bar=False
    )

    if single:
        return vectors[0].reshape(1, -1)

    return vectors

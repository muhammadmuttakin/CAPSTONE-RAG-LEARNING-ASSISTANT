import faiss
import numpy as np
import os
import json
from typing import List, Dict, Tuple, Optional
from rag.embedder import embed

INDEX_PATH = "faiss.index"
META_PATH = "faiss_meta.json"


def _normalize(v: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(v, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return v / norms


class VectorStore:
    def __init__(self, docs: List[Dict], embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        """
        Build fresh vectorstore from docs.
        """
        self.docs = docs
        self.embedding_model = embedding_model
        self.vectors: Optional[np.ndarray] = None
        self.index: Optional[faiss.IndexFlatIP] = None
        self._build()

    def _build(self):
        """Build FAISS index dari dokumen"""
        texts = [d["text"] for d in self.docs]

        if not texts:
            self.vectors = np.zeros((0, 1), dtype="float32")
            self.index = faiss.IndexFlatIP(1)
            return

        vectors = embed(texts, model_name=self.embedding_model).astype("float32")
        vectors = _normalize(vectors)

        self.vectors = vectors

        dim = vectors.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(vectors)

    def search(self, query: str, k: int = 3, min_score: float = 0.0):
        """
        Search dokumen yang paling relevan dengan query.
        Return: List[(doc, score)]
        """
        qvec = embed([query], model_name=self.embedding_model).astype("float32")
        qvec = _normalize(qvec)

        if self.index.ntotal == 0:
            return []

        k = min(k, self.index.ntotal)
        scores, ids = self.index.search(qvec, k)

        results = []
        for score, idx in zip(scores[0], ids[0]):
            if score >= min_score:
                results.append((self.docs[int(idx)], float(score)))
        
        return results

    def save(self, index_path=INDEX_PATH, meta_path=META_PATH):
        """
        Save FAISS index dan metadata ke disk.
        FAISS index berisi semua embedding vectors.
        Metadata berisi dokumen dan config.
        """
        faiss.write_index(self.index, index_path)

        meta = {
            "docs": self.docs,
            "embedding_model": self.embedding_model
        }

        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)


    @classmethod
    def load(cls, index_path=INDEX_PATH, meta_path=META_PATH):
        """
        Load vectorstore tanpa membangun ulang embedding atau index.
        Perbaikan penting: tidak panggil __init__()!
        
        FIXED: Added error handling
        """

        if not os.path.exists(index_path):
            raise FileNotFoundError(f"Index file not found: {index_path}")
        if not os.path.exists(meta_path):
            raise FileNotFoundError(f"Metadata file not found: {meta_path}")

        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)

        inst = cls.__new__(cls)

        inst.docs = meta["docs"]
        inst.embedding_model = meta["embedding_model"]

        inst.index = faiss.read_index(index_path)

        inst.vectors = None

        return inst
<p align="center">
  <img src="https://www.python.org/static/community_logos/python-logo.png" alt="Python" height="40"/>
  <img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI" height="40"/>
  <img src="https://upload.wikimedia.org/wikipedia/commons/3/3f/OpenAI_Logo.svg" alt="LLM" height="40"/>
  <img src="https://railway.app/brand/logo-light.svg" alt="Railway" height="40"/>
</p>

# Dicoding Personal Learning Assistant (RAG-Based)

## Deskripsi Singkat Proyek

Dicoding Personal Learning Assistant adalah aplikasi **Retrieval-Augmented Generation (RAG)** berbasis API yang berfungsi sebagai asisten pembelajaran personal. Aplikasi ini mampu menjawab pertanyaan pengguna terkait pembelajaran, melacak progres belajar, menyimpan riwayat percakapan, serta memberikan rekomendasi course dan learning path secara cerdas.

Proyek ini dikembangkan sebagai bagian dari **Capstone Project** dan di-*deploy* sebagai layanan backend menggunakan **FastAPI**.

---

## Tautan Penting

* **Repository GitHub**: [https://github.com/muhammadmuttakin/CAPSTONE-RAG-LEARNING-ASSISTANT](https://github.com/muhammadmuttakin/CAPSTONE-RAG-LEARNING-ASSISTANT)
* **Deployment (API Endpoint)**: [https://web-production-de61.up.railway.app/chat](https://web-production-de61.up.railway.app/chat)
* **API Documentation (Swagger)**: [https://web-production-de61.up.railway.app/docs](https://web-production-de61.up.railway.app/docs)

---

## Arsitektur Singkat

Aplikasi menggunakan pendekatan modular dengan komponen utama:

* **RAG Pipeline**: Menjawab pertanyaan pengguna secara kontekstual
* **Chat History Manager**: Menyimpan dan mengelola sesi percakapan
* **Progress Tracker**: Melacak progres pembelajaran user
* **Recommendation Engine**: Memberikan rekomendasi course dan learning path
* **Data Loader**: Memuat data course, level, dan learning path

---

## Struktur Proyek

Struktur proyek dirancang modular agar mudah dikembangkan dan dipelihara:

```
CAPSTONE-RAG-LEARNING-ASSISTANT/
├── main.py                # Entry point FastAPI
├── config.py              # Konfigurasi aplikasi
├── requirements.txt       # Daftar dependency Python
├── faiss.index            # Vector index (FAISS)
├── faiss_meta.json        # Metadata vector store
├── prompts/               # Prompt template untuk LLM
│   ├── classifier.txt
│   ├── learning.txt
│   ├── recommendation.txt
│   └── tracking.txt
└── rag/                   # Core RAG modules
    ├── pipeline.py        # Orkestrasi RAG (smart_answer)
    ├── classifier.py      # Klasifikasi intent query
    ├── embedder.py        # Embedding generator
    ├── vectorstore.py     # FAISS vector store
    ├── chunker.py         # Pemecah dokumen
    ├── data_loader.py     # Loader data course & learning path
    ├── prompt_loader.py   # Loader prompt
    ├── history.py         # Manajemen riwayat chat
    ├── tracking.py        # Tracking progres belajar
    ├── recommendation.py # Engine rekomendasi
    └── llm.py             # Wrapper LLM
```

---

## Dependency

Pastikan Python **3.9+** telah terpasang.

Install dependency menggunakan:

```
pip install -r requirements.txt
```

---

## Petunjuk Setup Environment

1. Clone repository:

   ```
   git clone https://github.com/muhammadmuttakin/CAPSTONE-RAG-LEARNING-ASSISTANT.git
   cd CAPSTONE-RAG-LEARNING-ASSISTANT
   ```

2. (Opsional) Buat dan aktifkan virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # Linux / macOS
   venv\Scripts\activate     # Windows
   ```

3. Install dependency:

   ```
   pip install -r requirements.txt
   ```

4. Salin file environment:

   ```
   cp .env.example .env
   ```

   Lalu isi nilai environment yang dibutuhkan.

---

## Cara Menjalankan Aplikasi

Jalankan server FastAPI menggunakan:

```
uvicorn main:app --reload
```

Aplikasi akan berjalan di:

```
http://127.0.0.1:8000
```

Dokumentasi API:

* Swagger UI: `/docs`
* ReDoc: `/redoc`

---

## Endpoint Utama

### Chat

`POST /chat`
Mengirim pertanyaan dan mendapatkan jawaban dari RAG Assistant.

---

## Deployment Model ML

Model dan pipeline RAG telah di-*deploy* dan dapat langsung diakses melalui endpoint:

```
https://web-production-de61.up.railway.app/chat
```

Contoh request:

```json
{
  "query": "Saya ingin belajar backend developer",
  "session_id": "optional-session-id"
}
```

---

## Catatan Tambahan

* State percakapan dan progres dikelola di sisi server.
* Cocok digunakan sebagai *learning assistant*, *chat-based recommender system*, atau dasar pengembangan LMS berbasis AI.

---

# Reference Search

A Retrieval-Augmented Generation (RAG) pipeline that matches enterprise customer challenges to the most relevant Intershop customer case studies, returning ranked references with reasoning, supporting evidence, and confidence scores.

---

## Overview

Sales engineers, solution consultants, and pre-sales teams routinely need to answer the question: *"Which of our existing customers solved a problem like the one this prospect is describing?"* Manually scanning case studies for the right match is slow, biased toward recently-read references, and easy to get wrong when prospects describe their challenges in their own vocabulary.

Reference Search solves this by:

1. **Ingesting** structured case studies (company, challenges, outcomes) into a knowledge base.
2. **Embedding** each case study with `text-embedding-3-large` and indexing it in Qdrant.
3. **Retrieving** the top-5 semantically similar case studies for a free-text query.
4. **Generating** a ranked list of 1–3 customer references using `gpt-5-nano`, with the model required to ground its reasoning in both the *challenges* and *outcomes* of each case study.

The system ships with two evaluation harnesses (Recall@5, MRR, and an LLM-as-judge response evaluator) so retrieval quality and answer quality can be measured as the knowledge base grows.

---

## Architecture

<img width="1202" height="765" alt="Screenshot 2026-05-10 at 15 38 39" src="https://github.com/user-attachments/assets/ed002445-70ab-4657-bf4f-b92ac31558cd" />

---

The Docker Compose stack runs two services:

| Service     | Image           | Port | Role                                |
| ----------- | --------------- | ---- | ----------------------------------- |
| `app`       | built locally   | 8000 | FastAPI application                 |
| `vector_db` | `qdrant/qdrant` | 6333 | Vector store for embeddings         |

---

## Tech stack

- **Python** 3.11+
- **FastAPI** (`fastapi[standard]`) — HTTP API
- **OpenAI** (`openai`, `langchain-openai`) — embeddings + LLM
- **Qdrant** (`langchain-qdrant`, `qdrant-client`) — vector store
- **aiofiles** — async file I/O for the knowledge base
- **python-dotenv** — environment loading
- **uv** — dependency manager (lockfile committed as `uv.lock`)

---

## Project structure

```
.
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
└── src/
    ├── main.py                       # FastAPI entry point + routes
    ├── dtos.py                       # Pydantic request DTOs
    ├── knowledge-base/
    │   └── case-studies.txt          # generated/appended via API (gitignored)
    └── rag_pipeline/
        ├── chat.py                   # retrieval + generation
        ├── inngest.py                # ingestion pipeline
        └── evals/
            ├── retrieval_eval.py     # Recall@5, MRR
            ├── response_eval.py      # LLM-as-judge response scoring
            └── test_data.py          # ground-truth queries + relevant docs
```

---

## Prerequisites

- Docker and Docker Compose (recommended path)
- An OpenAI API key with access to `text-embedding-3-large`, `gpt-5-nano`, and (for response evals) `gpt-5`
- Python 3.11+ if running outside Docker

---

## Environment variables

Create a `.env` file at the repo root (it is gitignored). Only the variable **keys** are documented here — supply your own values.

| Variable         | Required | Default                  | Used by                                      |
| ---------------- | -------- | ------------------------ | -------------------------------------------- |
| `OPENAI_API_KEY` | yes      | —                        | `langchain-openai`, `openai.AsyncOpenAI`     |
| `QDRANT_URL`     | no       | `http://localhost:6333`  | `chat.py`, `inngest.py` (Compose overrides to `http://vector_db:6333`) |

---

## Quick start (Docker Compose)

```bash
# 1. Provide credentials
cp .env.example .env   # if you keep an example file; otherwise create .env yourself
echo 'OPENAI_API_KEY=sk-...' >> .env

# 2. Boot the stack (FastAPI on :8000, Qdrant on :6333)
docker-compose up --build

# 3. Health check
curl http://localhost:8000/root
# {"message":"I am running!"}
```

The app container mounts `./src` for hot reload (`--reload`), so source edits take effect without rebuilding.

---

## Local development (without Docker)

```bash
# Install dependencies (uv recommended; pip works too)
uv sync                       # or: pip install -e .

# Run a Qdrant instance separately, e.g.:
docker run -p 6333:6333 qdrant/qdrant

# Start the API
export OPENAI_API_KEY=sk-...
uvicorn src.main:app --reload --port 8000
```

`QDRANT_URL` defaults to `http://localhost:6333`, which matches the standalone container above.

---

## API reference

### `GET /root`

Health check.

```bash
curl http://localhost:8000/root
# → {"message": "I am running!"}
```

### `POST /api/case-studies`

Ingest one or more case studies. The handler appends new entries to `src/knowledge-base/case-studies.txt` (skipping companies that already exist by name, case-insensitive), then **drops and re-creates** the Qdrant `case-studies` collection from the full file.

**Request body** (`CreateCaseStudiesDto`):

```json
{
  "caseStudies": [
    {
      "companyName": "SHOPcloud360",
      "challenges": [
        "Managing a catalog of one million products",
        "Onboarding hundreds of merchants onto a single platform"
      ],
      "outcomes": [
        "350 online shops managed centrally",
        "1M products served from a single backend"
      ]
    }
  ]
}
```

**Response**: `201 Created`

```json
{ "message": "Added to knowledge base" }
```

```bash
curl -X POST http://localhost:8000/api/case-studies \
  -H 'Content-Type: application/json' \
  -d @case-studies.json
```

### `GET /api/customer-references?search=<query>`

Retrieve up to 3 ranked customer references for a natural-language challenge.

**Query parameters**

| Name     | Type   | Required | Description                   |
| -------- | ------ | -------- | ----------------------------- |
| `search` | string | yes      | Free-text customer challenge  |

**Response** (`200 OK`) wraps a `CustomerReferences` payload:

```json
{
  "message": {
    "customerReferences": [
      {
        "companyName": "SHOPcloud360",
        "reason": "Operates a platform with one million products...",
        "relevantChallenges": ["Managing a catalog of one million products"],
        "relevantOutcomes":   ["350 online shops managed centrally"],
        "confidenceScore": 92
      }
    ]
  }
}
```

```bash
curl 'http://localhost:8000/api/customer-references?search=we%20have%20a%20very%20large%20product%20catalog'
```

If retrieval returns no documents, `message` will be `null`.

---

## Knowledge-base format

`src/knowledge-base/case-studies.txt` is a plain-text file built up incrementally by the API. Each company is delimited by a `Company Name:` header, which is also the chunking boundary used by `inngest.create_chunks`.

```
Company Name: SHOPcloud360

Challenges:
   1. Managing a catalog of one million products
   2. Onboarding hundreds of merchants onto a single platform

Outcomes:
   - 350 online shops managed centrally
   - 1M products served from a single backend


Company Name: Nice S.p.A.

Challenges:
   1. ...
```

Each chunk becomes one LangChain `Document` whose `page_content` is the whitespace-collapsed text and whose `metadata.company_name` is the parsed company name. The Qdrant collection used is `case-studies`.

---

## RAG pipeline internals

| Component        | Setting                                                                |
| ---------------- | ---------------------------------------------------------------------- |
| Embedding model  | `text-embedding-3-large` (OpenAI)                                      |
| Vector store     | Qdrant, collection `case-studies`                                      |
| Retrieval        | similarity search, `k = 5`                                             |
| Generation model | `gpt-5-nano` (OpenAI Responses API, `responses.parse`)                 |
| Output schema    | `CustomerReferences` (Pydantic) — list of `CustomerReference` objects  |

The system prompt in `src/rag_pipeline/chat.py` requires the model to:

- Use **both** the `challenges` *and* `outcomes` fields when scoring relevance — never keyword similarity alone.
- Consider business context, scale, and proven outcomes (large revenue, many countries, millions of products, etc.).
- Return **1–3** references, ranked by relevance, each with a `reason`, `relevantChallenges`, `relevantOutcomes`, and a 0–100 `confidenceScore`.

Each call to `POST /api/case-studies` triggers a full re-index: `clean_vector_store` deletes the existing collection, then `create_embeddings` rebuilds it from the updated text file. This is intentional — it keeps the index consistent with the knowledge base — but it means ingestion cost scales with total knowledge-base size, not the size of the new batch.

---

## Evaluation

Two evaluation scripts live under `src/rag_pipeline/evals/`. Both expect the API/Qdrant stack to be running and a populated knowledge base.

### Retrieval evaluation — `retrieval_eval.py`

Computes per-query and average **Recall@5** and **Mean Reciprocal Rank (MRR)** against the five ground-truth queries in `test_data.RETRIEVAL_TEST_DATA`.

```bash
python -m src.rag_pipeline.evals.retrieval_eval
```

For each test case it prints:

- `recall_at_k` — fraction of ground-truth relevant companies present in top-5
- `retrieved_companies`, `relevant_companies`, `matched_companies`
- `mrr` — `1 / rank` of the first relevant document, or 0 if none in top-5

It then prints aggregate `Average Recall@5` and `Average MRR` over all queries.

### Response evaluation — `response_eval.py`

Picks one random case from `test_data.RESPONSE_TEST_DATA`, calls `search_customer_references`, and asks `gpt-5` to score the generated response on five 0–5 dimensions plus a `final_score` and `summary`:

| Score                       | What it measures                                                       |
| --------------------------- | ---------------------------------------------------------------------- |
| `relevance_score`           | Does the response match the customer challenge?                        |
| `primary_reference_score`   | Is the expected primary reference correctly identified and ranked?     |
| `evidence_grounding_score`  | Are reasons grounded in the actual challenges/outcomes?                |
| `completeness_score`        | Are multiple relevant references included where appropriate?           |
| `hallucination_score`       | Penalizes invented claims or unsupported statements.                   |

```bash
python -m src.rag_pipeline.evals.response_eval
```

### Ground-truth queries

Both evaluators use the same five queries (covering catalog scale, multi-country sales, automation, fragmented systems, and ERP/CRM integration). See `src/rag_pipeline/evals/test_data.py` to extend the dataset.

---

## Notes & limitations

- **`case-studies.txt` is gitignored.** The knowledge base is built up at runtime via `POST /api/case-studies` and is not version-controlled. Re-deployments start from an empty file unless you persist the volume.
- **Full re-index on every ingest.** `initiate_rag` always drops and recreates the Qdrant collection. This is simple and correct but not incremental — keep that in mind for large knowledge bases.
- **Hard-coded constants.** `COLLECTION_NAME` and `RETRIEVAL_K` are defined in `src/rag_pipeline/chat.py` and `src/rag_pipeline/inngest.py`; change them in code if you need different defaults.
- **Model availability.** `gpt-5-nano` and `gpt-5` must be enabled on your OpenAI account for generation and the LLM judge respectively.

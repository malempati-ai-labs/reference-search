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

## Key Features

- Semantic search over enterprise customer case studies
- Vector retrieval using Qdrant
- GPT-powered ranking and reasoning
- Structured JSON API responses
- Retrieval evaluation with Recall@5 and MRR
- LLM-as-a-judge response evaluation
- Dockerized local development environment

---

## Why RAG Instead of Keyword Search?

- Semantic retrieval allows the system to match customer intent even when queries use different wording than the original case studies. This improves recall and reduces dependency on exact keyword overlap.

---

## High Level Architecture

<img width="1208" height="751" alt="Screenshot 2026-05-11 at 09 56 51" src="https://github.com/user-attachments/assets/134c636d-66c1-44e6-a907-eb4268f96061" />



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
├── server/
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
          ├── constants.py              # shared config: paths, collection name, models, Qdrant URL
          ├── search.py                 # retrieval + generation
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
| `QDRANT_URL`     | no       | `http://localhost:6333`  | `src/rag_pipeline/constants.py` (Compose overrides to `http://vector_db:6333`) |

---

## Quick start (Docker Compose)

```bash
# 1. Provide credentials
cp .env.example .env   # if you keep an example file; otherwise create .env yourself
echo 'OPENAI_API_KEY=sk-...' >> .env

# 2. Boot the stack (FastAPI on :8000, Qdrant on :6333)
docker-compose up --build

# 3. Health check
curl http://localhost:8000/health
# {"message":"Server is running!"}
```

The Docker Compose stack runs two services:

| Service     | Image           | Port | Role                                |
| ----------- | --------------- | ---- | ----------------------------------- |
| `app`       | built locally   | 8000 | FastAPI application                 |
| `vector_db` | `qdrant/qdrant` | 6333 | Vector store for embeddings         |

The app container mounts `./src` for hot reload (`--reload`), so source edits take effect without rebuilding.

## API reference

### `GET /health`

Health check.

```bash
curl http://localhost:8000/health
# → {"message": "Server is running!"}
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
{ "message": "The knowledge base is updated." }
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

**Response** (`200 OK`) returns the ranked references under a `data` array:

```json
{
  "data": [
    {
      "companyName": "SHOPcloud360",
      "reason": "Operates a platform with one million products...",
      "relevantChallenges": ["Managing a catalog of one million products"],
      "relevantOutcomes":   ["350 online shops managed centrally"],
      "confidenceScore": 92
    }
  ]
}
```

```bash
curl 'http://localhost:8000/api/customer-references?search=we%20have%20a%20very%20large%20product%20catalog'
```

If retrieval returns no documents, `data` will be `[]`.

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
| Chunking Strategy| Structured: Best results when we have control over document formatting |
| Embedding model  | `text-embedding-3-large` (OpenAI)                                      |
| Vector store     | Qdrant, collection `case-studies`                                      |
| Retrieval        | similarity search, `k = 5`                                             |
| Generation model | `gpt-5-nano` (OpenAI Responses API, `responses.parse`)                 |
| Output schema    | `CustomerReferences` (Pydantic) — list of `CustomerReference` objects  |

The system prompt in `src/rag_pipeline/search.py` requires the model to:

- Use **both** the `challenges` *and* `outcomes` fields when scoring relevance — never keyword similarity alone.
- Consider business context, scale, and proven outcomes (large revenue, many countries, millions of products, etc.).
- Return **1–3** references, ranked by relevance, each with a `reason`, `relevantChallenges`, `relevantOutcomes`, and a 0–100 `confidenceScore`.

`search_customer_references` is composed of three small steps: `retrieve_similar_documents` (Qdrant similarity search), `format_context` (concatenates retrieved docs), and `call_llm_for_references` (structured `responses.parse` call against `gpt-5-nano`).

Each call to `POST /api/case-studies` triggers `initiate_rag_pipeline`, which runs `add_to_knowledge_base` → `create_chunks` → `clean_vector_store` → `create_embeddings`. The vector collection is dropped and rebuilt from the updated text file on every ingest. This is intentional — it keeps the index consistent with the knowledge base — but it means ingestion cost scales with total knowledge-base size, not the size of the new batch.

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

## Current Limitations & Future Improvements

Current Limitations:

- **`case-studies.txt` is gitignored.** The knowledge base is built up at runtime via `POST /api/case-studies` and is not version-controlled. Re-deployments start from an empty file unless you persist the volume.
- **Full re-index on every ingest.** `initiate_rag_pipeline` always drops and recreates the Qdrant collection. This is simple and correct but not incremental — keep that in mind for large knowledge bases.
- **Centralized config.** `KNOWLEDGE_BASE_FILE_PATH`, `VECTOR_STORE_COLLECTION_NAME`, `EMBEDDING_MODEL`, and `QDRANT_URL` live in `src/rag_pipeline/constants.py`. `RETRIEVAL_K` is still defined locally in `src/rag_pipeline/search.py`. Change them in code if you need different defaults; only `QDRANT_URL` is env-overridable.
- **Model availability.** `gpt-5-nano` and `gpt-5` must be enabled on your OpenAI account for generation and the LLM judge respectively.

Future improvements:

- Incremental indexing via Qdrant upserts
- Hybrid search (keyword + semantic)
- Automated customer-reference scraping
- Product recommendation retrieval

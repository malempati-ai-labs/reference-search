# Reference Search

A Retrieval-Augmented Generation (RAG) pipeline that matches enterprise customer challenges to the most relevant customer case studies, returning ranked references with reasoning, supporting evidence, and confidence scores.

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

**Server**

- **Python** 3.11+
- **FastAPI** (`fastapi[standard]`) — HTTP API (CORS enabled for the local client origin)
- **OpenAI** (`openai`, `langchain-openai`) — embeddings + LLM
- **Qdrant** (`langchain-qdrant`, `qdrant-client`) — vector store
- **aiofiles** — async file I/O for the knowledge base
- **python-dotenv** — environment loading
- **uv** — dependency manager (lockfile committed as `uv.lock`)

**Client**

- **React 19** + **TypeScript** + **Vite**
- **TailwindCSS 4** — styling
- **React Router** — routing
- **TanStack Query** — server state (mutations, devtools)
- **React Hook Form** — form state and validation
- **lucide-react** — icons

---

## Project structure

```
.
├── CLAUDE.md                             # entry point for AI context (imports files in context/)
├── .claude/
│   ├── agents/
│   │   └── client-code-scanner.md        # reviews frontend changes against coding standards
│   └── skills/
│       ├── feature/                      # /feature load|start|review|explain|complete
│       └── list-components/              # /list-components
├── context/
│   ├── project-overview.md               # backend API contract and data shapes
│   ├── frontend-coding-standards.md      # React/TS/Tailwind conventions
│   ├── ai-interactions.md                # rules for how the AI works in this repo
│   ├── current-feature.md                # active feature, goals, notes, history
│   ├── features/                         # feature/fix specs (one file each)
│   └── designs/                          # UI screenshots used as design references
├── client/
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.ts
│   └── src/
│       ├── main.tsx                      # entry: QueryClientProvider + BrowserRouter
│       ├── App.tsx                       # routes
│       ├── components/                   # shared layout and header
│       ├── pages/
│       │   ├── search-page.tsx           # search route (`/`)
│       │   └── add-case-study-page.tsx   # thin wrapper around the feature component
│       ├── features/
│       │   └── add-case-study/
│       │       ├── add-case-study.tsx    # form UI, validation, submit feedback
│       │       ├── types.ts              # feature types
│       │       └── hooks/
│       │           └── use-create-case-studies.ts   # React Query mutation
│       └── lib/
│           └── api/
│               └── case-studies.ts       # createCaseStudies() — the only `fetch` call
└── server/
    ├── Dockerfile
    ├── docker-compose.yml                # app, vector_db, client
    ├── .env.example
    ├── pyproject.toml
    ├── uv.lock
    └── src/
        ├── main.py                       # FastAPI entry point + routes + CORS
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

The client follows a strict layering: **page → feature component → React Query hook → `lib/api` function**. Pages stay thin, components never call `fetch`, hooks hold no UI concerns, and only `lib/api` talks to the backend.

---

## Prerequisites

- Docker and Docker Compose (recommended path)
- An OpenAI API key with access to `text-embedding-3-large`, `gpt-5-nano`, and (for response evals) `gpt-5`
- Python 3.11+ if running outside Docker

---

## Environment variables

Create a `.env` file in `server/` (it is gitignored; see `server/.env.example`). Only the variable **keys** are documented here — supply your own values.

| Variable         | Required | Default                  | Used by                                      |
| ---------------- | -------- | ------------------------ | -------------------------------------------- |
| `OPENAI_API_KEY` | yes      | —                        | `langchain-openai`, `openai.AsyncOpenAI`     |
| `QDRANT_URL`     | no       | `http://localhost:6333`  | `src/rag_pipeline/constants.py` (Compose overrides to `http://vector_db:6333`) |

---

## Quick start (Docker Compose)

```bash
# 1. Provide credentials
cd server
cp .env.example .env
echo 'OPENAI_API_KEY=sk-...' >> .env

# 2. Boot the stack (FastAPI on :8000, Qdrant on :6333, client on :5173)
docker-compose up --build

# 3. Open the client at http://localhost:5173, or health check the API
curl http://localhost:8000/health
# {"message":"Server is running!"}
```

The Docker Compose stack runs three services:

| Service     | Image           | Port | Role                                |
| ----------- | --------------- | ---- | ----------------------------------- |
| `app`       | built locally   | 8000 | FastAPI application                 |
| `vector_db` | `qdrant/qdrant` | 6333 | Vector store for embeddings         |
| `client`    | built locally   | 5173 | React + Vite dev server             |

The app container mounts `./src` for hot reload (`--reload`), and the client container mounts `../client` for Vite HMR, so source edits take effect without rebuilding. The client reads the API base URL from `VITE_API_BASE_URL` (default `http://localhost:8000`).

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

## AI-assisted development workflow

This project is built with [Claude Code](https://claude.com/claude-code). The client app (search page, add-case-study page, and the API integration) was developed feature by feature with an AI pair-programmer, guided by checked-in context files so every session starts with the same understanding of the project.

### What the AI is used for

- **Implementing frontend features** — React/TypeScript/Tailwind UI built against the screenshots in `context/designs/`.
- **Refactoring to a target structure** — e.g. moving the add-case-study page logic into `features/`, `hooks/` and `lib/api/` layers.
- **Debugging** — e.g. tracing a browser CORS error to the real cause (a 500 from a missing knowledge-base directory).
- **Reviewing** — checking changes against the feature goals and the frontend coding standards before merging.
- **Keeping docs current** — specs, feature history and this README.

### Context files

`CLAUDE.md` imports the files in `context/`, which give the AI persistent project knowledge:

| File | Purpose |
| ---- | ------- |
| `context/project-overview.md` | Backend API contract, data shapes, known behavior |
| `context/frontend-coding-standards.md` | Stack, naming, code style, patterns |
| `context/ai-interactions.md` | How the AI should work: communication, branching, commits, when stuck |
| `context/current-feature.md` | The single active feature: goals, notes, and a running history |
| `context/features/*.md` | One spec per feature or fix |
| `context/designs/*.png` | UI design references |

### Feature lifecycle (`/feature` skill)

Every feature or fix follows the same loop, driven by the custom `/feature` slash command (`.claude/skills/feature/`):

1. **Spec** — write a spec in `context/features/<name>.md`.
2. **`/feature load <name>`** — load the spec (or an inline description) into `current-feature.md` as goals and notes.
3. **`/feature start`** — set status to In Progress, create a `feature/<name>` branch, and implement the goals.
4. **Test and iterate** — verify in the browser, run `npm run build` and `npm run lint`, and fix issues.
5. **`/feature review`** — check goals met, code quality, and scope creep, ending in a ready/needs-changes verdict.
6. **`/feature explain`** — document what changed and why (optional).
7. **`/feature complete`** — commit with a conventional message, merge to `master`, delete the branch, reset `current-feature.md` with a History entry, and push.

### Review agent

`.claude/agents/client-code-scanner.md` is a read-only review subagent that checks frontend diffs against `context/frontend-coding-standards.md` (naming, imports, TypeScript, accessibility). It is meant to run after frontend changes and before committing.

### Ground rules for the AI

- Minimal, focused changes — no unrequested features or unrelated refactors.
- Reuse and refactor existing code instead of duplicating it.
- Conventional commit messages, no attribution trailers, and one feature per commit.
- If something fails after 2–3 attempts, stop and explain rather than guessing.

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

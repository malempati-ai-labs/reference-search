# Reference Search — Project Overview
 
## 1. What this project is
 
**Reference Search** is an internal tool for sales engineers, solution consultants, and pre-sales teams. It helps answer: *"Which of our existing customers solved a problem like the one this prospect is describing?"*
 
The backend is a RAG (Retrieval-Augmented Generation) pipeline that:
- Stores customer case studies (company name, challenges, outcomes) in a Qdrant vector database.
- Given a free-text description of a prospect's challenge, retrieves the top 5 semantically similar case studies.
- Uses an LLM to generate a ranked list of 1–3 customer references, each with a reason, supporting evidence, and a confidence score.
**The backend is already built and running.** This document is a stable reference for anything built on top of it (a client app, a script, an internal tool, etc.) — it describes the API contract, data shapes, and known behavior, without assuming any particular frontend, framework, or feature set.
 
## 2. Users & core use cases
 
- **Search for a reference**: given a prospect's challenge described in plain language (e.g. "we have a very large product catalog spread across multiple countries"), get back a ranked list of matching customer case studies with reasoning.
- **Manage the knowledge base**: add new case studies (company name, list of challenges, list of outcomes) to grow the reference library over time.
There is no authentication in the backend as specified — assume none exists unless told otherwise.
 
## 3. Backend API contract
 
Base URL: `http://localhost:8000` locally (via Docker Compose). Treat as configurable — don't hardcode it into anything built on top.
 
### `GET /health`
Health check.
```json
{ "message": "Server is running!" }
```
 
### `POST /api/case-studies`
Ingest one or more new case studies into the knowledge base. Duplicate companies (case-insensitive name match) are skipped server-side.
 
**Request body:**
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
 
**Response:** `201 Created`
```json
{ "message": "The knowledge base is updated." }
```
 
⚠️ **Behavioral note:** every ingest call triggers a full drop-and-rebuild of the vector index server-side (`initiate_rag_pipeline`). Cost and latency scale with the *total* knowledge-base size, not the size of the new batch — this can get noticeably slower as the knowledge base grows. Anything calling this endpoint should not assume a fast response.
 
### `GET /api/customer-references?search=<query>`
The core search endpoint. Takes a free-text query and returns up to 3 ranked references.
 
**Response:** `200 OK`
```json
{
  "data": [
    {
      "companyName": "SHOPcloud360",
      "reason": "Operates a platform with one million products...",
      "relevantChallenges": ["Managing a catalog of one million products"],
      "relevantOutcomes": ["350 online shops managed centrally"],
      "confidenceScore": 92
    }
  ]
}
```
 
Confirmed from the actual route handler (`main.py`): the response is always wrapped under a `data` key, and is normalized to `data: []` whenever the underlying search returns no result (including the internal `None` case) — there's only one empty-state to handle, never a null.
 
## 4. Data shapes (mirroring the backend Pydantic DTOs)
 
```
CaseStudyDto
├── companyName: string
├── challenges: string[]
└── outcomes: string[]
 
CreateCaseStudiesDto
└── caseStudies: CaseStudyDto[]
 
CustomerReference
├── companyName: string
├── reason: string
├── relevantChallenges: string[]
├── relevantOutcomes: string[]
└── confidenceScore: int (0–100)
```
 
Note: internally the search pipeline uses a `CustomerReferences` model with a `customerReferences` field, but that never reaches the API consumer in that shape — the route handler always re-wraps it as `{"data": [...]}`. Only the wire format above (`data: []` at the top level of the response) matters to anything consuming this API.
 
## 5. Knowledge-base format (for context, not directly consumed by clients)
 
`case-studies.txt` is a plain-text file built up incrementally via the ingest endpoint. Each company is delimited by a `Company Name:` header, which is also the chunking boundary for embedding:
 
```
Company Name: SHOPcloud360
 
Challenges:
   1. Managing a catalog of one million products
   2. Onboarding hundreds of merchants onto a single platform
 
Outcomes:
   - 350 online shops managed centrally
   - 1M products served from a single backend
```
 
Each chunk becomes one embedded document scoped by `metadata.company_name`, stored in the Qdrant `case-studies` collection.
 
## 6. Known behavioral characteristics worth designing around
 
- **Both endpoints are LLM/embedding-backed and can be slow.** Neither should be treated as a fast, cheap call — anything built on top should assume noticeable latency, especially on ingest.
- **Ingest is a full reindex, not incremental.** Every `POST /api/case-studies` rebuilds the whole vector store from the full knowledge-base file, so its cost grows with total knowledge-base size over time.
- **Search returns at most 3 ranked results**, or an empty array — there's no pagination and no partial/streaming response.
- **No authentication** exists at the API layer currently.
- **No endpoint exists to list or browse all existing case studies** — only to add new ones and to search. If a future feature needs to show what's in the knowledge base, that's a gap to raise with the backend, not something to build around client-side.

## 7. Out of scope / not part of this backend
 
- Authentication or authorization.
- Editing or deleting existing case studies.
- Listing/browsing the full knowledge base.
- Direct access to Qdrant — everything goes through the FastAPI layer.
- Retrieval/response evaluation tooling (`retrieval_eval.py`, `response_eval.py`) — these are backend/ops scripts, not part of the API surface.

## 8. Open questions
 
- Will an endpoint to list/browse all existing case studies be added? Worth confirming before building any feature that assumes one.
- Is there a plan to add authentication, or is this intentionally an internal, unauthenticated tool?
- What's the expected/typical latency for both endpoints in the target deployment (vs. local Docker Compose), for realistic UX planning?
 

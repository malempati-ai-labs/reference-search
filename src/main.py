from fastapi import FastAPI, status
from src.dtos import CreateCaseStudiesDto
from .rag_pipeline.inngest import initiate_rag_pipeline
from .rag_pipeline.search import search_customer_references

app = FastAPI()

@app.get("/health")
def health():
    return {"message": "Server is running!"}


@app.post("/api/case-studies", status_code=status.HTTP_201_CREATED)
async def ingest_case_studies(dto: CreateCaseStudiesDto):
    await initiate_rag_pipeline(dto)
    return {
        "message": "The knowledge base is updated."
    }


@app.get("/api/customer-references", status_code=status.HTTP_200_OK)
async def get_customer_references(search: str):
    results = await search_customer_references(search)
    return {
        'data': results
    }

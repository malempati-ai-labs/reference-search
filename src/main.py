from fastapi import FastAPI, status
from src.dtos import CreateCaseStudiesDto
from .rag_pipeline.inngest import initiate_rag
from .rag_pipeline.chat import search_customer_references

app = FastAPI()

@app.get("/root")
def root():
    return {"message": "I am running!"}


@app.post("/api/case-studies", status_code=status.HTTP_201_CREATED)
async def create_case_studies(dto: CreateCaseStudiesDto):
    await initiate_rag(dto)
    return {"message": "Added to knowledge base"}


@app.get("/api/customer-references", status_code=status.HTTP_200_OK)
async def get_customer_references(search: str):
    results = await search_customer_references(search)
    return {
        'message': results
    }

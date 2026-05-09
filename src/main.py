from fastapi import FastAPI, status
from src.dtos import CreateCaseStudiesDto
from .rag_pipeline.inngest import initiate_rag

app = FastAPI()

@app.get("/root")
def root():
    return {"message": "I am running!"}


@app.post("/api/case-studies", status_code=status.HTTP_201_CREATED)
async def create_case_studies(dto: CreateCaseStudiesDto):
    await initiate_rag(dto)
    return {"companies": "added to knowledge base"}

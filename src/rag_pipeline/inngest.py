import aiofiles
import os
from pathlib import Path
from src.dtos import CreateCaseStudiesDto
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import AsyncQdrantClient


load_dotenv(override=True)

FILE_PATH = str(Path(__file__).parent.parent /
                "knowledge-base" / "case-studies.txt")

COLLECTION_NAME = 'case-studies'

QDRANT_URL = os.getenv('QDRANT_URL', 'http://localhost:6333')

embedding_model = OpenAIEmbeddings(model='text-embedding-3-small')

aQdrant_client = AsyncQdrantClient(url=QDRANT_URL, check_compatibility=False)


async def add_to_knowledge_base(dto: CreateCaseStudiesDto):
    for caseStudy in dto.caseStudies:
        formatted_text = f"Company Name: {caseStudy.companyName}\n\n"

        formatted_text += "Challenges:\n"
        for index, challenge in enumerate(caseStudy.challenges, start=1):
            formatted_text += f"   {index}. {challenge}\n"

        formatted_text += "\nKey Metrics:\n"
        for metric in caseStudy.keyMetrics:
            formatted_text += f"   - {metric}\n"

        formatted_text += "\n\n"

        # Append asynchronously
        async with aiofiles.open(FILE_PATH, mode="a", encoding="utf-8") as file:
            await file.write(formatted_text)


async def create_chunks():
    documents = []
    async with aiofiles.open(FILE_PATH, mode="r", encoding="utf-8") as file:
        content = await file.read()

    # Split by marker
    sections = content.split("Company Name:")

    # Clean empty parts and restore header
    chunks = [
        "Company Name:" + section.strip()
        for section in sections
        if section.strip()
    ]

    for chunk in chunks:
        lines = chunk.splitlines()
        company_name = lines[0].replace("Company Name:", "").strip()
        doc = Document(
            page_content=chunk.replace("\n", " "),
            metadata={
                "company_name": company_name
            }
        )

        documents.append(doc)

    return documents


async def clean_vector_store(collectionName: str):
    try:
        print('Cleaning up existing collection')
        collections = await aQdrant_client.get_collections()
        if collectionName in [collection_name.name for collection_name in collections.collections]:
            await aQdrant_client.delete_collection(collection_name=collectionName)
            print('Deleted existing collection')
    except Exception as e:
        print('Something went wrong during cleaning vector store', e)


async def create_embeddings(chunks: list[Document]):
    QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embedding_model,
        url=QDRANT_URL,
        collection_name=COLLECTION_NAME
    )
    print('Indexing of documents is done!')


async def initiate_rag(dto: CreateCaseStudiesDto):
    try:
        await add_to_knowledge_base(dto)
        chunks = await create_chunks()
        await clean_vector_store(COLLECTION_NAME)
        await create_embeddings(chunks)
    except Exception as e:
        print('Something went wrong during RAG initiation', e)

import aiofiles
import os
from src.dtos import CreateCaseStudiesDto
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import AsyncQdrantClient
from .constants import QDRANT_URL, KNOWLEDGE_BASE_FILE_PATH, VECTOR_STORE_COLLECTION_NAME, EMBEDDING_MODEL


load_dotenv(override=True)

embedding_model = OpenAIEmbeddings(model=EMBEDDING_MODEL)

aQdrant_client = AsyncQdrantClient(url=QDRANT_URL, check_compatibility=False)


async def read_knowledge_base_content():
    """Reads the content of the knowledge base file asynchronously."""
    try:
        async with aiofiles.open(KNOWLEDGE_BASE_FILE_PATH, mode="r", encoding="utf-8") as file:
            return await file.read()
    except Exception as e:
        print(f"Error reading knowledge base file: {e}")
        raise


def parse_company_sections(content: str):
    """Parses the file content into individual company sections."""
    try:
        sections = content.split("Company Name:")
        return [
            "Company Name:" + section.strip()
            for section in sections
            if section.strip()
        ]
    except Exception as e:
        print(f"Error parsing company sections: {e}")
        raise


async def load_existing_companies():
    """Loads and extracts existing company names from the knowledge base file."""
    try:
        existing_companies = set()
        if os.path.exists(KNOWLEDGE_BASE_FILE_PATH):
            content = await read_knowledge_base_content()
            sections = content.split("Company Name:")
            for section in sections:
                company_name = section.splitlines(
                )[0].strip() if section.strip() else ""
                if company_name:
                    existing_companies.add(company_name.lower())
        return existing_companies
    except Exception as e:
        print(f"Error loading existing companies: {e}")
        raise


def format_case_study(case_study):
    """Formats a single case study into the required text structure."""
    try:
        formatted_text = f"Company Name: {case_study.companyName}\n\n"
        formatted_text += "Challenges:\n"
        for index, challenge in enumerate(case_study.challenges, start=1):
            formatted_text += f"   {index}. {challenge}\n"
        formatted_text += "\nOutcomes:\n"
        for metric in case_study.outcomes:
            formatted_text += f"   - {metric}\n"
        formatted_text += "\n\n"
        return formatted_text
    except Exception as e:
        print(f"Error formatting case study: {e}")
        raise


async def append_to_file(texts: list[str]):
    """Appends a list of formatted texts to the knowledge base file."""
    try:
        if texts:
            async with aiofiles.open(KNOWLEDGE_BASE_FILE_PATH, mode="a", encoding="utf-8") as file:
                await file.write("".join(texts))
    except Exception as e:
        print(f"Error appending to knowledge base file: {e}")
        raise


async def add_to_knowledge_base(dto: CreateCaseStudiesDto):
    """Adds new case studies to the knowledge base, avoiding duplicates."""
    try:
        existing_companies = await load_existing_companies()
        texts_to_append = []
        for caseStudy in dto.caseStudies:
            company_name_lower = caseStudy.companyName.strip().lower()
            if company_name_lower in existing_companies:
                print(f"Skipping existing company: {caseStudy.companyName}")
                continue
            formatted_text = format_case_study(caseStudy)
            texts_to_append.append(formatted_text)
            existing_companies.add(company_name_lower)
        await append_to_file(texts_to_append)
    except Exception as e:
        print(f"Error adding to knowledge base: {e}")
        raise


async def create_chunks():
    """
        Creates Document objects from the knowledge base content for embedding.
        Chunking Strategy: Structure-based
            - Best results when we have control over document formatting (like internal company reports)
    """
    try:
        documents = []
        content = await read_knowledge_base_content()
        chunks = parse_company_sections(content)

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
    except Exception as e:
        print(f"Error creating chunks: {e}")
        raise


async def clean_vector_store(collectionName: str):
    """
        Deletes the specified collection from the vector store if it exists.
        Note: For production prefer data upsert instead of full-cleanup 
    """
    try:
        print('Cleaning up existing collection')
        collections = await aQdrant_client.get_collections()
        if collectionName in [collection_name.name for collection_name in collections.collections]:
            await aQdrant_client.delete_collection(collection_name=collectionName)
            print('Deleted existing collection')
    except Exception as e:
        print('Something went wrong during cleaning vector store', e)


async def create_embeddings(chunks: list[Document]):
    """Creates and stores embeddings for the given documents in the vector store."""
    try:
        QdrantVectorStore.from_documents(
            documents=chunks,
            embedding=embedding_model,
            url=QDRANT_URL,
            collection_name=VECTOR_STORE_COLLECTION_NAME,
        )
        print('Indexing of documents is done!')
    except Exception as e:
        print(f"RAG Initialization Failed: {e}")
        raise


async def initiate_rag_pipeline(dto: CreateCaseStudiesDto):
    """Initiates the full RAG pipeline: adds to knowledge base, creates chunks, cleans vector store, and creates embeddings."""
    try:
        await add_to_knowledge_base(dto)
        chunks = await create_chunks()
        await clean_vector_store(VECTOR_STORE_COLLECTION_NAME)
        await create_embeddings(chunks)
    except Exception as e:
        print(f"RAG Initialization Failed: {e}")
        raise

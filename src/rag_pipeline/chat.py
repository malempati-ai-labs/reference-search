from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
import os


embedding_model = OpenAIEmbeddings(model='text-embedding-3-small')
COLLECTION_NAME = 'case-studies'
QDRANT_URL = os.getenv('QDRANT_URL', 'http://localhost:6333')


async def retrieve_similar_documents(query: str):
    try:
        print('Retrieving similar documents for user query')
        vector_store = QdrantVectorStore.from_existing_collection(
            collection_name=COLLECTION_NAME,
            url=QDRANT_URL,
            embedding=embedding_model
        )

        retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 1})
        results = await retriever.ainvoke(input=query)
        return results
    except Exception as e:
        print('Something went wrong during retrieve similar documents for user query', e)

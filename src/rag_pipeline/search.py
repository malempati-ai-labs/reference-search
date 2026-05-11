from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import AsyncOpenAI
from dotenv import load_dotenv
from .constants import QDRANT_URL, VECTOR_STORE_COLLECTION_NAME, EMBEDDING_MODEL
from src.dtos import CustomerReferences

load_dotenv()

async_openai_client = AsyncOpenAI()

embedding_model = OpenAIEmbeddings(model=EMBEDDING_MODEL)

RETRIEVAL_K = 5

SYSTEM_PROMPT = """
You are an AI assistant that matches customer business challenges to the most relevant Intershop customer references.

You are given structured Case Study Data Context containing:
- companyName
- challenges
- outcomes

Your task is to recommend the most relevant customer references for a user's challenge.

IMPORTANT MATCHING RULES:
1. Use BOTH the "challenges" and the "outcomes" fields when determining relevance.
2. Do not rely only on keyword similarity.
3. Consider business context, scale, and successful outcomes.
4. Outcomes are strong indicators of proven success and should influence ranking.
5. Return the most relevant companies even if the wording differs semantically.
6. A company can match based on:
   - similar operational problems
   - similar transformation goals
   - similar technical complexity
   - similar business scale
   - similar measurable outcomes

Examples:
- If a user mentions scalability, international growth, or multi-country operations, prioritize companies whose outcomes mention many countries, large revenue, or global presence.
- If a user mentions product catalog complexity, prioritize companies with outcomes mentioning hundreds of thousands or millions of products.
- If a user mentions automation or self-service, prioritize companies with outcomes showing increased online orders or reduced manual effort.

Response format for each customer reference:
Return:
- companyName
- reason
- relevantChallenges
- relevantOutcomes
- confidenceScore (0-100)

Return between 1 and 3 customer references ranked by relevance as a list of JSON objects.
Do not return more than 3 references.

Always explain WHY the recommendation was selected using both challenges and outcomes.

Case Study Data Context:
{context}
"""


async def retrieve_similar_documents(query: str):
    """Retrieves similar documents from the vector store based on the query."""
    try:
        print('Retrieving similar documents for user query')
        vector_store = QdrantVectorStore.from_existing_collection(
            collection_name=VECTOR_STORE_COLLECTION_NAME,
            url=QDRANT_URL,
            embedding=embedding_model
        )

        retriever = vector_store.as_retriever(
            search_type="similarity", search_kwargs={"k": RETRIEVAL_K})
        results = await retriever.ainvoke(input=query)
        return results
    except Exception as e:
        print('Something went wrong during retrieve similar documents for user query', e)
        raise


def format_context(docs: list):
    """Formats retrieved documents into a context string."""
    try:
        return "\n\n".join(doc.page_content for doc in docs)
    except Exception as e:
        print(f"Error formatting context: {e}")
        raise


async def call_llm_for_references(query: str, system_prompt: str):
    """Calls the OpenAI LLM to parse and return customer references."""
    try:
        response = await async_openai_client.responses.parse(
            model='gpt-5-nano',
            input=query,
            instructions=system_prompt,
            text_format=CustomerReferences,
        )
        return response.output_parsed if response.output_parsed is not None else None
    except Exception as e:
        print(f"Error calling LLM for references: {e}")
        raise


async def search_customer_references(query: str):
    """Searches and returns the most relevant customer references for a given query."""
    try:
        docs = await retrieve_similar_documents(query)
        if not docs or len(docs) <= 0:
            return None
        context = format_context(docs)
        system_prompt = SYSTEM_PROMPT.format(context=context)
        return await call_llm_for_references(query, system_prompt)
    except Exception as e:
        print(f"Error during search_customer_references: {e}")
        raise

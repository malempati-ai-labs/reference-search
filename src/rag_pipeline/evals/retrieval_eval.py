from .test_data import RETRIEVAL_TEST_DATA

from typing import List, Dict, Any
from langchain_core.documents import Document
import asyncio
from src.rag_pipeline.search import retrieve_similar_documents



def calculate_recall_at_k(
    retrieved_docs: List[Document],
    relevant_companies: List[str],
    k: int = 5,
) -> Dict[str, Any]:
    """
    Calculate Recall@K as percentage.
    """

    top_k_docs = retrieved_docs[:k]

    retrieved_company_names = [
        doc.metadata.get("company_name")
        for doc in top_k_docs
        if doc.metadata.get("company_name")
    ]

    matched_companies = list(
        set(retrieved_company_names).intersection(set(relevant_companies))
    )

    recall = len(matched_companies) / len(relevant_companies)


    return {
        "recall_at_k": round(recall, 4),
        "k": k,
        "retrieved_companies": retrieved_company_names,
        "relevant_companies": relevant_companies,
        "matched_companies": matched_companies,
        "num_matches": len(matched_companies),
        "total_relevant": len(relevant_companies),
    }


def calculate_mrr(
    retrieved_docs: List[Any],
    relevant_companies: List[str],
    k: int = 5,
) -> float:
    """
    Calculate reciprocal rank for a single query.
    """

    top_k_docs = retrieved_docs[:k]

    retrieved_company_names = [
        doc.metadata.get("company_name")
        for doc in top_k_docs
        if doc.metadata.get("company_name")
    ]

    for rank, company_name in enumerate(retrieved_company_names, start=1):

        if company_name in relevant_companies:
            return 1 / rank

    return 0.0


async def run_retrieval_evaluation():

    recall_scores = []
    reciprocal_ranks = []

    print("\n==============================")
    print("RUNNING RETRIEVAL EVALUATION")
    print("==============================\n")

    for idx, item in enumerate(RETRIEVAL_TEST_DATA, start=1):

        query = item["query"]
        relevant_docs = item["relevantDocs"]

        print(f"\nTEST CASE #{idx}")
        print(f"Query: {query}")

        # ----------------------------------------
        # Retrieve documents from vector DB
        # ----------------------------------------
        retrieved_docs = await retrieve_similar_documents(query)

        if retrieved_docs is None:
            print("No documents from vector DB found for evaluation")
            return

        # ----------------------------------------
        # Recall@K
        # ----------------------------------------

        recall_result = calculate_recall_at_k(
            retrieved_docs=retrieved_docs,
            relevant_companies=relevant_docs,
            k=5,
        )

        recall_scores.append(
            recall_result["recall_at_k"]
        )

 # ----------------------------------------
        # MRR
        # ----------------------------------------

        reciprocal_rank = calculate_mrr(
            retrieved_docs=retrieved_docs,
            relevant_companies=relevant_docs,
            k=5,
        )

        reciprocal_ranks.append(reciprocal_rank)

        # ----------------------------------------
        # Print results
        # ----------------------------------------

        print(f"\nRetrieved Companies:")
        print(recall_result["retrieved_companies"])

        print(f"\nRelevant Companies:")
        print(relevant_docs)

        print(f"\nMatched Companies:")
        print(recall_result["matched_companies"])

        print(f"\nRecall@5:")
        print(f"{recall_result['recall_at_k']}")

        print(f"\nReciprocal Rank:")
        print(round(reciprocal_rank, 4))

        print("\n----------------------------------")

    # ========================================================
    # FINAL METRICS
    # ========================================================

    avg_recall = round(sum(recall_scores) / len(recall_scores), 2)
    mrr = round(sum(reciprocal_ranks) / len(reciprocal_ranks), 4)

    print("\n====================================")
    print("FINAL EVALUATION RESULTS")
    print("====================================")

    print(f"\nAverage Recall@5: {avg_recall}")
    print(f"Average MRR: {mrr}")
    print("\n====================================")



if __name__ == "__main__":
    asyncio.run(run_retrieval_evaluation())

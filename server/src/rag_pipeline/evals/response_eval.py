import random
import json
from openai import AsyncOpenAI
import asyncio

from .test_data import RESPONSE_TEST_DATA
from src.rag_pipeline.search import search_customer_references

client = AsyncOpenAI()

def get_random_test_case():
    return random.choice(RESPONSE_TEST_DATA)

def build_judge_prompt(
    query: str,
    expected_primary: str,
    relevant_refs: list[str],
    prediction
):
    return f"""
You are an expert evaluator for enterprise RAG systems.

Your task is to evaluate whether the generated customer references
correctly answer the customer challenge query.

USER QUERY:
{query}

EXPECTED PRIMARY CUSTOMER REFERENCE:
{expected_primary}

EXPECTED RELEVANT CUSTOMER REFERENCES:
{json.dumps(relevant_refs, indent=2)}

GENERATED RESPONSE:
{json.dumps(prediction, indent=2, ensure_ascii=False)}

Evaluate the response using the following criteria:

1. relevance_score (0-5)
- Does the response match the customer challenge?

2. primary_reference_score (0-5)
- Is the expected primary customer reference correctly identified and ranked highly?

3. evidence_grounding_score (0-5)
- Are the reasons grounded in the provided customer challenges and outcomes?

4. completeness_score (0-5)
- Does the response include multiple relevant customer references?

5. hallucination_score (0-5)
- Penalize invented claims or unsupported statements.

Return ONLY valid JSON in this format:

{{
  "relevance_score": 0,
  "primary_reference_score": 0,
  "evidence_grounding_score": 0,
  "completeness_score": 0,
  "hallucination_score": 0,
  "final_score": 0.0,
  "summary": ""
}}
"""


async def evaluate_random_test_case():

    try:
        # Pick random test case
        test_case = get_random_test_case()

        query = test_case["query"]

        print("\n===================================")
        print("RANDOM TEST CASE")
        print("===================================")
        print(f"Query: {query}")

        # Generate prediction from your RAG system
        prediction = await search_customer_references(query)

        if prediction is None:
            print("Could not generate prediction")
            return

        prediction_dict = prediction.model_dump()

        print(json.dumps(prediction_dict, indent=2, ensure_ascii=False))

        # Build judge prompt
        judge_prompt = build_judge_prompt(
            query=query,
            expected_primary=test_case["expectedPrimaryGroundTruthCustomerReference"],
            relevant_refs=test_case["groundTruthRelevantCustomerReference"],
            prediction=prediction_dict
        )

        # Ask LLM to judge
        judge_response = await client.responses.create(
            model="gpt-5",
            input=judge_prompt
        )

        # Print result
        print("\n===================================")
        print("LLM JUDGE EVALUATION")
        print("===================================")

        print(judge_response.output_text)
    except Exception as e:
        print("Something went wrong during evaluation", e)


if __name__ == '__main__':
    asyncio.run(evaluate_random_test_case())

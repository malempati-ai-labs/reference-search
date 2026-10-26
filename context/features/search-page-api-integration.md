# Search Page API Integration

## Goal
- Replace the dummy data in the search results components with real data from the backend.

## API Contract

GET /api/customer-references?search=<query>

{
  "data": [
    {
      "companyName": "SHOPcloud360",
      "reason": "Operates a platform with one million products...",
      "relevantChallenges": ["Managing a catalog of one million products"],
      "relevantOutcomes":   ["350 online shops managed centrally"],
      "confidenceScore": 92
    }
  ]
}

Note: If retrieval returns no documents, data will be [].

## What it should do
 
- Wire the search form (input + Search button) to the endpoint above
- Trim the query and block empty submissions (basic validation message)
- Pressing Enter or clicking Search triggers the request
- Make the example "Try:" chips fill the input and run the search
- Put the single `fetch` call in `lib/api`, with the request/response types and URL-encoding of the query
- Map the API response to the existing result card props
- Show these states:
  - **Idle:** no results section yet
  - **Loading:** disable the Search button, show a loading indicator or skeleton cards
  - **Success:** heading `Top N references for “<query>”` (N = number returned) and the ranked cards
  - **Empty:** friendly "No matching references found" message
  - **Error:** clear error message with a retry option (network failure or non-2xx response)
- Keep the heading showing the query that was actually searched, not what is currently typed
- Handle slow responses gracefully (the LLM call can take several seconds)

## What it should not do
 
- No backend changes
- No `fetch` calls outside `lib/api`
- No hardcoded/mock data in the running app (it may remain in tests)
- No changes to the Add Case Study page
- No search history, caching across sessions, or saved queries
- No streaming responses, pagination, or filters
- No auth
- No redesign of the result cards, keep the current look


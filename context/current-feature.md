# Current Feature: Search Page API Integration

<!-- Feature Name -->

## Status

<!-- Not Started|In Progress|Completed -->

In Progress

## Goals

<!-- Goals & requirements -->

- Replace the dummy data in the search results components with real data from the backend
- Wire the search form (input + Search button) to `GET /api/customer-references?search=<query>`
- Trim the query and block empty submissions with a basic validation message
- Pressing Enter or clicking Search triggers the request
- "Try:" chips fill the input and run the search
- Single `fetch` call in `lib/api`, with request/response types and URL-encoding of the query
- Map the API response to the existing result card props
- Show these states:
  - Idle: no results section yet
  - Loading: Search button disabled, loading indicator or skeleton cards
  - Success: heading `Top N references for “<query>”` (N = number returned) and the ranked cards
  - Empty: friendly "No matching references found" message
  - Error: clear error message with a retry option (network failure or non-2xx response)
- Heading shows the query that was actually searched, not what is currently typed
- Handle slow responses gracefully (LLM call can take several seconds)

## Notes

<!-- Any extra notes -->

- Spec: `context/features/search-page-api-integration.md`
- Response shape: `{ "data": CustomerReference[] }`; `data` is `[]` when retrieval returns no documents
- Must not: change the backend, call `fetch` outside `lib/api`, keep hardcoded/mock data in the running app (may remain in tests), change the Add Case Study page, add search history/session caching/saved queries, add streaming/pagination/filters/auth, or redesign the result cards

## History

<!-- Keep this updated. Earliest to latest -->

- Project setup and boilerplate cleanup
- Implemented App UI Phase 1: shared header with nav, static Search page (default route), static Add case study page; pushed on `app-ui-phase-1`
- Implemented Add Case Study Interactivity: dynamic add/remove of challenges, outcomes, and company sections; react-hook-form validation; submit logs `CreateCaseStudiesDto`-shaped payload to console; pushed on `feature/add-case-study-interactivity`
- Implemented Logo Links to Homepage: header logo/title is now a React Router `Link` to `/` with hover and focus-visible styles
- Implemented Create Case Study: layered page → `AddCaseStudy` feature component → `useCreateCaseStudies` mutation hook → `createCaseStudies()` fetch API; validation, loading/success/error states; server CORS middleware and auto-created knowledge-base directory
- Implemented Search Page Results: `search-results` feature with `SearchResults` list and `ReferenceCard` (rank, confidence tier badge and bar, reason, challenges/outcomes panels) rendered on the Search page from dummy data; responsive, no API integration

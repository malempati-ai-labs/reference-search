# Create Case Study

## Overview

Users can create one or more case studies from the `add-case-study` page. Submitted case studies are sent to the backend, which updates the knowledge base.

## Goals

- Let a user add multiple case studies in a single submission.
- Keep page, UI, data-fetching, and API logic in separate layers.
- Give clear feedback for loading, success, and error states.
- Ensure any pre-existing code for this feature conforms to the project structure below.

## Out of Scope

- Editing or deleting existing case studies
- Listing or viewing case studies
- Authentication (assumed to be handled elsewhere)

## Project Structure

```
src/
├── pages/
│   └── AddCaseStudyPage.tsx          # Thin container/wrapper for the feature
├── features/
│   └── add-case-study/
│       ├── AddCaseStudy.tsx          # Component: form UI and submit logic
│       ├── hooks/
│       │   └── useCreateCaseStudies.ts   # React Query mutation hook
│       └── types.ts                  # Shared types for this feature
└── lib/
    └── api/
        └── caseStudies.ts            # createCaseStudies() – fetch POST
```

> The page file name and location should follow the project's existing routing convention (e.g. `src/pages/add-case-study/index.tsx`). The rule that matters is that the page stays a thin wrapper.

## Layer Responsibilities

| Layer | Location | Responsibility | Must NOT |
|-------|----------|----------------|----------|
| Page | `src/pages/` | Container/wrapper: route entry point, page layout, page title, and rendering the feature component | Contain form logic, validation, data fetching, or call `fetch` |
| Feature component | `src/features/add-case-study/` | Form UI, validation, and submit handling | Call `fetch` directly |
| Hook | `src/features/add-case-study/hooks/` | React Query mutation | Contain UI concerns |
| API function | `src/lib/api/` | HTTP request with `fetch` | Contain React code |

## Existing Code and Refactoring

Before implementing anything, search the codebase for existing code related to this feature (pages, components, hooks, API calls, types, or inline `fetch` calls on the `add-case-study` page).

- **Do not duplicate.** If any requirement in this spec is already implemented, do not rewrite it from scratch. Reuse and refactor it.
- **Move to the target structure.** Relocate existing code to the file locations defined in "Project Structure" and update all imports.
  - Case-study logic found inside the page → extracted into `src/features/add-case-study/AddCaseStudy.tsx`, leaving the page as a thin wrapper
  - Components containing case-study logic → `src/features/add-case-study/`
  - Mutation or data-fetching hooks → `src/features/add-case-study/hooks/`
  - Direct `fetch` calls → extracted into `src/lib/api/caseStudies.ts`
  - Feature types → `src/features/add-case-study/types.ts`
- **Align with the requirements.** Where existing code differs from the requirements below (for example, calling `fetch` inside the component, putting form logic in the page, using `useQuery` for a POST, or missing loading/error handling), refactor it to comply.
- **Preserve behavior.** Keep existing working behavior unless it contradicts this spec. Do not change unrelated code.
- **Clean up.** Remove dead code, unused files, and leftover imports. Make sure no old copies remain in the previous locations.
- **Verify.** After refactoring, the app must build, type-check, and pass existing tests with no broken imports. Update affected tests to match the new paths.

## Requirements

### 1. Page container (`src/pages/AddCaseStudyPage.tsx`)

- Acts as a **container/wrapper** for the whole feature. It is the route entry point for `add-case-study` and nothing more.
- Renders `<AddCaseStudy />` from `src/features/add-case-study/`.
- May provide page-level concerns only: layout, heading/title, and navigation (e.g. redirecting after success via the component's `onSuccess` prop).
- Must not contain form state, validation, data fetching, `useCreateCaseStudies`, or `fetch` calls.
- Should stay small. If the page grows beyond composing layout and the feature component, the extra logic belongs in the feature.

### 2. API function (`src/lib/api/caseStudies.ts`)

- Export `createCaseStudies(payload: CreateCaseStudiesPayload): Promise<CreateCaseStudiesResponse>`.
- Send a `POST` request to `/api/case-studies` using the native `fetch` API.
- Set the `Content-Type: application/json` header and serialize the body with `JSON.stringify`.
- If `response.ok` is false, throw an `Error` with a meaningful message (use the server's error message if present, otherwise a generic fallback that includes the status code).
- Return the parsed JSON response on success.

### 3. Custom hook (`src/features/add-case-study/hooks/useCreateCaseStudies.ts`)

- Use React Query's `useMutation` with `createCaseStudies` as the `mutationFn`.
- Expose `mutate` / `mutateAsync`, `isPending`, `isError`, `error`, `isSuccess`, `data`, and `reset`.
- Do not put UI concerns (toasts, navigation) in the hook; leave those to the component via `onSuccess` / `onError` callbacks passed by the caller.

### 4. Feature component (`src/features/add-case-study/AddCaseStudy.tsx`)

- Owns all the logic for adding a case study: form state, validation, submission, and feedback states.
- Render a form that supports **one or more** case studies:
  - "Add another case study" and "Remove" controls (at least one entry must always remain).
  - Per case study: `companyName` (text), `challenges` (list of text inputs), `outcomes` (list of text inputs). Each list supports adding and removing items.
- Use `useCreateCaseStudies` for submission. The component must not call `fetch` directly.
- Accept an optional `onSuccess` prop so the parent page can react to a successful submission (e.g. navigate) without owning any logic.

### 5. Validation (client-side, before submitting)

- `companyName`: required, trimmed, non-empty.
- `challenges` and `outcomes`: each must contain at least one non-empty item. Trim items and drop empty ones before sending.
- Show inline error messages next to the offending fields. Do not send a request while validation fails.

### 6. Loading, success, and error states

| State | Behavior |
|-------|----------|
| Loading | Disable the submit button and form inputs, and show a loading indicator or "Submitting…" label. Prevent duplicate submissions. |
| Success | Show the message returned by the API (`message`), and reset the form to its initial state. |
| Error | Show a visible, accessible error message (`role="alert"`) with the failure reason. Keep the user's input intact so they can retry. |

## Types

```ts
export interface CaseStudy {
  companyName: string;
  challenges: string[];
  outcomes: string[];
}

export interface CreateCaseStudiesPayload {
  caseStudies: CaseStudy[];
}

export interface CreateCaseStudiesResponse {
  message: string;
}
```

## API Endpoint

`POST /api/case-studies`

**Request body**

```json
{
  "caseStudies": [
    {
      "companyName": "SHOPcloud360",
      "challenges": [
        "Managing a catalog of one million products",
        "Onboarding hundreds of merchants onto a single platform"
      ],
      "outcomes": [
        "350 online shops managed centrally",
        "1M products served from a single backend"
      ]
    }
  ]
}
```

**Success response** (`200 OK`)

```json
{ "message": "The knowledge base is updated." }
```

**Error response**

Any non-2xx status is treated as a failure. If the body contains a `message` field, display it; otherwise display a generic error.

## Acceptance Criteria

- [ ] A user can submit a single case study and see the success message.
- [ ] A user can add multiple case studies and submit them in one request.
- [ ] Submitting with an empty company name, or with no challenges or outcomes, is blocked and shows inline errors.
- [ ] The submit button is disabled and a loading indicator is shown while the request is in flight.
- [ ] A failed request (network error or non-2xx) shows an error message and preserves the form data.
- [ ] After a successful submission, the form resets.
- [ ] The page in `src/pages` only renders the feature component and page-level layout. It contains no form logic, hooks for data fetching, or `fetch` calls.
- [ ] The page uses the component; the component uses the custom hook; the hook uses the `lib` function; only the `lib` function calls `fetch`.
- [ ] Any pre-existing implementation of the above has been refactored into the project structure, with no duplicate or leftover files, and the project builds, type-checks, and passes tests.

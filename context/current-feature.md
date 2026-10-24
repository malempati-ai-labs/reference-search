# Current Feature: Create Case Study

<!-- Feature Name -->

## Status

<!-- Not Started|In Progress|Completed -->

In Progress

## Goals

<!-- Goals & requirements -->

- Let a user add multiple case studies in a single submission.
- Keep page, UI, data-fetching, and API logic in separate layers.
- Give clear feedback for loading, success, and error states.
- Ensure any pre-existing code for this feature conforms to the project structure below.
- Page (`src/pages/AddCaseStudyPage.tsx`) is a thin wrapper that only renders `<AddCaseStudy />` and page-level layout.
- API function `createCaseStudies()` in `src/lib/api/caseStudies.ts` does `POST /api/case-studies` with native `fetch`; throws a meaningful `Error` on non-ok responses.
- `useCreateCaseStudies` hook in `src/features/add-case-study/hooks/` wraps `useMutation`; no UI concerns.
- `AddCaseStudy.tsx` owns form state, validation, submission, and feedback; accepts optional `onSuccess` prop; never calls `fetch` directly.
- Validation: `companyName` required/trimmed; `challenges` and `outcomes` need at least one non-empty item; trim and drop empties before sending; inline errors; no request while invalid.
- Loading: disable submit and inputs, show "Submitting…", prevent duplicate submissions.
- Success: show API `message` and reset the form.
- Error: show `role="alert"` message with failure reason and keep user input.
- Refactor pre-existing code into the target structure with no duplicates or leftovers; build, type-check, and tests pass.

## Notes

<!-- Any extra notes -->

- Spec: `context/features/create-case-study.md`
- Target structure:
  - `src/pages/AddCaseStudyPage.tsx`
  - `src/features/add-case-study/AddCaseStudy.tsx`
  - `src/features/add-case-study/hooks/useCreateCaseStudies.ts`
  - `src/features/add-case-study/types.ts`
  - `src/lib/api/caseStudies.ts`
- Search for existing add-case-study code first (page, components, hooks, inline fetch, types); reuse and refactor rather than rewrite, and update imports/tests.
- Currently the form submit only logs a `CreateCaseStudiesDto`-shaped payload to the console.
- Base API URL must be configurable, not hardcoded.
- Out of scope: editing/deleting, listing/viewing case studies, authentication.
- Types: `CaseStudy`, `CreateCaseStudiesPayload`, `CreateCaseStudiesResponse { message: string }`.
- Backend ingest does a full reindex, so expect slow responses.

## History

<!-- Keep this updated. Earliest to latest -->

- Project setup and boilerplate cleanup
- Implemented App UI Phase 1: shared header with nav, static Search page (default route), static Add case study page; pushed on `app-ui-phase-1`
- Implemented Add Case Study Interactivity: dynamic add/remove of challenges, outcomes, and company sections; react-hook-form validation; submit logs `CreateCaseStudiesDto`-shaped payload to console; pushed on `feature/add-case-study-interactivity`
- Implemented Logo Links to Homepage: header logo/title is now a React Router `Link` to `/` with hover and focus-visible styles

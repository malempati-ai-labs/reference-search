# Add Case Study Interactivity Spec

## Overview

The Add case study page (`client/src/pages/add-case-study-page.tsx`) currently renders the static UI for Phase 1 (see `app-ui-phase-1-spec.md`) with no behavior wired up. This feature adds the interactivity for that page: dynamic challenge/outcome fields, dynamic company sections, form validation, and a submit handler — without touching the visual design already implemented. No backend integration (no `POST /api/case-studies` call) is part of this feature; submission only logs to console.

## Requirements

### Add challenge
- Clicking "Add challenge" within a company section appends a new empty challenge input to that company's Challenges list.
- Each company section manages its own list of challenges independently.

### Add outcome
- Clicking "Add outcome" within a company section appends a new empty outcome input to that company's Outcomes list.
- Each company section manages its own list of outcomes independently.

### Delete challenge / outcome
- Each challenge and outcome input has a trash icon button.
- Clicking the trash icon removes that specific challenge or outcome input from the list.
- A company must always retain at least one challenge input and at least one outcome input — the trash icon is disabled (or hidden) when it is the last remaining item in its list, consistent with the `challenges: string[]` / `outcomes: string[]` shapes in `context/project-overview.md`, which require at least one entry per case study.

### Add another company
- Clicking "Add another company" appends a new company section to the form, using the same layout as the first (Company name input, one Challenges input, one Outcomes input, Add challenge / Add outcome buttons).
- Each new company section is numbered sequentially in its header (e.g. "Company 1", "Company 2", ...).
- There is no upper limit on the number of companies that can be added.

### Remove a company
- Each company section (beyond the first) has a way to remove that entire company section from the form — e.g. a trash icon in the company section header, consistent with the trash icon pattern used for challenges/outcomes.
- Removing a company removes its company name, all its challenges, and all its outcomes from form state.
- The first company section cannot be removed — at least one company must always remain in the form.
- Remaining company sections are renumbered sequentially after a removal (e.g. removing "Company 1" shifts "Company 2" up to "Company 1").

### Form state & validation (react-hook-form)
- The form is managed with `react-hook-form`, using a `useFieldArray` per company for challenges and a separate `useFieldArray` per company for outcomes, nested under a top-level `useFieldArray` for companies.
- Validation rules, enforced on submit:
  - Company name is required (non-empty, trimmed) for every company section.
  - Each challenge input is required (non-empty, trimmed).
  - Each outcome input is required (non-empty, trimmed).
- Validation errors are shown inline under the invalid field, matching the visual style already established for inputs on this page (border/background/text — reuse existing Tailwind patterns, don't introduce a new visual language).
- The "Add to knowledge base" button submits the form; if validation fails, submission is blocked and errors are shown — nothing is logged to console in that case.

### Submit behavior
- On successful validation, the form data is logged to the console in the shape of `CreateCaseStudiesDto` from `context/project-overview.md`:
  ```
  { caseStudies: [{ companyName, challenges, outcomes }, ...] }
  ```
- No API call is made. No loading state, no success/error UI, no navigation, and no form reset are part of this feature — the ⚠️ note in `project-overview.md` about ingest being a full, slow reindex is why the actual API call is deliberately excluded from this pass; wiring it up is a separate future feature.

## Non-goals

- No call to `POST /api/case-studies`.
- No changes to layout, spacing, colors, icons, or copy from the existing static markup, beyond adding the company-removal control described above.
- No persistence across page reloads/navigation.

## References

- @context/designs/add-case-studies-page.png
- @context/project-overview.md (data shapes: `CaseStudyDto`, `CreateCaseStudiesDto`)
- @context/features/app-ui-phase-1-spec.md
- Existing static markup: `client/src/pages/add-case-study-page.tsx`

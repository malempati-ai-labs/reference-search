# Current Feature: Logo Links to Homepage

## Status

In Progress

## Goals

- Clicking the logo in the header navigates to the home page (Search page, `/`)
- Works from any page in the app
- Uses client-side routing (React Router `Link`), no full page reload

## Notes

- Spec: `context/features/logo-links-to-homepage.md`
- User story: as a user, I want to click the logo to return to the home page, so I can get back to the start from anywhere.
- Existing static markup: `client/src/components/header.tsx`

## History

<!-- Keep this updated. Earliest to latest -->

- Project setup and boilerplate cleanup
- Implemented App UI Phase 1: shared header with nav, static Search page (default route), static Add case study page; pushed on `app-ui-phase-1`
- Implemented Add Case Study Interactivity: dynamic add/remove of challenges, outcomes, and company sections; react-hook-form validation; submit logs `CreateCaseStudiesDto`-shaped payload to console; pushed on `feature/add-case-study-interactivity`

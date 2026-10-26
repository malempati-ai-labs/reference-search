import { RotateCw, SearchX, TriangleAlert } from 'lucide-react';

import { ReferenceCard } from './components/reference-card';
import { ReferenceCardSkeleton } from './components/reference-card-skeleton';
import type { CustomerReference } from './types';

interface SearchResultsProps {
  status: 'pending' | 'success' | 'error';
  query: string;
  references: CustomerReference[];
  onRetry: () => void;
}

const QueryText = ({ query }: { query: string }) => (
  <span className="font-medium text-slate-900">“{query}”</span>
);

export const SearchResults = ({ status, query, references, onRetry }: SearchResultsProps) => (
  <section aria-live="polite" className="mx-auto mt-14 w-full max-w-5xl text-left">
    {status === 'pending' && (
      <>
        <h2 className="text-lg text-slate-500">
          Searching references for <QueryText query={query} />
        </h2>
        <p className="mt-1 text-sm text-slate-400">This can take a few seconds…</p>
        <div className="mt-5 space-y-5">
          <ReferenceCardSkeleton />
          <ReferenceCardSkeleton />
        </div>
      </>
    )}

    {status === 'success' && references.length > 0 && (
      <>
        <h2 className="text-lg text-slate-500">
          Top {references.length} references for <QueryText query={query} />
        </h2>
        <div className="mt-5 space-y-5">
          {references.map((reference, index) => (
            <ReferenceCard key={reference.companyName} reference={reference} rank={index + 1} />
          ))}
        </div>
      </>
    )}

    {status === 'success' && references.length === 0 && (
      <div className="flex flex-col items-center rounded-3xl border border-slate-200 bg-white px-6 py-12 text-center">
        <SearchX className="h-8 w-8 text-slate-400" />
        <h2 className="mt-4 text-lg font-semibold text-slate-900">No matching references found</h2>
        <p className="mt-1 text-slate-500">
          Nothing in the knowledge base matched <QueryText query={query} />. Try rephrasing the
          challenge.
        </p>
      </div>
    )}

    {status === 'error' && (
      <div
        role="alert"
        className="flex flex-col items-center rounded-3xl border border-red-200 bg-white px-6 py-12 text-center"
      >
        <TriangleAlert className="h-8 w-8 text-red-400" />
        <h2 className="mt-4 text-lg font-semibold text-slate-900">Something went wrong</h2>
        <p className="mt-1 text-slate-500">We couldn’t complete your search. Please try again.</p>
        <button
          type="button"
          onClick={onRetry}
          className="mt-5 flex items-center gap-2 rounded-full border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 transition-colors hover:border-slate-300 hover:bg-slate-50"
        >
          <RotateCw className="h-4 w-4" />
          Try again
        </button>
      </div>
    )}
  </section>
);

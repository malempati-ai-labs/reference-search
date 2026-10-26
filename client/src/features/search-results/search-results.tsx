import { ReferenceCard } from './components/reference-card';
import type { CustomerReference } from './types';

interface SearchResultsProps {
  query: string;
  references: CustomerReference[];
}

export const SearchResults = ({ query, references }: SearchResultsProps) => (
  <section className="mx-auto mt-14 w-full max-w-5xl text-left">
    <h2 className="text-lg text-slate-500">
      Top {references.length} references for{' '}
      <span className="font-medium text-slate-900">“{query}”</span>
    </h2>
    <div className="mt-5 space-y-5">
      {references.map((reference, index) => (
        <ReferenceCard key={reference.companyName} reference={reference} rank={index + 1} />
      ))}
    </div>
  </section>
);

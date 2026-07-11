import { ArrowRight, Search as SearchIcon, Sparkles } from 'lucide-react';

const SUGGESTIONS = [
  "We have a very large product catalog sprea...",
  'Need to onboard hundreds of partners onto ...',
  'Struggling with slow product discovery at ...',
];

export const SearchPage = () => {
  return (
    <div className="mx-auto flex max-w-3xl flex-col items-center px-6 pt-20 text-center">
      <span className="mb-6 inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-1.5 text-sm text-slate-600">
        <Sparkles className="h-4 w-4 text-blue-500" />
        Semantic reference matching
      </span>

      <h1 className="text-4xl font-bold leading-tight text-slate-900 sm:text-5xl">
        Which customer solved
        <br />
        a problem like this?
      </h1>

      <p className="mt-6 text-lg text-slate-500">
        Describe your prospect's challenge in plain language. We'll surface the closest matching
        customer case studies, ranked by relevance.
      </p>

      <div className="mt-10 flex w-full items-center gap-2 rounded-full border border-slate-200 bg-white p-2 shadow-sm">
        <SearchIcon className="ml-3 h-5 w-5 shrink-0 text-slate-400" />
        <input
          type="text"
          placeholder="Describe the prospect's challenge in plain language..."
          className="min-w-0 flex-1 border-none bg-transparent text-slate-700 placeholder:text-slate-400 focus:outline-none"
        />
        <button
          type="button"
          className="flex items-center gap-2 whitespace-nowrap rounded-full bg-blue-500 px-5 py-2.5 text-sm font-medium text-white transition-colors hover:bg-blue-600"
        >
          <ArrowRight className="h-4 w-4" />
          Search
        </button>
      </div>

      <div className="mt-4 flex flex-wrap items-center justify-center gap-2 text-sm text-slate-500">
        <span>Try:</span>
        {SUGGESTIONS.map((suggestion) => (
          <button
            key={suggestion}
            type="button"
            className="max-w-xs truncate rounded-full border border-slate-200 bg-white px-3 py-1.5 text-slate-600 transition-colors hover:border-slate-300"
          >
            {suggestion}
          </button>
        ))}
      </div>
    </div>
  );
};

import { useState } from 'react';

import { ArrowRight, Info, Loader2, Search as SearchIcon, Sparkles } from 'lucide-react';
import { useForm } from 'react-hook-form';

import { useCustomerReferences } from './hooks/use-customer-references';
import { SearchResults } from './search-results';

interface SearchFormValues {
  query: string;
}

const SUGGESTIONS = [
  'We have a very large product catalog spread across multiple countries and need to consolidate it',
  'Need to onboard hundreds of partners onto a single platform',
  'Struggling with slow product discovery at scale',
];

export const SearchReference = () => {
  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm<SearchFormValues>({ defaultValues: { query: '' } });
  const [searchedQuery, setSearchedQuery] = useState<string | null>(null);
  const { status, data, isFetching, isError, refetch } = useCustomerReferences(searchedQuery);

  const [notice, setNotice] = useState<string | null>(null);
  const [requestedQueries, setRequestedQueries] = useState<string[]>([]);

  const search = (query: string) => {
    const previous = requestedQueries.find((item) => item.toLowerCase() === query.toLowerCase());

    if (previous !== undefined && previous === searchedQuery) {
      if (isError) {
        setNotice(null);
        refetch();
      } else {
        setNotice('You’ve already searched for this. The results are shown below.');
      }
      return;
    }

    setNotice(null);
    if (previous === undefined) {
      setRequestedQueries((queries) => [...queries, query]);
    }
    setSearchedQuery(previous ?? query);
  };

  const onSubmit = ({ query }: SearchFormValues) => search(query.trim());

  const onSuggestionClick = (suggestion: string) => {
    if (isFetching) return;
    setValue('query', suggestion, { shouldValidate: true });
    search(suggestion);
  };

  return (
    <div className="px-6 pb-16 pt-20 text-center">
      <div className="mx-auto flex max-w-4xl flex-col items-center">
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

        <form onSubmit={handleSubmit(onSubmit)} noValidate className="mt-10 w-full">
          <div
            className={`flex w-full items-center gap-2 rounded-full border bg-white p-2 shadow-sm ${
              errors.query ? 'border-red-300' : 'border-slate-200'
            }`}
          >
            <SearchIcon className="ml-3 h-5 w-5 shrink-0 text-slate-400" />
            <input
              type="text"
              aria-label="Prospect challenge"
              aria-invalid={Boolean(errors.query)}
              placeholder="Describe the prospect's challenge in plain language..."
              className="min-w-0 flex-1 border-none bg-transparent text-slate-700 placeholder:text-slate-400 focus:outline-none"
              {...register('query', {
                validate: (value) =>
                  value.trim().length > 0 || 'Enter the prospect’s challenge to search',
              })}
            />
            <button
              type="submit"
              disabled={isFetching}
              className="flex items-center gap-2 whitespace-nowrap rounded-full bg-blue-500 px-5 py-2.5 text-sm font-medium text-white transition-colors hover:bg-blue-600 disabled:cursor-not-allowed disabled:opacity-60 disabled:hover:bg-blue-500"
            >
              {isFetching ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <ArrowRight className="h-4 w-4" />
              )}
              Search
            </button>
          </div>
          {errors.query && (
            <p role="alert" className="mt-2 text-sm text-red-500">
              {errors.query.message}
            </p>
          )}
          {notice && (
            <p
              role="status"
              className="mt-2 flex items-center justify-center gap-1.5 text-sm text-blue-600"
            >
              <Info className="h-4 w-4 shrink-0" />
              {notice}
            </p>
          )}
        </form>

        <div className="mt-4 flex flex-wrap items-center justify-center gap-2 text-sm text-slate-500">
          <span>Try:</span>
          {SUGGESTIONS.map((suggestion) => (
            <button
              key={suggestion}
              type="button"
              disabled={isFetching}
              onClick={() => onSuggestionClick(suggestion)}
              className="max-w-xs truncate rounded-full border border-slate-200 bg-white px-3 py-1.5 text-slate-600 transition-colors hover:border-slate-300 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {suggestion}
            </button>
          ))}
        </div>
      </div>

      {searchedQuery !== null && (
        <SearchResults
          status={status}
          query={searchedQuery}
          references={data ?? []}
          onRetry={() => search(searchedQuery)}
        />
      )}
    </div>
  );
};

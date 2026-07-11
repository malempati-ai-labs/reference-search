import { Building2, Info, Plus, Trash2 } from 'lucide-react';

export const AddCaseStudyPage = () => {
  return (
    <div className="mx-auto max-w-3xl px-6 py-16">
      <h1 className="text-4xl font-bold text-slate-900">Add case studies</h1>
      <p className="mt-4 text-lg text-slate-500">
        Grow the reference library. Add one or more companies with their challenges and outcomes
        — they'll be embedded and made searchable.
      </p>

      <div className="mt-8 flex items-start gap-3 rounded-xl border border-blue-100 bg-blue-50 px-5 py-4 text-sm text-blue-700">
        <Info className="mt-0.5 h-5 w-5 shrink-0" />
        <p>
          Submitting rebuilds the entire vector index server-side. This can take a while as the
          library grows — the form stays disabled until it's done. Duplicate company names are
          skipped automatically.
        </p>
      </div>

      <div className="mt-8 rounded-2xl border border-slate-200 bg-white p-6">
        <p className="text-sm font-medium text-slate-500">Company 1</p>

        <label className="mt-4 block text-sm font-medium text-slate-900">Company name</label>
        <div className="mt-2 flex items-center gap-2 rounded-xl border border-slate-200 px-4 py-3">
          <Building2 className="h-4 w-4 shrink-0 text-slate-400" />
          <input
            type="text"
            placeholder="e.g. SHOPcloud360"
            className="min-w-0 flex-1 border-none bg-transparent text-slate-700 placeholder:text-slate-400 focus:outline-none"
          />
        </div>

        <div className="mt-6 grid grid-cols-1 gap-6 sm:grid-cols-2">
          <div>
            <label className="block text-sm font-medium text-slate-900">Challenges</label>
            <div className="mt-2 flex items-center gap-2 rounded-xl border border-slate-200 px-4 py-3">
              <input
                type="text"
                placeholder="e.g. Managing a catalog of one million"
                className="min-w-0 flex-1 border-none bg-transparent text-slate-700 placeholder:text-slate-400 focus:outline-none"
              />
              <Trash2 className="h-4 w-4 shrink-0 text-slate-400" />
            </div>
            <button
              type="button"
              className="mt-3 flex items-center gap-1.5 text-sm font-medium text-blue-600 hover:text-blue-700"
            >
              <Plus className="h-4 w-4" />
              Add challenge
            </button>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-900">Outcomes</label>
            <div className="mt-2 flex items-center gap-2 rounded-xl border border-slate-200 px-4 py-3">
              <input
                type="text"
                placeholder="e.g. 350 online shops managed central"
                className="min-w-0 flex-1 border-none bg-transparent text-slate-700 placeholder:text-slate-400 focus:outline-none"
              />
              <Trash2 className="h-4 w-4 shrink-0 text-slate-400" />
            </div>
            <button
              type="button"
              className="mt-3 flex items-center gap-1.5 text-sm font-medium text-blue-600 hover:text-blue-700"
            >
              <Plus className="h-4 w-4" />
              Add outcome
            </button>
          </div>
        </div>
      </div>

      <button
        type="button"
        className="mt-6 flex w-full items-center justify-center gap-2 rounded-2xl border border-dashed border-slate-300 bg-white py-4 text-sm font-medium text-slate-500 transition-colors hover:border-slate-400"
      >
        <Plus className="h-4 w-4" />
        Add another company
      </button>

      <div className="mt-8 flex justify-end">
        <button
          type="button"
          className="flex items-center gap-2 rounded-full bg-blue-500 px-6 py-3 text-sm font-medium text-white transition-colors hover:bg-blue-600"
        >
          <Plus className="h-4 w-4" />
          Add to knowledge base
        </button>
      </div>
    </div>
  );
};

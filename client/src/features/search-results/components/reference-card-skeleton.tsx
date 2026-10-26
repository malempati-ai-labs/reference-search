export const ReferenceCardSkeleton = () => (
  <div className="animate-pulse rounded-3xl border border-slate-200 bg-white p-5 sm:p-8">
    <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between sm:gap-8">
      <div className="flex items-start gap-4">
        <div className="h-12 w-12 shrink-0 rounded-xl bg-slate-100" />
        <div className="space-y-3">
          <div className="h-5 w-40 rounded bg-slate-100" />
          <div className="h-5 w-28 rounded-full bg-slate-100" />
        </div>
      </div>
      <div className="h-8 w-full rounded bg-slate-100 sm:w-60" />
    </div>
    <div className="mt-5 space-y-2">
      <div className="h-4 w-full rounded bg-slate-100" />
      <div className="h-4 w-3/4 rounded bg-slate-100" />
    </div>
    <div className="mt-6 grid gap-4 md:grid-cols-2">
      <div className="h-28 rounded-2xl bg-slate-100" />
      <div className="h-28 rounded-2xl bg-slate-100" />
    </div>
  </div>
);

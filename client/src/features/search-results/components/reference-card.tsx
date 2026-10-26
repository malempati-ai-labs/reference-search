import { Building2, CircleCheck, Target } from 'lucide-react';

import type { CustomerReference } from '../types';

interface ReferenceCardProps {
  reference: CustomerReference;
  rank: number;
}

interface ConfidenceTier {
  label: string;
  badge: string;
  bar: string;
}

const getConfidenceTier = (score: number): ConfidenceTier => {
  if (score >= 85) {
    return {
      label: 'High confidence',
      badge: 'border-green-200 bg-green-50 text-green-600',
      bar: 'bg-green-500',
    };
  }
  if (score >= 70) {
    return {
      label: 'Good match',
      badge: 'border-blue-200 bg-blue-50 text-blue-600',
      bar: 'bg-blue-600',
    };
  }
  return {
    label: 'Possible match',
    badge: 'border-amber-200 bg-amber-50 text-amber-600',
    bar: 'bg-amber-500',
  };
};

export const ReferenceCard = ({ reference, rank }: ReferenceCardProps) => {
  const { companyName, reason, relevantChallenges, relevantOutcomes, confidenceScore } = reference;
  const tier = getConfidenceTier(confidenceScore);

  return (
    <article className="rounded-3xl border border-slate-200 bg-white p-5 text-left shadow-sm transition-shadow hover:shadow-md sm:p-8">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between sm:gap-8">
        <div className="flex items-start gap-4">
          <span className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-slate-100 font-medium text-slate-700">
            {rank}
          </span>
          <div className="min-w-0">
            <h3 className="flex items-center gap-2 text-xl font-semibold text-slate-900">
              <Building2 className="h-4 w-4 shrink-0 text-slate-500" />
              <span className="truncate">{companyName}</span>
            </h3>
            <span
              className={`mt-2 inline-block rounded-full border px-2.5 py-0.5 text-sm ${tier.badge}`}
            >
              {tier.label}
            </span>
          </div>
        </div>

        <div className="w-full sm:w-60">
          <div className="flex items-baseline justify-between text-sm text-slate-500">
            <span>Confidence</span>
            <span className="text-base font-semibold text-slate-900">
              {confidenceScore}
              <span className="font-medium">/100</span>
            </span>
          </div>
          <div
            role="progressbar"
            aria-label="Confidence"
            aria-valuenow={confidenceScore}
            aria-valuemin={0}
            aria-valuemax={100}
            className="mt-1.5 h-1.5 overflow-hidden rounded-full bg-slate-100"
          >
            <div
              className={`h-full rounded-full ${tier.bar}`}
              style={{ width: `${confidenceScore}%` }}
            />
          </div>
        </div>
      </div>

      <p className="mt-5 text-lg leading-relaxed text-slate-500">{reason}</p>

      <div className="mt-6 grid gap-4 md:grid-cols-2">
        <section className="rounded-2xl border border-slate-200 p-5">
          <h4 className="flex items-center gap-2 text-sm font-medium uppercase tracking-wide text-slate-500">
            <Target className="h-4 w-4" />
            Relevant challenges
          </h4>
          <ul className="mt-3 space-y-2 text-slate-900">
            {relevantChallenges.map((challenge) => (
              <li key={challenge}>{challenge}</li>
            ))}
          </ul>
        </section>

        <section className="rounded-2xl border border-slate-200 p-5">
          <h4 className="flex items-center gap-2 text-sm font-medium uppercase tracking-wide text-slate-500">
            <CircleCheck className="h-4 w-4" />
            Relevant outcomes
          </h4>
          <ul className="mt-3 space-y-2 text-slate-900">
            {relevantOutcomes.map((outcome) => (
              <li key={outcome} className="flex items-start gap-2">
                <CircleCheck className="mt-1 h-4 w-4 shrink-0 text-green-500" />
                {outcome}
              </li>
            ))}
          </ul>
        </section>
      </div>
    </article>
  );
};

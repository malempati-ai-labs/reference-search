import type { CustomerReferencesResponse } from './types';

export const DUMMY_QUERY =
  'We have a very large product catalog spread across multiple countries and need to consolidate it';

export const DUMMY_RESPONSE: CustomerReferencesResponse = {
  data: [
    {
      companyName: 'SHOPcloud360',
      reason:
        'Operates a multi-tenant commerce platform serving roughly one million products across hundreds of merchants — a very close structural match to a large, multi-country catalog.',
      relevantChallenges: [
        'Managing a catalog of one million products',
        'Onboarding hundreds of merchants onto a single platform',
      ],
      relevantOutcomes: [
        '350 online shops managed centrally',
        '1M products served from a single backend',
      ],
      confidenceScore: 92,
    },
    {
      companyName: 'Meridian Retail Group',
      reason:
        'Consolidated regional product catalogs from several countries into one unified source of truth, closely mirroring the prospect’s multi-country consolidation need.',
      relevantChallenges: [
        'Fragmented product data across regional storefronts',
        'Inconsistent pricing and availability between countries',
      ],
      relevantOutcomes: [
        'Unified catalog across 8 countries',
        'Catalog update time reduced by 60%',
      ],
      confidenceScore: 81,
    },
    {
      companyName: 'Nordic Commerce Hub',
      reason:
        'Handles a growing catalog for marketplace sellers, with some overlap in scale and localization challenges, though less focus on cross-border consolidation.',
      relevantChallenges: ['Scaling product search for a growing seller base'],
      relevantOutcomes: ['Search latency cut to under 200ms'],
      confidenceScore: 64,
    },
  ],
};

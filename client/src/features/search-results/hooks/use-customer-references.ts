import { useQuery } from '@tanstack/react-query';

import { getCustomerReferences } from '../../../lib/api/customer-references';

const STALE_TIME_MS = 10 * 60 * 1000;

export const useCustomerReferences = (query: string | null) =>
  useQuery({
    queryKey: ['customer-references', query],
    queryFn: () => getCustomerReferences(query ?? ''),
    enabled: query !== null,
    staleTime: STALE_TIME_MS,
    retry: false,
  });

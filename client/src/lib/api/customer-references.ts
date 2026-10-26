import type {
  CustomerReference,
  CustomerReferencesResponse,
} from '../../features/search-results/types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000';

export const getCustomerReferences = async (query: string): Promise<CustomerReference[]> => {
  const response = await fetch(
    `${API_BASE_URL}/api/customer-references?search=${encodeURIComponent(query)}`,
  );

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  const body: CustomerReferencesResponse = await response.json();
  return body.data ?? [];
};

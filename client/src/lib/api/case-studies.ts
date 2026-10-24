import type {
  CreateCaseStudiesPayload,
  CreateCaseStudiesResponse,
} from '../../features/add-case-study/types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000';

export const createCaseStudies = async (
  payload: CreateCaseStudiesPayload,
): Promise<CreateCaseStudiesResponse> => {
  const response = await fetch(`${API_BASE_URL}/api/case-studies`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(body?.message ?? `Request failed with status ${response.status}`);
  }

  return response.json();
};

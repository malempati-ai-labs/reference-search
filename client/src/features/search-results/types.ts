export interface CustomerReference {
  companyName: string;
  reason: string;
  relevantChallenges: string[];
  relevantOutcomes: string[];
  confidenceScore: number;
}

export interface CustomerReferencesResponse {
  data: CustomerReference[];
}

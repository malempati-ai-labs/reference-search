export interface CaseStudy {
  companyName: string;
  challenges: string[];
  outcomes: string[];
}

export interface CreateCaseStudiesPayload {
  caseStudies: CaseStudy[];
}

export interface CreateCaseStudiesResponse {
  message: string;
}

export interface CaseStudyFormValues {
  companies: {
    companyName: string;
    challenges: { value: string }[];
    outcomes: { value: string }[];
  }[];
}

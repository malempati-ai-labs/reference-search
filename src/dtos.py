from pydantic import BaseModel

class CaseStudyDto(BaseModel):
    companyName: str
    challenges: list[str]
    outcomes: list[str]

class CreateCaseStudiesDto(BaseModel):
    caseStudies: list[CaseStudyDto]


class CustomerReference(BaseModel):
    companyName: str
    reason: str
    relevantChallenges: list[str]
    relevantOutcomes: list[str]
    confidenceScore: int


class CustomerReferences(BaseModel):
    customerReferences: list[CustomerReference]
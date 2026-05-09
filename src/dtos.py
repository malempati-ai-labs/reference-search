from pydantic import BaseModel

class CaseStudyDto(BaseModel):
    companyName: str
    challenges: list[str]
    keyMetrics: list[str]

class CreateCaseStudiesDto(BaseModel):
    caseStudies: list[CaseStudyDto]

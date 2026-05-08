from pydantic import BaseModel

class CreateCaseStudyDto(BaseModel):
    companyName: str
    challenges: list[str]
    keyMetrics: list[str]

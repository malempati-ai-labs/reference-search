from fastapi import FastAPI, status
from src.dtos import CreateCaseStudyDto
import aiofiles

app = FastAPI()


async def append_company_data(data: CreateCaseStudyDto):
    formatted_text = f"## Company Name: {data.companyName}\n\n"

    formatted_text += "Challenges:\n"
    for index, challenge in enumerate(data.challenges, start=1):
        formatted_text += f"   {index}. {challenge}\n"

    formatted_text += "\nKey Metrics:\n"
    for metric in data.keyMetrics:
        formatted_text += f"   - {metric}\n"

    formatted_text += "\n\n"

    # Append asynchronously
    async with aiofiles.open('case-studies.txt', mode="a", encoding="utf-8") as file:
        await file.write(formatted_text)

@app.get("/root")
def root():
    return {"message": "I am running!"}


@app.post("/case-studies", status_code=status.HTTP_201_CREATED)
async def create_case_studies(createCaseStudyDto: CreateCaseStudyDto):
    await append_company_data(createCaseStudyDto)

    return {
        "message": "Company data added successfully"
    }

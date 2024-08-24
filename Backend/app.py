import json
import os
from fastapi import FastAPI, Path, File, UploadFile, Response, status

from github import Github
from github import Auth

from fastapi.middleware.cors import CORSMiddleware

from pdfx import PDFx
from utils import clear_directory, get_github_username
from chains import resume_analysis_chain, project_analysis_chain

from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Resume Analysis API",
    description="Resume analysis Api for feedback and github analysis",
    version="1.0.0",
)

# allow cors for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Hello! Welcome to the API"}


# To accept the body of the request we need to set the type of the controller function
# parameter to a class that inherits from BaseModel
@app.post("/resume")
async def resume_feedback(resume: UploadFile, response: Response):
    # Create a unique filename
    filename = f"{resume.filename}_{os.urandom(10).hex()}.pdf"

    content = await resume.read()

    os.makedirs("./uploads", exist_ok=True)
    with open(f"./uploads/{filename}", "wb") as buffer:
        buffer.write(content)

    pdf = PDFx(f"./uploads/{filename}")
    resume_text = pdf.get_text()

    if resume_text == "":
        response.status_code == status.HTTP_400_BAD_REQUEST
        return {"message": "Invalid resume file"}

    links = pdf.get_references_as_dict()["url"]

    print("Printing the links of the pdf", links)

    github_profile = get_github_username(links)

    resume_analysis_response = resume_analysis_chain.invoke(
        {"resume_text": str(resume_text)}
    )
    project_analysis_response = project_analysis_chain.invoke(
        {"resume_text": str(resume_text)}
    )

    clear_directory("./uploads")

    return {
        "filename": resume.filename,
        "resume_feedback": resume_analysis_response.model_dump(),
        "project_feedback": project_analysis_response.model_dump(),
        "github_profile": github_profile,
    }


@app.get("/github/{username}")
async def github_analysis(username: str):
    auth = Auth.Token(os.environ["GITHUB_ACCESS_TOKEN"])
    github = Github(auth=auth)
    user = github.get_user(username)

    languages_used = {}
    max_count = 0
    max_repo = ""
    for repo in user.get_repos():
        if repo.stargazers_count + repo.forks_count > max_count:
            max_count = repo.stargazers_count + repo.forks_count
            max_repo = repo.name
        languages = repo.get_languages()
        if languages:
            language = max(languages, key=languages.get)
            if language in languages_used:
                languages_used[language] += 1
            else:
                languages_used[language] = 1

    languages_used = dict(
        sorted(languages_used.items(), key=lambda x: x[1], reverse=True)
    )

    if max_count == 0:
        max_repo = ""

    return {"BestRepo": max_repo, "languages_used": languages_used}

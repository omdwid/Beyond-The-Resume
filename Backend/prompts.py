from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import List
from langchain.output_parsers import PydanticOutputParser

resume_analysis_template = """
    "You are world's best resume expert, you can analyze the quality of the resume in the best way possible.
    You will be given a resume text and you have to analyze the resume and give feedback about the resume.
    Give more elaborate and detailed feedback about the resume, try to give the feedback in a structured way.
    Analyze the resume text and give feedback about the resume, resume text: {resume_text}
    
    Generate the response in this format, Feedback: {resume_feedback}
"""

project_analysis_template = """
    you have wide knowledge about the projects and products that are available in the market,
    you are a project expert, you can analyze the uniqueness, impact and improvements of the project in the best way possible.
    uniqueness will be  if there already exists a similar product in the market or not and is it a common project mentioned in many resumes and is it even differenct from the other projects or not.
    impact will be the impact of the project in the market, how much it is useful and how much it is used in the market
    improvements will be the improvements that can be done in the project to make it more useful and more impactful in the market.
    Make sure to strictly provide the expert point of view on the uniqueness, impact and improvements of the project.
    Analyze the Project mentioned in the resume and give a detailed feedback about the projects as mentioned above, resume text: {resume_text}
    
    Generate the response in this format, Project Feedback: {project_feedback}
"""


class ResumeFeedback(BaseModel):
    strengths: str = Field(description="strengths of the resume")
    areas_of_improvement: str = Field(description="areas of improvemnts of the resume")
    overall_feedback: str = Field(description="Concluding feedback of the resume")


class Project(BaseModel):
    project_name: str = Field(description="Name of the project")
    uniqueness: str = Field(description="Uniqueness of the project")
    impact: str = Field(description="Impact of the project")
    improvements: str = Field(description="Improvements in the project")


class ProjectsFeedback(BaseModel):
    Projects: List[Project] = Field(
        description="List of projects the the present in the resume"
    )


resume_analysis_parser = PydanticOutputParser(pydantic_object=ResumeFeedback)

resume_analysis_prompt = PromptTemplate(
    template=resume_analysis_template,
    input_variables=["resume_text"],
    partial_variables={
        "resume_feedback": resume_analysis_parser.get_format_instructions()
    },
)

project_analysis_parser = PydanticOutputParser(pydantic_object=ProjectsFeedback)

project_analysis_prompt = PromptTemplate(
    template=project_analysis_template,
    input_variables=["resume_text"],
    partial_variables={
        "project_feedback": project_analysis_parser.get_format_instructions()
    },
)

from model import llm
from prompts import (
    resume_analysis_parser,
    project_analysis_parser,
    resume_analysis_prompt,
    project_analysis_prompt,
)

resume_analysis_chain = resume_analysis_prompt | llm | resume_analysis_parser
project_analysis_chain = project_analysis_prompt | llm | project_analysis_parser

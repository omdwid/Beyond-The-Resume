from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
import os
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import pdfx
from langchain.chains.sequential import SimpleSequentialChain
from dotenv import load_dotenv
from github import Github
from github import Auth
import markdown
import textwrap
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

def to_markdown(text):
  text = text.replace('•', '  *')
  return markdown.markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

google_api_key = os.environ['GEMINI_API_KEY']


auth = Auth.Token(os.environ['GITHUB_ACCESS_TOKEN'])
github = Github(auth=auth)

print(github.get_user().login)

llm = ChatGoogleGenerativeAI(google_api_key=google_api_key, model="gemini-pro")


pdf = pdfx.PDFx('./om_resume.pdf')
resume_text = pdf.get_text()

links = pdf.get_references_as_dict()['url']

# def get_github_username(links):  
#   for link in links:
#     if 'https://github.com' in link:
#       if link[-1] == '/':
#         return link.split[-2]
#       return link.split[-1]
    
#   return ''
    
# username = get_github_username(links)
# print(username)
    
prompt1 = PromptTemplate.from_template('Analyze the resume text and give feedback about the resume, resume text: {resume_text}')
prompt2 = PromptTemplate.from_template('Analyze the resume text and Give the tech stack of each of the projects made by the candidate, resume text: {resume_text}')

text_chain1 = LLMChain(llm=llm, prompt=prompt1, verbose=True, output_key = 'resume_summary')
text_chain2 = LLMChain(llm=llm, prompt=prompt2, verbose=True, output_key = 'tech_stack')

response = text_chain1.invoke(resume_text)
response2 = text_chain2.invoke(resume_text)

print(list(response.keys()))

print(response['resume_summary'])
print("-------------------------------------------------------------------------------------------------------")
print(response2['tech_stack'])

# celeb_name = input("enter the name of the celebrity:- ")

# response = text_chain.invoke(input=celeb_name)

# print(response['dob'])

# # llm = ChatGoogleGenerativeAI(model="gemini-pro")
# # result = llm.invoke("Write a ballad about LangChain")
# # print(result.content)
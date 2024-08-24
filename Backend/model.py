import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

google_api_key = os.environ["GEMINI_API_KEY"]
llm = ChatGoogleGenerativeAI(
    google_api_key=google_api_key, model="gemini-pro", temperature=0.3
)

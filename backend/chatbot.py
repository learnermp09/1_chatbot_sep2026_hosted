# important libraries
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR/".env")

# Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are very good AI assitant. Please respond to the user input"),
    ("user", "question :{question}"),
])

# LLM
llm = ChatGroq(model = "openai/gpt-oss-120b", temperature = 0)

# Output
output_parser = StrOutputParser()


chain  = prompt | llm | output_parser

def get_response(question:str) -> str:
    response =  chain.invoke({"question" : question})
    return response

# if __name__ == "__main__":
#     get_response("Who is PM of India")




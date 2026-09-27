from fastapi import FastAPI
from pydantic import BaseModel

from chatbot import get_response

app = FastAPI(title = "LLM Chatbot API",
              version = "1.1.0"
              )

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.get("/")
def home():
    return {"message": "LLM chatbot API is running"}


@app.get("/health")
def health():
    return {"message": "Healthy"}

@app.post("/chat", response_model = ChatResponse)
def chat(request: ChatRequest):
    answer = get_response(request.message)
    return {"response" : answer}
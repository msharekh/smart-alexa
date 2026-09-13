import os

from dotenv import load_dotenv
from fastapi import FastAPI
from openai import OpenAI

load_dotenv()

app = FastAPI()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


@app.get("/")
def home():
    return {"status": "Moaen is running"}


@app.get("/ask")
def ask(question: str):
    response = client.responses.create(
        model="gpt-5",
        instructions="أجب بالعربية بشكل مختصر وواضح.",
        input=question
    )

    return {
        "question": question,
        "answer": response.output_text
    }
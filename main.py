#!/bin/python3

from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel
import uvicorn
import os

# Read OpenAI API key from Kubernetes secret env variable
api_key = os.environ["OPENAI_API"]

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Create FastAPI app
app = FastAPI()

# Request body schema
class Body(BaseModel):
    text: str

# Root endpoint
@app.get("/")
def welcome():
    return {"message": "Welcome to ChatGPT AI Application V2"}

# Home endpoint
@app.get("/home")
def home():
    return {"message": "welcome home"}

# Dummy test endpoint
@app.post("/dummy")
def demo_function(data: dict):
    return {"message": data}

# GPT response endpoint
@app.post("/response")
def generate(body: Body):

    prompt = body.text

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response.choices[0].message.content

    return {"response": answer}

# Run FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
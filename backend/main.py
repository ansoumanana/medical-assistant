from fastapi import FastAPI
from pydantic import BaseModel
import faiss
import pickle
import numpy as np
import requests
import os
from sentence_transformers import SentenceTransformer

app = FastAPI()

class Query(BaseModel):
    question: str

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Your OpenRouter API key (set this as a Cloud Run env variable or GitHub Secret)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def query_mistral(prompt: str) -> str:
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        json={
            "model": "mistral",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        },
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        timeout=60
    )
    return response.json()["choices"][0]["message"]["content"]

@app.post("/ask")
async def ask_question(query: Query):
    index = faiss.read_index("medical_index.faiss")
    with open("medical_docs.pkl", "rb") as f:
        chunks = pickle.load(f)

    q_embedding = model.encode([query.question])
    D, I = index.search(np.array(q_embedding), k=3)
    context = "\n\n".join(chunks[i].page_content for i in I[0])

    prompt = f"""Réponds à la question en t'appuyant uniquement sur le contexte suivant :

{context}

Question : {query.question}
Réponse :"""
    answer = query_mistral(prompt)
    return {"answer": answer}

from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

app = FastAPI()

class Query(BaseModel):
    question: str

model = SentenceTransformer("all-MiniLM-L6-v2")

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

    response = subprocess.run([
        "ollama", "run", "mistral"
    ], input=prompt.encode(), capture_output=True)
    answer = response.stdout.decode()
    return {"answer": answer}

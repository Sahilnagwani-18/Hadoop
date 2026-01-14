from fastapi import FastAPI
from pydantic import BaseModel
import json
import numpy as np
import re

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load model
with open("lr_model_export.json", "r") as f:
    model = json.load(f)

coef = np.array(model["coefficient_matrix"])
intercepts = np.array(model["intercepts"])
labels = model["labels"]
num_features = model["num_features"]

def hashing_tf(tokens, num_features=2000):
    vec = np.zeros(num_features)
    for token in tokens:
        h = hash(token) % num_features
        vec[h] += 1
    return vec

def preprocess_title(title):
    title = title.lower()
    title = re.sub(r"[^a-z0-9 ]", " ", title)
    return title.split()

def softmax(z):
    e = np.exp(z - np.max(z))
    return e / e.sum()

def predict(title):
    tokens = preprocess_title(title)
    features = hashing_tf(tokens, num_features)
    logits = coef.dot(features) + intercepts
    probs = softmax(logits)
    return labels[int(np.argmax(probs))]

class MovieInput(BaseModel):
    title: str

@app.post("/predict")
def predict_genre(data: MovieInput):
    predicted = predict(data.title)
    return {"title": data.title, "predicted_genre": predicted}


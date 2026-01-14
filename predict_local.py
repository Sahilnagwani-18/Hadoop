import json
import numpy as np
import re

# -------------------------------
# Load exported model parameters
# -------------------------------
with open("lr_model_export.json", "r") as f:
    model = json.load(f)

coef = np.array(model["coefficient_matrix"])      # shape (20, 2000)
intercepts = np.array(model["intercepts"])        # shape (20,)
labels = model["labels"]
num_features = model["num_features"]

# -------------------------------
# Hashing Trick (same as Spark)
# -------------------------------
def hashing_tf(tokens, num_features=2000):
    vec = np.zeros(num_features)
    for token in tokens:
        h = hash(token) % num_features
        vec[h] += 1
    return vec

# -------------------------------
# Preprocess Movie Title
# -------------------------------
def preprocess_title(title):
    title = title.lower()
    title = re.sub(r"[^a-z0-9 ]", " ", title)
    words = title.split()
    return words

# -------------------------------
# Softmax for multiclass LR
# -------------------------------
def softmax(z):
    e = np.exp(z - np.max(z))
    return e / e.sum()

# -------------------------------
# Predict Genre
# -------------------------------
def predict_genre(title):
    tokens = preprocess_title(title)
    features = hashing_tf(tokens, num_features)
    logits = coef.dot(features) + intercepts
    probs = softmax(logits)
    pred_idx = np.argmax(probs)
    return labels[pred_idx], float(probs[pred_idx])

# -------------------------------
# Example
# -------------------------------
if __name__ == "__main__":
    title = input("Enter movie title: ")
    genre, confidence = predict_genre(title)
    print("Predicted Genre:", genre)
    print("Confidence:", confidence)



import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib
import os

os.makedirs("model", exist_ok=True)

# Load data
df = pd.read_csv("data/samples/intent_training_data.csv")

# Combine fields as input text
X = (df["user_agent"] + " " + df["description"]).values
y = df["label"].values

# Build classifier pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression(max_iter=500))
])

# Train
model.fit(X, y)

# Save
joblib.dump(model, "model/intent_classifier.joblib")
print("[+] Model saved to model/intent_classifier.joblib")

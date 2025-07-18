import joblib
import os

# Load the trained ML model (TfidfVectorizer + LogisticRegression pipeline)
model_path = os.path.join(os.path.dirname(__file__), "intent_classifier.joblib")

try:
    classifier = joblib.load(model_path)
except Exception as e:
    # Fallback if model fails to load (e.g., cold start or packaging issue)
    print(f"[ERROR] Failed to load intent classifier model: {e}")
    classifier = None

def classify_intent(log_entry):
    """
    Accepts a parsed deception log and returns predicted attacker intent.
    """

    if classifier is None:
        return "unknown"

    ua = log_entry.get("request_metadata", {}).get("user_agent", "")
    desc = log_entry.get("description", "")
    text = f"{ua} {desc}".strip()

    try:
        prediction = classifier.predict([text])[0]
        return prediction
    except Exception as e:
        print(f"[ERROR] Prediction failed: {e}")
        return "unknown"

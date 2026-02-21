import joblib
import os

# 1. Locate and load the saved model
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, "stress_model.joblib")

try:
    # Load the model into memory
    stress_classifier = joblib.load(model_path)
    print("✅ AI Stress Model loaded successfully.")
except FileNotFoundError:
    stress_classifier = None
    print("⚠️ Warning: stress_model.joblib not found. Run train.py first.")

def predict_stress_level(text: str) -> int:
    """
    Takes user text, feeds it to the ML pipeline, and returns a stress score (1-10).
    """
    if not stress_classifier:
        return 5 # Fallback average score if the model fails to load
        
    # The model expects a list of strings, even if it's just one string
    prediction = stress_classifier.predict([text])
    
    return int(prediction[0])
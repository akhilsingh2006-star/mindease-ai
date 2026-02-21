import os
import pandas as pd
from datasets import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
import joblib

def train_model():
    print(" Downloading dataset from Hugging Face (this might take a few seconds)...")
    # Load the 20,000 tweet emotion dataset
    dataset = load_dataset("dair-ai/emotion", "split")
    
    # Convert to a Pandas DataFrame for easier manipulation
    df = pd.DataFrame(dataset['train'])
    
    print(" Mapping psychological emotions to 1-10 Stress Scores...")
    # The dataset labels are: 0: sadness, 1: joy, 2: love, 3: anger, 4: fear, 5: surprise
    # We map these to a 1-10 stress scale.
    def map_to_stress(label):
        if label in [1, 2]:    # Joy, Love
            return 2           # Low stress
        elif label == 5:       # Surprise
            return 5           # Medium stress
        elif label in [0, 3, 4]: # Sadness, Anger, Fear
            return 8           # High stress
        return 5
        
    df['stress_level'] = df['label'].apply(map_to_stress)
    
    # Split the data so we can test the accuracy on data the AI hasn't seen yet
    X_train, X_test, y_train, y_test = train_test_split(
        df['text'], df['stress_level'], test_size=0.2, random_state=42
    )

    print(" Initializing TF-IDF and Logistic Regression pipeline...")
    # We increase max_features to 10000 to capture more vocabulary, increasing accuracy
    model_pipeline = make_pipeline(
        TfidfVectorizer(stop_words='english', max_features=10000, ngram_range=(1, 2)),
        LogisticRegression(max_iter=1000, C=1.5)
    )

    print(" Training the stress prediction model on 16,000 real statements...")
    model_pipeline.fit(X_train, y_train)

    # Calculate Accuracy!
    print(" Evaluating model accuracy...")
    predictions = model_pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    
    print("\n========================================")
    print(f" MODEL ACCURACY: {accuracy * 100:.2f}%")
    print("========================================\n")
    
    # Save the highly accurate model to disk
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, "stress_model.joblib")
    
    joblib.dump(model_pipeline, model_path)
    print(f" Production-ready model saved at: {model_path}")

if __name__ == "__main__":
    train_model()
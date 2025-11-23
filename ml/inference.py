"""
ML Model Inference Script
Loads trained model and performs batch inference on new data.
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from datetime import datetime

# Configuration
MODEL_DIR = Path(__file__).parent / "models"
MODEL_NAME = "phishing_detection_model_latest.pkl"

def load_model():
    """Load the latest trained model."""
    model_path = MODEL_DIR / MODEL_NAME
    
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found: {model_path}. Run train.py first.")
    
    model = joblib.load(model_path)
    print(f"Loaded model from: {model_path}")
    return model

def prepare_features(df):
    """Prepare features for inference (same as training)."""
    # Exclude id and target if present
    exclude_cols = ['id', 'CLASS_LABEL']
    feature_cols = [col for col in df.columns if col not in exclude_cols]
    
    X = df[feature_cols].copy()
    
    # Handle missing values
    X = X.fillna(0)
    X = X.replace(-1, 0)
    
    return X, feature_cols

def predict(model, X):
    """Make predictions."""
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)
    
    return predictions, probabilities

def batch_inference(input_file, output_file=None):
    """Perform batch inference on a CSV file."""
    print(f"Loading data from: {input_file}")
    df = pd.read_csv(input_file)
    print(f"Loaded {len(df)} records")
    
    # Load model
    model = load_model()
    
    # Prepare features
    X, feature_cols = prepare_features(df)
    
    # Make predictions
    print("Making predictions...")
    predictions, probabilities = predict(model, X)
    
    # Add predictions to dataframe
    df['predicted_class'] = predictions
    df['prediction_probability'] = probabilities[:, 1]  # Probability of phishing
    df['prediction_confidence'] = np.max(probabilities, axis=1)
    
    # Save results
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = Path(__file__).parent / "predictions" / f"predictions_{timestamp}.csv"
        output_file.parent.mkdir(exist_ok=True)
    
    df.to_csv(output_file, index=False)
    print(f"\nPredictions saved to: {output_file}")
    
    # Summary statistics
    print(f"\nPrediction Summary:")
    print(f"  Total records: {len(df)}")
    print(f"  Predicted phishing: {sum(predictions == 1)}")
    print(f"  Predicted legitimate: {sum(predictions == 0)}")
    print(f"  Average confidence: {df['prediction_confidence'].mean():.4f}")
    
    return df

def predict_single_record(features_dict):
    """Predict for a single record (for API use)."""
    model = load_model()
    
    # Convert to DataFrame
    df = pd.DataFrame([features_dict])
    
    # Prepare features
    X, _ = prepare_features(df)
    
    # Make prediction
    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0]
    
    return {
        'predicted_class': int(prediction),
        'is_phishing': bool(prediction == 1),
        'phishing_probability': float(probability[1]),
        'legitimate_probability': float(probability[0]),
        'confidence': float(np.max(probability))
    }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python inference.py <input_csv> [output_csv]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    batch_inference(input_file, output_file)


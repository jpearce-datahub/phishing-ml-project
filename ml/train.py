"""
ML Model Training Script
Trains a phishing detection model using the dataset features.
Supports both local training and SageMaker training.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
import joblib
import os
from pathlib import Path
import boto3
from datetime import datetime

# Configuration
MODEL_DIR = Path(__file__).parent / "models"
MODEL_DIR.mkdir(exist_ok=True)
S3_MODEL_BUCKET = "org-product-logs-ml-models"
MODEL_NAME = "phishing_detection_model"

def load_data():
    """Load the phishing dataset."""
    data_path = Path(__file__).parent.parent / "Phishing_Legitimate_full.csv"
    df = pd.read_csv(data_path)
    return df

def prepare_features(df):
    """Prepare features for model training."""
    # Exclude id and target
    feature_cols = [col for col in df.columns if col not in ['id', 'CLASS_LABEL']]
    
    X = df[feature_cols].copy()
    y = df['CLASS_LABEL'].copy()
    
    # Handle any missing values
    X = X.fillna(0)
    
    # Replace -1 values (likely missing indicators) with 0
    X = X.replace(-1, 0)
    
    return X, y, feature_cols

def train_model(X_train, y_train, X_val, y_val):
    """Train Random Forest model."""
    print("Training Random Forest model...")
    
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate on validation set
    y_pred = model.predict(X_val)
    
    accuracy = accuracy_score(y_val, y_pred)
    precision = precision_score(y_val, y_pred)
    recall = recall_score(y_val, y_pred)
    f1 = f1_score(y_val, y_pred)
    
    print(f"\nValidation Metrics:")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")
    
    return model, {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1
    }

def get_feature_importance(model, feature_names, top_n=20):
    """Get top N most important features."""
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:top_n]
    
    feature_importance = []
    for i in indices:
        feature_importance.append({
            'feature': feature_names[i],
            'importance': float(importances[i])
        })
    
    return feature_importance

def save_model(model, metrics, feature_names, feature_importance):
    """Save model and metadata."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save model
    model_path = MODEL_DIR / f"{MODEL_NAME}_{timestamp}.pkl"
    joblib.dump(model, model_path)
    print(f"\nModel saved to: {model_path}")
    
    # Save latest model (for easy access)
    latest_path = MODEL_DIR / f"{MODEL_NAME}_latest.pkl"
    joblib.dump(model, latest_path)
    
    # Save metadata
    metadata = {
        'timestamp': timestamp,
        'model_name': MODEL_NAME,
        'metrics': metrics,
        'feature_count': len(feature_names),
        'top_features': feature_importance
    }
    
    import json
    metadata_path = MODEL_DIR / f"{MODEL_NAME}_{timestamp}_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    return model_path, metadata_path

def upload_to_s3(model_path, metadata_path):
    """Upload model to S3 (optional, for SageMaker)."""
    try:
        s3_client = boto3.client('s3')
        
        model_key = f"models/{model_path.name}"
        metadata_key = f"models/{metadata_path.name}"
        
        s3_client.upload_file(str(model_path), S3_MODEL_BUCKET, model_key)
        s3_client.upload_file(str(metadata_path), S3_MODEL_BUCKET, metadata_key)
        
        print(f"\nModel uploaded to S3:")
        print(f"  s3://{S3_MODEL_BUCKET}/{model_key}")
        print(f"  s3://{S3_MODEL_BUCKET}/{metadata_key}")
        
    except Exception as e:
        print(f"\nWarning: Could not upload to S3: {e}")
        print("Continuing with local model only...")

def main():
    """Main training function."""
    print("Loading data...")
    df = load_data()
    print(f"Loaded {len(df)} records")
    
    print("\nPreparing features...")
    X, y, feature_names = prepare_features(df)
    print(f"Features: {len(feature_names)}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.2, random_state=42, stratify=y_train
    )
    
    print(f"\nData splits:")
    print(f"  Train: {len(X_train)}")
    print(f"  Validation: {len(X_val)}")
    print(f"  Test: {len(X_test)}")
    
    # Train model
    model, metrics = train_model(X_train, y_train, X_val, y_val)
    
    # Get feature importance
    print("\nCalculating feature importance...")
    feature_importance = get_feature_importance(model, feature_names)
    print("\nTop 10 Features:")
    for i, feat in enumerate(feature_importance[:10], 1):
        print(f"  {i}. {feat['feature']}: {feat['importance']:.4f}")
    
    # Final test evaluation
    print("\nEvaluating on test set...")
    y_test_pred = model.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_test_pred)
    test_f1 = f1_score(y_test, y_test_pred)
    print(f"Test Accuracy: {test_accuracy:.4f}")
    print(f"Test F1 Score: {test_f1:.4f}")
    
    # Save model
    model_path, metadata_path = save_model(model, metrics, feature_names, feature_importance)
    
    # Upload to S3 (optional)
    upload_to_s3(model_path, metadata_path)
    
    print("\nTraining complete!")

if __name__ == "__main__":
    main()


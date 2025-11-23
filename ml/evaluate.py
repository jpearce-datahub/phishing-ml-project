"""
Model Evaluation Script
Evaluates model performance with detailed metrics and visualizations.
"""

import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import joblib

MODEL_DIR = Path(__file__).parent / "models"
MODEL_NAME = "phishing_detection_model_latest.pkl"
OUTPUT_DIR = Path(__file__).parent / "evaluation"
OUTPUT_DIR.mkdir(exist_ok=True)

def load_model_and_data():
    """Load model and test data."""
    # Load model
    model_path = MODEL_DIR / MODEL_NAME
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found: {model_path}")
    model = joblib.load(model_path)
    
    # Load data
    data_path = Path(__file__).parent.parent / "Phishing_Legitimate_full.csv"
    df = pd.read_csv(data_path)
    
    # Prepare features
    feature_cols = [col for col in df.columns if col not in ['id', 'CLASS_LABEL']]
    X = df[feature_cols].copy()
    y = df['CLASS_LABEL'].copy()
    
    X = X.fillna(0).replace(-1, 0)
    
    return model, X, y, feature_cols

def evaluate_model(model, X, y):
    """Evaluate model with comprehensive metrics."""
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)[:, 1]
    
    metrics = {
        'accuracy': accuracy_score(y, predictions),
        'precision': precision_score(y, predictions),
        'recall': recall_score(y, predictions),
        'f1_score': f1_score(y, predictions),
        'roc_auc': roc_auc_score(y, probabilities)
    }
    
    return predictions, probabilities, metrics

def plot_confusion_matrix(y_true, y_pred, save_path):
    """Plot and save confusion matrix."""
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Legitimate', 'Phishing'],
                yticklabels=['Legitimate', 'Phishing'])
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    print(f"Confusion matrix saved to: {save_path}")

def plot_roc_curve(y_true, y_prob, save_path):
    """Plot and save ROC curve."""
    fpr, tpr, thresholds = roc_curve(y_true, y_prob)
    auc = roc_auc_score(y_true, y_prob)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {auc:.4f})')
    plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    print(f"ROC curve saved to: {save_path}")

def plot_feature_importance(model, feature_names, top_n=20, save_path=None):
    """Plot feature importance."""
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:top_n]
    
    plt.figure(figsize=(10, 8))
    plt.barh(range(top_n), importances[indices])
    plt.yticks(range(top_n), [feature_names[i] for i in indices])
    plt.xlabel('Importance')
    plt.title(f'Top {top_n} Feature Importance')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        plt.close()
        print(f"Feature importance plot saved to: {save_path}")
    else:
        plt.show()

def main():
    """Main evaluation function."""
    print("Loading model and data...")
    model, X, y, feature_names = load_model_and_data()
    print(f"Evaluating on {len(X)} records")
    
    print("\nEvaluating model...")
    predictions, probabilities, metrics = evaluate_model(model, X, y)
    
    print("\n" + "="*50)
    print("MODEL EVALUATION RESULTS")
    print("="*50)
    print(f"\nAccuracy:  {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall:    {metrics['recall']:.4f}")
    print(f"F1 Score:  {metrics['f1_score']:.4f}")
    print(f"ROC AUC:   {metrics['roc_auc']:.4f}")
    
    print("\n" + "="*50)
    print("CLASSIFICATION REPORT")
    print("="*50)
    print(classification_report(y, predictions, 
                                target_names=['Legitimate', 'Phishing']))
    
    # Generate plots
    print("\nGenerating visualizations...")
    plot_confusion_matrix(y, predictions, OUTPUT_DIR / "confusion_matrix.png")
    plot_roc_curve(y, probabilities, OUTPUT_DIR / "roc_curve.png")
    plot_feature_importance(model, feature_names, 
                           save_path=OUTPUT_DIR / "feature_importance.png")
    
    # Save metrics to file
    import json
    metrics_file = OUTPUT_DIR / "metrics.json"
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"\nMetrics saved to: {metrics_file}")
    
    print("\nEvaluation complete!")

if __name__ == "__main__":
    main()


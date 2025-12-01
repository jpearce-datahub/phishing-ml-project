# Machine Learning Components

This directory contains the core machine learning components for phishing URL detection.

## Overview

The ML pipeline implements a Random Forest classifier trained on 48 URL-based features to detect phishing websites with 98%+ accuracy.

## Components

### Training (`train.py`)

Trains a Random Forest model on the phishing dataset:
- Loads and preprocesses the dataset
- Performs feature engineering and data splitting
- Trains the model with optimized hyperparameters
- Evaluates performance on validation and test sets
- Saves the trained model and metadata

**Usage:**
```bash
python train.py
```

**Output:**
- Trained model: `models/phishing_detection_model_latest.pkl`
- Model metadata: `models/phishing_detection_model_TIMESTAMP_metadata.json`

### Inference (`inference.py`)

Performs batch or single predictions using the trained model:
- Loads the trained model
- Preprocesses input features
- Generates predictions and confidence scores
- Supports both batch processing and single record prediction

**Usage:**
```bash
# Batch inference
python inference.py input_file.csv output_file.csv

# Single prediction (used by API)
from inference import predict_single_record
result = predict_single_record(features_dict)
```

### Evaluation (`evaluate.py`)

Comprehensive model evaluation and performance analysis:
- Detailed performance metrics
- Feature importance analysis
- Model comparison utilities
- Cross-validation results

## Model Performance

- **Algorithm**: Random Forest Classifier (100 estimators)
- **Training Accuracy**: 98.19%
- **Validation Accuracy**: 98.19%
- **Test Accuracy**: 98.30%
- **F1 Score**: 98.30%
- **Precision**: 98.49%
- **Recall**: 97.88%

## Feature Engineering

The model uses 48 URL-based features including:

### Top Features by Importance
1. **PctExtHyperlinks** (23.78%) - Percentage of external hyperlinks
2. **PctExtNullSelfRedirectHyperlinksRT** (9.77%) - External null redirect links
3. **FrequentDomainNameMismatch** (9.11%) - Domain name inconsistencies
4. **PctExtResourceUrls** (8.91%) - External resource URLs
5. **PctNullSelfRedirectHyperlinks** (7.02%) - Null self-redirect links

### Feature Categories
- **URL Structure**: Length, dots, subdomains, paths
- **Security Indicators**: HTTPS usage, IP addresses, certificates
- **Content Analysis**: External links, forms, scripts
- **Behavioral Patterns**: Redirects, pop-ups, disabled features

## Dataset

- **Total Records**: 10,000 labeled URLs
- **Features**: 48 URL-based characteristics
- **Classes**: Binary (0=Legitimate, 1=Phishing)
- **Split**: 64% train, 16% validation, 20% test

## Model Configuration

```python
RandomForestClassifier(
    n_estimators=100,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)
```

## Data Preprocessing

- Missing value imputation (fill with 0)
- Replacement of -1 indicators with 0
- Feature scaling not required for Random Forest
- Stratified sampling for balanced splits

## Model Artifacts

The training process generates:
- **Model File**: Serialized RandomForest classifier
- **Metadata**: Performance metrics, feature importance, timestamps
- **Feature Names**: List of all features used in training

## Dependencies

- pandas
- numpy
- scikit-learn
- joblib

## Future Enhancements

- XGBoost implementation for comparison
- Feature selection optimization
- Hyperparameter tuning with GridSearch
- Model ensemble techniques
- Online learning capabilities
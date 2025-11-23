# ML Component

Machine learning models for phishing detection and threat intelligence.

## Files

- `train.py`: Train phishing detection model
- `inference.py`: Batch and single-record inference
- `evaluate.py`: Comprehensive model evaluation
- `sagemaker_pipeline.yml`: AWS SageMaker pipeline configuration

## Usage

### Local Training

```bash
python train.py
```

This will:
1. Load the phishing dataset
2. Prepare features
3. Train a Random Forest classifier
4. Evaluate on validation and test sets
5. Save model and metadata
6. Optionally upload to S3

### Batch Inference

```bash
python inference.py input_data.csv output_predictions.csv
```

### Model Evaluation

```bash
python evaluate.py
```

Generates:
- Confusion matrix
- ROC curve
- Feature importance plot
- Detailed metrics report

## Model Details

- **Algorithm**: Random Forest Classifier
- **Features**: 48 URL characteristics
- **Target**: Binary classification (phishing vs legitimate)
- **Performance**: Typically achieves >95% accuracy

## SageMaker Integration

For cloud training, configure AWS credentials and use the SageMaker pipeline:

```bash
# Upload code to S3
aws s3 cp train.py s3://org-product-logs-ml-models/code/

# Create and run pipeline
python create_sagemaker_pipeline.py
```

## Model Outputs

Models are saved to `ml/models/`:
- `phishing_detection_model_latest.pkl`: Latest model
- `phishing_detection_model_TIMESTAMP.pkl`: Timestamped versions
- `phishing_detection_model_TIMESTAMP_metadata.json`: Model metadata

## Feature Importance

The model identifies key phishing indicators:
- URL structure (length, dots, subdomains)
- Security features (HTTPS, IP addresses)
- Behavioral indicators (sensitive words, forms, iframes)


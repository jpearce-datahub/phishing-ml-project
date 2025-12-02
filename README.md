# Phishing ML Project

A comprehensive machine learning project for phishing detection using URL features and threat intelligence metrics.

## Overview

This project implements an end-to-end machine learning pipeline for detecting phishing URLs. It includes data ingestion, feature engineering, model training, inference, and a REST API for real-time predictions.

## Architecture

```
CSV Dataset -> Feature Engineering -> ML Training -> Model Serving
                                          |
                                    FastAPI Service
                                          |
                              Real-time Predictions
```

## Project Structure

```
phishing-ml/
├── api/                    # FastAPI service
│   ├── app.py             # Main API application
│   ├── tests/             # API tests
│   ├── Dockerfile         # Container configuration
│   └── requirements.txt   # API dependencies
├── ml/                    # Machine learning components
│   ├── train.py          # Model training script
│   ├── inference.py      # Prediction script
│   ├── evaluate.py       # Model evaluation
│   └── models/           # Saved models (gitignored)
├── transform/            # dbt data transformations
│   └── dbt_project/      # dbt models and configurations
├── orchestration/        # Workflow management
│   ├── airflow_dag.py    # Airflow workflow
│   └── step_functions_definition.json
├── ingestion/           # Data ingestion scripts
│   ├── upload_to_s3.py  # S3 upload utility
│   └── process_dataset.py # Data preprocessing
├── docs/                # Documentation
└── Phishing_Legitimate_full.csv  # Training dataset
```

## Model Performance

- **Algorithm**: Random Forest Classifier
- **Training Accuracy**: 98.19%
- **Test Accuracy**: 98.30%
- **F1 Score**: 98.30%
- **Features**: 48 URL-based features
- **Dataset**: 10,000 labeled URLs

## Key Features Analyzed

1. **PctExtHyperlinks** (23.78% importance)
2. **PctExtNullSelfRedirectHyperlinksRT** (9.77% importance)
3. **FrequentDomainNameMismatch** (9.11% importance)
4. **PctExtResourceUrls** (8.91% importance)
5. **PctNullSelfRedirectHyperlinks** (7.02% importance)

## API Endpoints

- `GET /health` - System health check
- `POST /predict` - Real-time phishing detection
- `GET /metrics/threat-block-rate` - Threat blocking metrics
- `GET /metrics/product-efficacy` - Product efficacy scores
- `GET /metrics/user/{user_id}` - User-specific metrics
- `GET /model/info` - Model information and feature importance

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Train the model: `python ml/train.py`
4. Start the API: `python api/app.py`

## Usage

### Training a Model

```bash
cd ml
python train.py
```

### Running Inference

```bash
cd ml
python inference.py input_file.csv output_file.csv
```

### Starting the API

```bash
cd api
python app.py
```

The API will be available at `http://localhost:8000`

## Docker Support

Build and run the API container:

```bash
cd api
docker build -t phishing-api .
docker run -p 8000:8000 phishing-api
```

## Technologies

- **ML Framework**: Scikit-learn
- **API**: FastAPI
- **Data Processing**: Pandas, NumPy
- **Containerization**: Docker
- **Orchestration**: Airflow, AWS Step Functions
- **Data Transformation**: dbt

## Features

- Random Forest classifier with 98%+ accuracy
- Real-time phishing detection API
- Comprehensive feature engineering (48 URL-based features)
- Scalable data pipeline architecture
- Threat intelligence metrics and reporting
- Docker containerization support




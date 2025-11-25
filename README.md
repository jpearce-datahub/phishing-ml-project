# Product Threat-Intelligence Metrics Platform

A comprehensive, production-ready analytics engineering project demonstrating end-to-end data pipeline capabilities from ingestion to ML to dashboards.

## Project Overview

This platform ingests phishing threat intelligence data, transforms it through a dimensional model, trains ML models for threat detection, and exposes metrics through APIs and dashboards. Built to mirror real-world security SaaS analytics engineering workflows.

## Architecture

```
CSV Dataset -> S3 -> AWS Glue Crawler -> Athena External Tables
                    |
              dbt (Core)
                    |
        Dimensional Model in Athena (ELT)
                    |
       ML Training Pipeline (SageMaker)
                    |
         API Layer (FastAPI in Docker)
                    |
    Dashboard (PowerBI / Looker / Quicksight)
```

## Project Structure

```
phishing-ml/
├── ingestion/              # Data ingestion scripts
├── transform/              # dbt project
│   └── dbt_project/
├── orchestration/          # Pipeline orchestration configs
├── ml/                     # ML training and inference
├── api/                    # FastAPI service
├── bi/                     # Dashboard files
├── docs/                   # Documentation
└── Phishing_Legitimate_full.csv  # Source dataset
```



## Key Metrics

- **Threat Detection Rate**: Percentage of phishing URLs correctly identified
- **False Positive Rate**: Legitimate URLs incorrectly flagged
- **Model Accuracy**: Overall ML model performance
- **Feature Importance**: Top indicators of phishing URLs
- **Threat Severity Distribution**: Breakdown by threat characteristics


## Documentation

- [Architecture Documentation](docs/ARCHITECTURE.md)
- [dbt Model Documentation](transform/dbt_project/docs/)
- [API Documentation](api/README.md)
- [ML Model Documentation](ml/README.md)

## Technologies

- **Data Warehouse**: AWS Athena / PostgreSQL
- **Transformation**: dbt-core
- **ML Framework**: Scikit-learn, SageMaker
- **API**: FastAPI
- **Containerization**: Docker
- **Orchestration**: AWS Step Functions / Airflow
- **BI Tools**: PowerBI / Looker / Quicksight

## Features

- Dimensional modeling with dbt
- ML model training and inference
- RESTful API for metrics access
- Docker containerization
- Cloud-native architecture (AWS)
- Comprehensive data quality tests
- Automated pipeline orchestration

## License

MIT License

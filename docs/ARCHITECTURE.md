# Architecture Documentation

## Overview

The Product Threat-Intelligence Metrics Platform is a cloud-native analytics engineering system designed to process, analyze, and expose phishing threat intelligence data through a complete ELT pipeline.

## System Architecture

```
┌─────────────────┐
│  CSV Dataset    │
│  (10K records) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Ingestion      │
│  - process.py   │
│  - S3 Upload    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AWS S3         │
│  Raw JSON Files │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AWS Glue       │
│  Crawler        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AWS Athena     │
│  External Tables│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  dbt Core       │
│  Transformations│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Dimensional    │
│  Model          │
│  - dim_user     │
│  - dim_threat   │
│  - fact_events  │
│  - metrics      │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌──────────┐
│  ML    │ │  API     │
│ Model  │ │  Service │
└────┬───┘ └─────┬─────┘
     │          │
     └────┬─────┘
          │
          ▼
    ┌──────────┐
    │ Dashboard│
    │ (PowerBI)│
    └──────────┘
```

## Components

### 1. Data Ingestion

**Purpose**: Transform CSV dataset into event-like JSON structure

**Components**:
- `process_dataset.py`: Converts CSV to JSON events
- `upload_to_s3.py`: Uploads to S3 with date partitioning
- `glue_crawler_config.yml`: AWS Glue configuration

**Output**: JSON files in S3 partitioned by date

### 2. Data Warehouse (AWS Athena)

**Purpose**: Query raw data using SQL

**Setup**:
- Glue Crawler detects schema from JSON files
- Creates external tables in Athena
- Enables SQL queries on S3 data

### 3. Transformation Layer (dbt)

**Purpose**: Transform raw data into dimensional model

**Layers**:
- **Staging**: Clean and standardize raw data
- **Marts**: Dimensional models (facts and dimensions)
- **Metrics**: Pre-calculated business metrics

**Key Models**:
- `dim_user`: User dimension with aggregated metrics
- `dim_threat`: Threat dimension with severity classification
- `fact_events`: Event-level fact table
- `threat_block_rate`: Daily threat detection metrics
- `product_efficacy_score`: Overall product performance

### 4. ML Component

**Purpose**: Train and deploy phishing detection models

**Components**:
- `train.py`: Local or SageMaker training
- `inference.py`: Batch and real-time predictions
- `evaluate.py`: Model evaluation and metrics

**Model**: Random Forest Classifier
- 48 features (URL characteristics)
- Binary classification (phishing vs legitimate)
- Typically >95% accuracy

### 5. API Layer (FastAPI)

**Purpose**: Expose metrics and predictions via REST API

**Endpoints**:
- `/metrics/threat-block-rate`: Threat detection metrics
- `/metrics/product-efficacy`: Product performance score
- `/metrics/user/{id}`: User-specific metrics
- `/predict`: Real-time threat prediction

**Deployment**: Docker container

### 6. Orchestration

**Purpose**: Schedule and coordinate pipeline execution

**Options**:
- AWS Step Functions: Serverless orchestration
- Apache Airflow: More flexible workflow management

**Pipeline Steps**:
1. Process raw data
2. Run Glue crawler
3. Run dbt transformations
4. Run dbt tests
5. Train ML model
6. Update metrics
7. Send notifications

## Data Flow

### Batch Processing (Daily)

1. New data arrives in S3
2. Glue Crawler updates schema
3. dbt runs transformations
4. ML model retrains (if needed)
5. Metrics tables refresh
6. Dashboard updates

### Real-time

1. API receives prediction request
2. Loads ML model
3. Makes prediction
4. Returns result

## Technology Stack

- **Data Storage**: AWS S3
- **Data Warehouse**: AWS Athena / PostgreSQL
- **Transformation**: dbt-core
- **ML Framework**: Scikit-learn, SageMaker
- **API**: FastAPI
- **Containerization**: Docker
- **Orchestration**: AWS Step Functions / Airflow
- **BI Tools**: PowerBI / Looker / Quicksight

## Scalability Considerations

- **S3**: Virtually unlimited storage
- **Athena**: Pay-per-query, scales automatically
- **dbt**: Stateless transformations, parallel execution
- **ML**: SageMaker supports distributed training
- **API**: Horizontal scaling with load balancer

## Security

- IAM roles for AWS services
- VPC endpoints for S3 access
- API authentication (can add OAuth/JWT)
- Encrypted data at rest (S3)
- Encrypted data in transit (HTTPS)

## Monitoring & Observability

- CloudWatch logs for all services
- dbt test results for data quality
- ML model metrics (accuracy, F1 score)
- API response times and error rates
- Pipeline execution history

## Cost Optimization

- S3 lifecycle policies for old data
- Athena query result caching
- SageMaker spot instances for training
- API auto-scaling based on demand
- dbt incremental models for large tables

## Future Enhancements

- Real-time streaming with Kinesis
- Feature store for ML features
- A/B testing framework for models
- Advanced anomaly detection
- Graph database for threat relationships


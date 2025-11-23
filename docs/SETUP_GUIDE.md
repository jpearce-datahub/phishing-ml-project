# Setup Guide

Complete setup instructions for the Product Threat-Intelligence Metrics Platform.

## Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose
- AWS CLI configured (for cloud deployment)
- PostgreSQL (for local development) or AWS Athena (for cloud)
- Git

## Local Development Setup

### 1. Clone and Navigate

```bash
cd C:\Users\pearc\phishing-ml
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Process Dataset

```bash
cd ingestion
python process_dataset.py
```

This creates JSON files in `ingestion/output/`.

### 5. Setup Database (PostgreSQL)

```bash
# Create database
createdb phishing_ml

# Or using psql
psql -U postgres
CREATE DATABASE phishing_ml;
```

### 6. Configure dbt

Edit `transform/dbt_project/profiles.yml` with your database credentials.

### 7. Run dbt Transformations

```bash
cd transform/dbt_project
dbt deps
dbt run
dbt test
```

### 8. Train ML Model

```bash
cd ml
python train.py
```

### 9. Start API Service

```bash
cd api
docker-compose up --build
```

API will be available at http://localhost:8000

## AWS Cloud Setup

### 1. S3 Buckets

Create buckets:
- `org-product-logs` - Raw data
- `org-product-logs-ml-models` - ML models
- `org-product-logs/dbt-staging/` - dbt staging

### 2. AWS Glue

1. Create Glue database: `phishing_ml_db`
2. Create Glue crawler using `ingestion/glue_crawler_config.yml`
3. Run crawler to create Athena tables

### 3. AWS Athena

1. Verify tables created by Glue crawler
2. Test queries on raw data

### 4. dbt with Athena

1. Install dbt-athena-community:
   ```bash
   pip install dbt-athena-community
   ```

2. Configure `profiles.yml` for Athena:
   ```yaml
   type: athena
   s3_staging_dir: s3://org-product-logs/dbt-staging/
   region_name: us-east-1
   ```

3. Run dbt:
   ```bash
   dbt run --profiles-dir transform/dbt_project
   ```

### 5. SageMaker Setup

1. Create SageMaker execution role
2. Upload training code to S3
3. Configure SageMaker pipeline (see `ml/sagemaker_pipeline.yml`)

### 6. Step Functions

1. Create Lambda functions for each pipeline step
2. Deploy state machine using `orchestration/step_functions_definition.json`
3. Create EventBridge rule for scheduling

## Verification

### Test Data Pipeline

```bash
# Check ingestion output
ls ingestion/output/

# Verify dbt models
cd transform/dbt_project
dbt list
dbt run --select staging
dbt test --select staging
```

### Test ML Model

```bash
cd ml
python evaluate.py
```

### Test API

```bash
# Health check
curl http://localhost:8000/health

# Get metrics
curl http://localhost:8000/metrics/threat-block-rate

# Make prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d @api/test_request.json
```

## Troubleshooting

### dbt Connection Issues

- Verify database credentials in `profiles.yml`
- Check network connectivity
- Ensure database exists and is accessible

### ML Model Not Loading

- Verify model file exists in `ml/models/`
- Run `python ml/train.py` to generate model
- Check file permissions

### API Errors

- Check Docker logs: `docker-compose logs api`
- Verify model path in environment variables
- Ensure all dependencies installed

### AWS Issues

- Verify AWS credentials: `aws sts get-caller-identity`
- Check IAM permissions
- Verify S3 bucket policies
- Check CloudWatch logs

## Next Steps

1. Review [Architecture Documentation](ARCHITECTURE.md)
2. Explore dbt models in `transform/dbt_project/models/`
3. Customize metrics in `transform/dbt_project/models/marts/metrics/`
4. Add additional API endpoints as needed
5. Set up monitoring and alerting

## Support

For issues or questions:
- Check logs in respective component directories
- Review CloudWatch logs (AWS)
- Consult component-specific README files


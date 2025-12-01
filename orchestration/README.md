# Orchestration

Workflow orchestration components for the phishing ML pipeline using Airflow and AWS Step Functions.

## Overview

This directory contains orchestration configurations for automating the end-to-end ML pipeline:
- Data ingestion and preprocessing
- Model training and evaluation
- Model deployment and serving
- Monitoring and alerting

## Components

### Airflow DAG (`airflow_dag.py`)

Defines the complete ML pipeline workflow:

**Tasks:**
1. **Data Validation**: Check data quality and freshness
2. **Feature Engineering**: Transform raw data into ML features
3. **Model Training**: Train and validate ML models
4. **Model Evaluation**: Performance testing and validation
5. **Model Deployment**: Deploy to serving infrastructure
6. **Monitoring Setup**: Configure alerts and dashboards

**Schedule**: Daily execution with configurable parameters
**Dependencies**: Sequential execution with parallel branches where possible

### Step Functions (`step_functions_definition.json`)

AWS Step Functions state machine for cloud-native orchestration:

**States:**
- **DataIngestion**: Trigger S3 upload and Glue crawler
- **DataTransformation**: Execute dbt models
- **ModelTraining**: Launch SageMaker training job
- **ModelEvaluation**: Validate model performance
- **ModelDeployment**: Deploy to SageMaker endpoint
- **NotificationSuccess**: Send success notifications
- **NotificationFailure**: Handle error notifications

## Workflow Architecture

```
Data Ingestion → Feature Engineering → Model Training
       ↓                ↓                   ↓
   Validation    →  Transformation  →   Evaluation
       ↓                ↓                   ↓
   Monitoring    →    Deployment    →   Serving
```

## Configuration

### Airflow Configuration

```python
default_args = {
    'owner': 'ml-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}
```

### Environment Variables

- `AIRFLOW_HOME`: Airflow installation directory
- `AWS_DEFAULT_REGION`: AWS region for resources
- `S3_BUCKET`: Data storage bucket
- `SAGEMAKER_ROLE`: IAM role for SageMaker
- `API_ENDPOINT`: Model serving endpoint

## Deployment

### Local Airflow

```bash
# Initialize Airflow
airflow db init

# Create admin user
airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com

# Start scheduler
airflow scheduler

# Start webserver
airflow webserver --port 8080
```

### AWS Step Functions

```bash
# Deploy state machine
aws stepfunctions create-state-machine \
  --name phishing-ml-pipeline \
  --definition file://step_functions_definition.json \
  --role-arn arn:aws:iam::ACCOUNT:role/StepFunctionsRole
```

## Monitoring

### Airflow Monitoring

- **Web UI**: Task status and logs at `http://localhost:8080`
- **Email Alerts**: Failure notifications
- **Slack Integration**: Real-time status updates
- **Metrics**: Task duration and success rates

### Step Functions Monitoring

- **CloudWatch**: Execution metrics and logs
- **SNS Notifications**: Success/failure alerts
- **X-Ray Tracing**: Performance analysis
- **Cost Monitoring**: Execution cost tracking

## Error Handling

### Retry Logic

- **Transient Failures**: Automatic retry with exponential backoff
- **Data Quality Issues**: Alert and manual intervention
- **Resource Limits**: Scale up or queue for later execution
- **Dependency Failures**: Skip non-critical tasks

### Alerting

- **Email**: Critical failure notifications
- **Slack**: Real-time status updates
- **PagerDuty**: On-call escalation for production issues
- **Dashboard**: Visual status monitoring

## Performance Optimization

### Parallel Execution

- **Data Processing**: Parallel feature engineering
- **Model Training**: Multiple model variants
- **Evaluation**: Concurrent testing scenarios

### Resource Management

- **Dynamic Scaling**: Auto-scale based on workload
- **Spot Instances**: Cost optimization for training
- **Resource Pools**: Dedicated compute for critical tasks

## Dependencies

- Apache Airflow
- AWS CLI
- boto3
- pandas
- scikit-learn

## Best Practices

- **Idempotency**: All tasks can be safely re-run
- **Logging**: Comprehensive logging for debugging
- **Testing**: Unit tests for all workflow components
- **Documentation**: Clear task descriptions and dependencies
- **Version Control**: All configurations in git
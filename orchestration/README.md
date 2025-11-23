# Orchestration Layer

Pipeline orchestration configurations for AWS Step Functions and Apache Airflow.

## AWS Step Functions

The Step Functions state machine defines the complete pipeline workflow:

1. Process raw data
2. Run Glue crawler
3. Run dbt transformations
4. Run dbt tests
5. Train ML model (if tests pass)
6. Update metrics tables
7. Send notifications

### Deployment

```bash
# Create state machine
aws stepfunctions create-state-machine \
  --name phishing-ml-pipeline \
  --definition file://step_functions_definition.json \
  --role-arn arn:aws:iam::ACCOUNT_ID:role/StepFunctionsExecutionRole
```

### Scheduling

Use EventBridge to schedule the pipeline:

```json
{
  "ScheduleExpression": "cron(0 2 * * ? *)",
  "Target": {
    "Arn": "arn:aws:states:us-east-1:ACCOUNT_ID:stateMachine:phishing-ml-pipeline",
    "RoleArn": "arn:aws:iam::ACCOUNT_ID:role/EventBridgeExecutionRole"
  }
}
```

## Apache Airflow

The Airflow DAG provides an alternative orchestration option with more flexibility.

### Setup

1. Install Airflow with AWS providers:
   ```bash
   pip install apache-airflow[amazon]
   ```

2. Configure AWS connection in Airflow UI

3. Place `airflow_dag.py` in your DAGs folder

### DAG Structure

- Daily schedule
- Automatic retries on failure
- Email notifications
- Parallel task execution where possible

## Pipeline Flow

```
Raw Data Processing
    |
Glue Crawler (Schema Detection)
    |
dbt Transformations
    |
dbt Tests (Data Quality)
    |
ML Model Training (SageMaker)
    |
Metrics Table Updates
    |
Notifications
```

## Monitoring

Both orchestration options support:
- CloudWatch logs
- Error notifications (SNS/Email)
- Execution history
- Retry logic


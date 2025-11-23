"""
Apache Airflow DAG for Phishing ML Pipeline
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.amazon.aws.operators.glue import GlueCrawlerOperator
from airflow.providers.amazon.aws.operators.sagemaker import SageMakerTrainingOperator
from airflow.providers.amazon.aws.sensors.glue import GlueCrawlerSensor
from datetime import datetime, timedelta

default_args = {
    'owner': 'analytics-engineering',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'phishing_ml_pipeline',
    default_args=default_args,
    description='End-to-end phishing threat intelligence pipeline',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['phishing', 'ml', 'threat-intelligence'],
)

def process_raw_data(**context):
    """Process raw data and upload to S3."""
    import subprocess
    result = subprocess.run(
        ['python', 'ingestion/process_dataset.py'],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise Exception(f"Data processing failed: {result.stderr}")
    return "Data processed successfully"

def run_dbt_transform(**context):
    """Run dbt transformations."""
    import subprocess
    result = subprocess.run(
        ['dbt', 'run', '--project-dir', 'transform/dbt_project'],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise Exception(f"dbt transformation failed: {result.stderr}")
    return "dbt transformations completed"

def run_dbt_tests(**context):
    """Run dbt tests."""
    import subprocess
    result = subprocess.run(
        ['dbt', 'test', '--project-dir', 'transform/dbt_project'],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise Exception(f"dbt tests failed: {result.stderr}")
    return "dbt tests passed"

# Task definitions
process_data_task = PythonOperator(
    task_id='process_raw_data',
    python_callable=process_raw_data,
    dag=dag,
)

run_glue_crawler = GlueCrawlerOperator(
    task_id='run_glue_crawler',
    crawler_name='phishing-ml-events-crawler',
    aws_conn_id='aws_default',
    dag=dag,
)

wait_for_crawler = GlueCrawlerSensor(
    task_id='wait_for_crawler',
    crawler_name='phishing-ml-events-crawler',
    aws_conn_id='aws_default',
    dag=dag,
)

run_dbt_task = PythonOperator(
    task_id='run_dbt_transformations',
    python_callable=run_dbt_transform,
    dag=dag,
)

run_dbt_tests_task = PythonOperator(
    task_id='run_dbt_tests',
    python_callable=run_dbt_tests,
    dag=dag,
)

train_ml_model = SageMakerTrainingOperator(
    task_id='train_ml_model',
    config={
        'TrainingJobName': 'phishing-detection-{{ ds_nodash }}',
        'RoleArn': 'arn:aws:iam::ACCOUNT_ID:role/SageMakerExecutionRole',
        'AlgorithmSpecification': {
            'TrainingImage': '763104351884.dkr.ecr.us-east-1.amazonaws.com/sklearn-training:1.0-1-cpu',
            'TrainingInputMode': 'File'
        },
        'InputDataConfig': [
            {
                'ChannelName': 'training',
                'DataSource': {
                    'S3DataSource': {
                        'S3DataType': 'S3Prefix',
                        'S3Uri': 's3://org-product-logs-ml-models/processed/train/',
                        'S3DataDistributionType': 'FullyReplicated'
                    }
                }
            }
        ],
        'OutputDataConfig': {
            'S3OutputPath': 's3://org-product-logs-ml-models/models/'
        },
        'ResourceConfig': {
            'InstanceType': 'ml.m5.xlarge',
            'InstanceCount': 1,
            'VolumeSizeInGB': 30
        },
        'StoppingCondition': {
            'MaxRuntimeInSeconds': 3600
        },
        'HyperParameters': {
            'n_estimators': '100',
            'max_depth': '20',
            'min_samples_split': '5'
        }
    },
    aws_conn_id='aws_default',
    dag=dag,
)

update_metrics = BashOperator(
    task_id='update_metrics_tables',
    bash_command='python ml/inference.py --batch-mode',
    dag=dag,
)

# Task dependencies
process_data_task >> run_glue_crawler >> wait_for_crawler >> run_dbt_task
run_dbt_task >> run_dbt_tests_task >> train_ml_model >> update_metrics


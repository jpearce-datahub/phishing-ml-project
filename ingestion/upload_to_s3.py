"""
Script to upload processed JSON files to S3 bucket.
Requires AWS credentials configured via AWS CLI or environment variables.
"""

import boto3
from pathlib import Path
import os
from datetime import datetime

# Configuration
BUCKET_NAME = "org-product-logs"
S3_PREFIX = "raw"
LOCAL_DIR = Path(__file__).parent / "output"

def upload_files():
    """Upload JSON files to S3 with date partitioning."""
    s3_client = boto3.client('s3')
    
    if not LOCAL_DIR.exists():
        print(f"Error: Output directory {LOCAL_DIR} does not exist.")
        print("Run process_dataset.py first to generate JSON files.")
        return
    
    json_files = list(LOCAL_DIR.glob("*.json"))
    
    if not json_files:
        print(f"No JSON files found in {LOCAL_DIR}")
        return
    
    print(f"Found {len(json_files)} files to upload")
    
    # Get today's date for partitioning
    today = datetime.now().strftime("%Y-%m-%d")
    
    uploaded = 0
    for json_file in json_files:
        s3_key = f"{S3_PREFIX}/{today}/{json_file.name}"
        
        try:
            s3_client.upload_file(
                str(json_file),
                BUCKET_NAME,
                s3_key
            )
            print(f"Uploaded: {json_file.name} -> s3://{BUCKET_NAME}/{s3_key}")
            uploaded += 1
        except Exception as e:
            print(f"Error uploading {json_file.name}: {e}")
    
    print(f"\nUpload complete: {uploaded}/{len(json_files)} files uploaded")

if __name__ == "__main__":
    # Check AWS credentials
    try:
        boto3.client('sts').get_caller_identity()
    except Exception as e:
        print("Error: AWS credentials not configured.")
        print("Please configure AWS CLI or set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
        exit(1)
    
    upload_files()


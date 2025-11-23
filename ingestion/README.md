# Data Ingestion Layer

This directory contains scripts for processing and ingesting the phishing dataset into the data pipeline.

## Files

- `process_dataset.py`: Transforms CSV dataset into event-like JSON structure
- `upload_to_s3.py`: Uploads processed JSON files to S3 bucket
- `glue_crawler_config.yml`: AWS Glue Crawler configuration for schema detection

## Usage

1. Process the dataset:
   ```bash
   python process_dataset.py
   ```
   This creates JSON files in the `output/` directory.

2. Upload to S3 (requires AWS credentials):
   ```bash
   python upload_to_s3.py
   ```

## Output Format

Each JSON file contains an array of event objects with the following structure:

```json
{
  "event_id": "evt_1",
  "user_id": "user_123",
  "timestamp": "2024-01-15T10:30:00",
  "event_type": "threat_detected",
  "threat_id": "threat_1",
  "is_phishing": 1,
  "metadata": {
    "url_length": 72,
    "num_dots": 3,
    ...
  },
  "user_metadata": {
    "department": "Engineering",
    "region": "US-East",
    "role": "Manager"
  },
  "raw_features": { ... }
}
```

## S3 Structure

```
s3://org-product-logs/
  raw/
    YYYY-MM-DD/
      events_batch_0000.json
      events_batch_0001.json
      ...
```


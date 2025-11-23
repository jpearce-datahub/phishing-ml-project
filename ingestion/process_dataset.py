"""
Data ingestion script to process the phishing dataset and prepare it for ELT pipeline.

This script:
1. Reads the CSV dataset
2. Transforms it into event-like structure
3. Generates synthetic user and timestamp data
4. Outputs JSON files ready for S3 upload
"""

import pandas as pd
import json
import os
from datetime import datetime, timedelta
import random
from pathlib import Path

# Configuration
INPUT_CSV = Path(__file__).parent.parent / "Phishing_Legitimate_full.csv"
OUTPUT_DIR = Path(__file__).parent / "output"
BATCH_SIZE = 1000  # Records per JSON file

def generate_user_metadata():
    """Generate synthetic user metadata for each record."""
    departments = ["Engineering", "Sales", "Marketing", "HR", "Finance", "Operations"]
    regions = ["US-East", "US-West", "EU", "APAC"]
    roles = ["Manager", "Individual Contributor", "Director", "VP"]
    
    return {
        "department": random.choice(departments),
        "region": random.choice(regions),
        "role": random.choice(roles)
    }

def transform_to_event(row, user_id, timestamp):
    """Transform a CSV row into an event-like JSON structure."""
    event_type = "threat_detected" if row['CLASS_LABEL'] == 1 else "legitimate_url"
    
    # Extract key features for metadata
    metadata = {
        "url_length": int(row['UrlLength']),
        "num_dots": int(row['NumDots']),
        "subdomain_level": int(row['SubdomainLevel']),
        "path_level": int(row['PathLevel']),
        "has_https": 0 if row['NoHttps'] == 1 else 1,
        "has_ip_address": int(row['IpAddress']),
        "num_sensitive_words": int(row['NumSensitiveWords']),
        "has_random_string": int(row['RandomString']),
        "hostname_length": int(row['HostnameLength']),
        "path_length": int(row['PathLength']),
        "query_length": int(row['QueryLength']),
        "pct_ext_hyperlinks": float(row['PctExtHyperlinks']),
        "pct_ext_resource_urls": float(row['PctExtResourceUrls']),
        "abnormal_form_action": int(row['AbnormalFormAction']),
        "iframe_or_frame": int(row['IframeOrFrame']),
        "missing_title": int(row['MissingTitle']),
        "right_click_disabled": int(row['RightClickDisabled']),
        "popup_window": int(row['PopUpWindow']),
    }
    
    user_meta = generate_user_metadata()
    
    event = {
        "event_id": f"evt_{row['id']}",
        "user_id": user_id,
        "timestamp": timestamp.isoformat(),
        "event_type": event_type,
        "threat_id": f"threat_{row['id']}",
        "is_phishing": int(row['CLASS_LABEL']),
        "metadata": metadata,
        "user_metadata": user_meta,
        "raw_features": {
            k: float(v) if isinstance(v, (int, float)) else int(v)
            for k, v in row.items()
            if k not in ['id', 'CLASS_LABEL']
        }
    }
    
    return event

def process_dataset():
    """Main processing function."""
    print("Reading dataset...")
    df = pd.read_csv(INPUT_CSV)
    print(f"Loaded {len(df)} records")
    
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Generate base timestamp
    base_time = datetime.now() - timedelta(days=30)
    
    # Process in batches
    num_batches = (len(df) + BATCH_SIZE - 1) // BATCH_SIZE
    
    for batch_num in range(num_batches):
        start_idx = batch_num * BATCH_SIZE
        end_idx = min(start_idx + BATCH_SIZE, len(df))
        batch_df = df.iloc[start_idx:end_idx]
        
        events = []
        for idx, row in batch_df.iterrows():
            # Generate synthetic user_id (reuse some users)
            user_id = f"user_{random.randint(1, 500)}"
            
            # Generate timestamp (spread over last 30 days)
            days_offset = random.randint(0, 30)
            hours_offset = random.randint(0, 23)
            timestamp = base_time + timedelta(days=days_offset, hours=hours_offset)
            
            event = transform_to_event(row, user_id, timestamp)
            events.append(event)
        
        # Write batch to JSON file
        output_file = OUTPUT_DIR / f"events_batch_{batch_num:04d}.json"
        with open(output_file, 'w') as f:
            json.dump(events, f, indent=2)
        
        print(f"Processed batch {batch_num + 1}/{num_batches} ({len(events)} events)")
    
    print(f"\nProcessing complete. Output files in: {OUTPUT_DIR}")
    print(f"Total events: {len(df)}")
    print(f"Total batches: {num_batches}")

if __name__ == "__main__":
    process_dataset()


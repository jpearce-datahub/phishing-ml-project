# Data Ingestion

Scripts and utilities for ingesting phishing threat intelligence data into the ML pipeline.

## Overview

This directory contains tools for:
- Dataset preprocessing and validation
- S3 data upload and management
- AWS Glue crawler configuration
- Data quality monitoring

## Components

### Dataset Processing (`process_dataset.py`)

Preprocesses raw phishing datasets for ML training:

**Features:**
- Data validation and cleaning
- Feature engineering and normalization
- Missing value handling
- Data type conversions
- Statistical analysis and profiling

**Usage:**
```bash
python process_dataset.py --input raw_data.csv --output processed_data.csv
```

### S3 Upload Utility (`upload_to_s3.py`)

Manages data upload to AWS S3 for cloud processing:

**Features:**
- Batch file upload with progress tracking
- Automatic partitioning by date/type
- Metadata tagging and organization
- Error handling and retry logic
- Cost optimization with storage classes

**Usage:**
```bash
python upload_to_s3.py --bucket my-bucket --file dataset.csv --prefix phishing-data/
```

### Glue Crawler Configuration (`glue_crawler_config.yml`)

AWS Glue crawler configuration for automatic schema discovery:

**Features:**
- Automatic table creation in Data Catalog
- Schema evolution handling
- Partition discovery
- Data format detection
- Integration with Athena

## Data Sources

### Primary Dataset
- **File**: `Phishing_Legitimate_full.csv`
- **Records**: 10,000 labeled URLs
- **Features**: 48 URL characteristics
- **Format**: CSV with headers
- **Size**: ~2MB

### Feature Categories

**URL Structure Features:**
- NumDots, SubdomainLevel, PathLevel
- UrlLength, HostnameLength, PathLength
- NumDash, NumUnderscore, NumPercent

**Security Indicators:**
- NoHttps, HttpsInHostname
- IpAddress, AtSymbol, TildeSymbol
- RandomString, DomainInSubdomains

**Content Analysis:**
- PctExtHyperlinks, PctExtResourceUrls
- ExtFavicon, InsecureForms
- IframeOrFrame, MissingTitle

**Behavioral Patterns:**
- FrequentDomainNameMismatch
- FakeLinkInStatusBar, RightClickDisabled
- PopUpWindow, SubmitInfoToEmail

## Data Quality

### Validation Rules

- **Completeness**: No missing required fields
- **Consistency**: Valid value ranges for all features
- **Accuracy**: Logical relationships between features
- **Uniqueness**: No duplicate records

### Quality Metrics

- **Missing Values**: < 1% per feature
- **Outliers**: Statistical detection and handling
- **Data Types**: Proper numeric/categorical encoding
- **Distributions**: Feature distribution analysis

## Processing Pipeline

```
Raw Data → Validation → Cleaning → Feature Engineering → Upload
    ↓           ↓          ↓             ↓              ↓
  Schema    Quality    Normalize    Transform       Store
  Check     Check      Values       Features        S3
```

## Configuration

### Environment Variables

```bash
export AWS_REGION=us-east-1
export S3_BUCKET=phishing-ml-data
export GLUE_DATABASE=phishing_intelligence
export DATA_PREFIX=datasets/
```

### Processing Parameters

```python
PROCESSING_CONFIG = {
    'missing_value_threshold': 0.01,
    'outlier_detection_method': 'iqr',
    'feature_scaling': False,
    'validation_split': 0.2
}
```

## Monitoring

### Data Quality Dashboard

- **Freshness**: Data recency monitoring
- **Volume**: Record count tracking
- **Quality**: Validation rule compliance
- **Schema**: Structure change detection

### Alerts

- **Data Delays**: Missing expected data loads
- **Quality Issues**: Validation failures
- **Schema Changes**: Unexpected structure modifications
- **Processing Errors**: Pipeline failures

## Performance

### Optimization Strategies

- **Parallel Processing**: Multi-threaded data processing
- **Compression**: Efficient storage formats (Parquet)
- **Partitioning**: Date-based data organization
- **Caching**: Intermediate result storage

### Scalability

- **Batch Size**: Configurable processing chunks
- **Memory Management**: Efficient data handling
- **Distributed Processing**: Spark integration ready
- **Cloud Resources**: Auto-scaling capabilities

## Dependencies

- pandas
- numpy
- boto3
- s3fs
- great-expectations (data quality)
- pyyaml

## Best Practices

- **Idempotency**: Safe to re-run processing
- **Logging**: Comprehensive operation logging
- **Error Handling**: Graceful failure recovery
- **Documentation**: Clear data lineage
- **Testing**: Automated quality checks
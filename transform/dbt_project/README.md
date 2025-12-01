# dbt Data Transformation Project

This dbt project transforms raw phishing threat intelligence data into a dimensional model for analytics and ML training.

## Overview

The dbt project implements a dimensional modeling approach with staging, marts, and metrics layers to support:
- ML model training data preparation
- Threat intelligence analytics
- Business intelligence reporting
- Data quality monitoring

## Project Structure

```
dbt_project/
├── models/
│   ├── staging/           # Raw data cleaning and standardization
│   │   ├── stg_events.sql
│   │   ├── stg_threat_features.sql
│   │   └── stg_users.sql
│   └── marts/            # Business logic and dimensional models
│       ├── dim_threat.sql
│       ├── dim_user.sql
│       ├── fact_events.sql
│       ├── fact_threat_matches.sql
│       └── metrics/      # Calculated metrics
│           ├── phishing_report_rate.sql
│           ├── product_efficacy_score.sql
│           └── threat_block_rate.sql
├── macros/               # Reusable SQL functions
├── tests/                # Data quality tests
├── seeds/                # Static reference data
└── docs/                 # Model documentation
```

## Data Models

### Staging Layer

**stg_events**: Standardized event data from raw logs
- Event deduplication and cleaning
- Timestamp standardization
- Data type conversions

**stg_threat_features**: Processed threat feature data
- Feature normalization
- Missing value handling
- Feature engineering transformations

**stg_users**: User dimension staging
- User attribute standardization
- Department and region mapping

### Marts Layer

**dim_threat**: Threat dimension table
- Threat categorization and severity
- Feature aggregations
- Threat intelligence enrichment

**dim_user**: User dimension table
- User demographics and attributes
- Department and organizational hierarchy
- Geographic information

**fact_events**: Event fact table
- Core event metrics and measures
- Foreign keys to dimension tables
- Aggregatable metrics

**fact_threat_matches**: Threat detection fact table
- ML model predictions and confidence scores
- Threat classification results
- Detection accuracy metrics

### Metrics Layer

**phishing_report_rate**: User reporting behavior metrics
**product_efficacy_score**: Overall product performance scoring
**threat_block_rate**: Threat blocking effectiveness metrics

## Configuration

### Profiles

The project supports multiple target environments:
- **dev**: Local development (PostgreSQL/DuckDB)
- **staging**: Staging environment (Athena)
- **prod**: Production environment (Athena)

### Sources

Data sources are configured in `models/sources.yml`:
- Raw event logs
- Threat intelligence feeds
- User directory data
- ML model outputs

## Data Quality

### Tests

- **Uniqueness**: Primary key constraints
- **Not Null**: Required field validation
- **Referential Integrity**: Foreign key relationships
- **Data Freshness**: Recency checks
- **Custom Tests**: Business logic validation

### Macros

Reusable functions for:
- Data quality checks
- Feature engineering
- Metric calculations
- Date/time utilities

## Usage

### Development

```bash
# Install dependencies
dbt deps

# Run models
dbt run

# Test data quality
dbt test

# Generate documentation
dbt docs generate
dbt docs serve
```

### Production Deployment

```bash
# Full refresh
dbt run --full-refresh

# Incremental updates
dbt run --models +fact_events

# Specific model selection
dbt run --select marts.metrics
```

## Dependencies

- dbt-core
- dbt-postgres (development)
- dbt-athena-community (production)

## Model Lineage

```
sources → staging → marts → metrics
   ↓         ↓        ↓        ↓
raw data → clean → business → KPIs
```

## Incremental Strategy

- **Events**: Append new records based on event timestamp
- **Dimensions**: Type 2 slowly changing dimensions
- **Metrics**: Daily aggregation with historical preservation

## Performance Optimization

- Partitioning by date for large fact tables
- Clustering on frequently filtered columns
- Materialization strategy optimization
- Query performance monitoring
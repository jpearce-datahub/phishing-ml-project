# dbt Transformation Layer

This dbt project transforms raw event data into a dimensional model optimized for analytics and reporting.

## Project Structure

```
dbt_project/
├── models/
│   ├── staging/          # Staging models (views)
│   │   ├── stg_events.sql
│   │   ├── stg_users.sql
│   │   └── stg_threat_features.sql
│   └── marts/            # Dimensional models (tables)
│       ├── dim_user.sql
│       ├── dim_threat.sql
│       ├── fact_events.sql
│       ├── fact_threat_matches.sql
│       └── metrics/
│           ├── threat_block_rate.sql
│           ├── phishing_report_rate.sql
│           └── product_efficacy_score.sql
├── tests/                # Custom data tests
├── macros/               # Reusable SQL macros
└── dbt_project.yml       # Project configuration
```

## Models

### Staging Layer

- **stg_events**: Cleans and standardizes raw event data
- **stg_users**: Extracts user dimension data
- **stg_threat_features**: Extracts threat feature data

### Dimensional Models

- **dim_user**: User dimension with aggregated metrics
- **dim_threat**: Threat dimension with severity classification
- **fact_events**: Fact table for event-level analysis
- **fact_threat_matches**: Aggregated threat match statistics

### Metrics Layer

- **threat_block_rate**: Daily threat detection rates
- **phishing_report_rate**: User-level phishing reporting metrics
- **product_efficacy_score**: Overall product performance score

## Usage

### Setup

1. Configure `profiles.yml` with your database credentials
2. Install dbt dependencies:
   ```bash
   dbt deps
   ```

### Run Models

```bash
# Run all models
dbt run

# Run specific model
dbt run --select stg_events

# Run models in staging
dbt run --select staging

# Run models in marts
dbt run --select marts
```

### Run Tests

```bash
# Run all tests
dbt test

# Test specific model
dbt test --select stg_events
```

### Generate Documentation

```bash
dbt docs generate
dbt docs serve
```

## Data Quality

All models include:
- Schema tests (unique, not_null, accepted_values)
- Data freshness tests
- Custom SQL tests
- Documentation

## Dependencies

- dbt-core >= 1.7.0
- dbt-postgres (for local development)
- dbt-athena-community (for AWS Athena)


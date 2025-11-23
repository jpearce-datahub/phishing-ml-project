# BI Dashboard

This directory contains dashboard files and configurations for visualizing threat intelligence metrics.

## Dashboard Components

### PowerBI

Create a PowerBI dashboard with the following visualizations:

1. **Threat Block Rate Over Time**
   - Line chart showing daily threat detection rates
   - Data source: `threat_block_rate` metric table

2. **User Risk Score Distribution**
   - Histogram of user risk scores
   - Data source: `dim_user` table

3. **Phishing Simulation Outcomes**
   - Stacked bar chart by department/region
   - Data source: `fact_events` joined with `dim_user`

4. **Threat Indicator Matches by Severity**
   - Pie chart or treemap
   - Data source: `dim_threat` table

5. **Product Performance KPIs**
   - Card visuals for key metrics
   - Data source: `product_efficacy_score` table

6. **Daily Trend Lines**
   - Multiple line chart for various metrics
   - Data source: Multiple metric tables

## Data Connection

### For PostgreSQL

```
Server: localhost
Database: phishing_ml
Schema: marts
Tables: dim_user, dim_threat, fact_events, threat_block_rate, etc.
```

### For AWS Athena

```
Data Source: AWS Athena
Database: phishing_ml_db
Workgroup: primary
Tables: dim_user, dim_threat, fact_events, etc.
```

## Dashboard Queries

### Threat Block Rate

```sql
SELECT 
    event_date,
    threat_block_rate_pct,
    threats_detected,
    total_events
FROM marts.threat_block_rate
ORDER BY event_date DESC
```

### User Metrics

```sql
SELECT 
    user_id,
    department,
    region,
    total_events,
    phishing_rate_pct
FROM marts.dim_user
ORDER BY phishing_rate_pct DESC
```

### Product Efficacy

```sql
SELECT 
    event_date,
    product_efficacy_score,
    detection_rate,
    high_severity_rate
FROM marts.product_efficacy_score
ORDER BY event_date DESC
```

## Looker Integration

For Looker, create a LookML project with:

- Explores for each fact/dimension table
- Pre-built dashboards
- Custom metrics using LookML

## QuickSight Integration

1. Connect to Athena data source
2. Import dbt-generated tables
3. Create visualizations
4. Set up scheduled refreshes

## Refresh Schedule

- **Real-time**: API metrics (via API calls)
- **Hourly**: Fact tables
- **Daily**: Dimension tables and metrics
- **Weekly**: ML model retraining

## Custom Metrics

Add custom calculations in your BI tool:

- **Threat Detection Accuracy**: (True Positives) / (True Positives + False Positives)
- **User Engagement Score**: Based on event frequency and reporting rate
- **Department Risk Ranking**: Aggregated by department


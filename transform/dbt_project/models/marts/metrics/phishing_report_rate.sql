{{ config(materialized='table') }}

with user_metrics as (
    select
        user_id,
        department,
        region,
        count(*) as total_events,
        sum(case when is_phishing = 1 then 1 else 0 end) as phishing_events,
        sum(case when event_type = 'threat_detected' then 1 else 0 end) as reported_events
    from {{ ref('fact_events') }}
    group by 1, 2, 3
)

select
    user_id,
    department,
    region,
    total_events,
    phishing_events,
    reported_events,
    round(100.0 * phishing_events / nullif(total_events, 0), 2) as phishing_rate_pct,
    round(100.0 * reported_events / nullif(phishing_events, 0), 2) as report_rate_pct,
    current_timestamp as dbt_updated_at
from user_metrics
where total_events > 0


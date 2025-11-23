{{ config(materialized='table') }}

with efficacy_metrics as (
    select
        event_date,
        count(*) as total_events,
        sum(case when is_phishing = 1 then 1 else 0 end) as threats_detected,
        sum(case when threat_severity = 'high' then 1 else 0 end) as high_severity_detected,
        sum(case when threat_severity = 'medium' then 1 else 0 end) as medium_severity_detected,
        sum(case when threat_severity = 'low' then 1 else 0 end) as low_severity_detected,
        count(distinct user_id) as active_users,
        count(distinct threat_id) as unique_threats
    from {{ ref('fact_events') }}
    group by 1
)

select
    event_date,
    total_events,
    threats_detected,
    high_severity_detected,
    medium_severity_detected,
    low_severity_detected,
    active_users,
    unique_threats,
    round(100.0 * threats_detected / nullif(total_events, 0), 2) as detection_rate,
    round(100.0 * high_severity_detected / nullif(threats_detected, 0), 2) as high_severity_rate,
    -- Efficacy score: weighted combination of detection rate and high-severity catch rate
    round(
        (100.0 * threats_detected / nullif(total_events, 0)) * 0.6 +
        (100.0 * high_severity_detected / nullif(threats_detected, 0)) * 0.4,
        2
    ) as product_efficacy_score,
    current_timestamp as dbt_updated_at
from efficacy_metrics
order by event_date desc


{{ config(materialized='table') }}

with daily_metrics as (
    select
        event_date,
        count(*) as total_events,
        sum(case when is_phishing = 1 then 1 else 0 end) as threats_detected,
        sum(case when is_phishing = 0 then 1 else 0 end) as legitimate_events,
        count(distinct user_id) as unique_users,
        count(distinct threat_id) as unique_threats
    from {{ ref('fact_events') }}
    group by 1
)

select
    event_date,
    total_events,
    threats_detected,
    legitimate_events,
    unique_users,
    unique_threats,
    round(100.0 * threats_detected / nullif(total_events, 0), 2) as threat_block_rate_pct,
    round(100.0 * legitimate_events / nullif(total_events, 0), 2) as legitimate_rate_pct,
    current_timestamp as dbt_updated_at
from daily_metrics
order by event_date desc


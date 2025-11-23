{{ config(materialized='table') }}

with threat_events as (
    select
        threat_id,
        event_date,
        count(*) as event_count,
        count(distinct user_id) as unique_users,
        sum(case when is_phishing = 1 then 1 else 0 end) as phishing_count,
        sum(case when is_phishing = 0 then 1 else 0 end) as legitimate_count
    from {{ ref('fact_events') }}
    group by 1, 2
)

select
    threat_id,
    event_date,
    event_count,
    unique_users,
    phishing_count,
    legitimate_count,
    round(100.0 * phishing_count / nullif(event_count, 0), 2) as phishing_rate_pct,
    current_timestamp as dbt_updated_at
from threat_events


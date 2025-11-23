{{ config(materialized='table') }}

with user_data as (
    select
        user_id,
        department,
        region,
        role,
        count(*) as total_events,
        sum(case when is_phishing = 1 then 1 else 0 end) as phishing_events,
        min(event_timestamp) as first_seen,
        max(event_timestamp) as last_seen
    from {{ ref('stg_events') }}
    group by 1, 2, 3, 4
)

select
    user_id,
    department,
    region,
    role,
    total_events,
    phishing_events,
    round(100.0 * phishing_events / nullif(total_events, 0), 2) as phishing_rate_pct,
    first_seen,
    last_seen,
    current_timestamp as dbt_updated_at
from user_data


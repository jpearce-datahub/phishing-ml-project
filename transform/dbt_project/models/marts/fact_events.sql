{{ config(materialized='table') }}

with events as (
    select
        e.event_id,
        e.user_id,
        e.threat_id,
        e.event_timestamp,
        e.event_date,
        e.event_type,
        e.is_phishing,
        e.department,
        e.region,
        e.role,
        t.threat_severity,
        t.url_length,
        t.has_https,
        t.has_ip_address,
        t.abnormal_form_action,
        t.iframe_or_frame,
        t.right_click_disabled
    from {{ ref('stg_events') }} e
    left join {{ ref('dim_threat') }} t
        on e.threat_id = t.threat_id
)

select
    event_id,
    user_id,
    threat_id,
    event_timestamp,
    event_date,
    event_type,
    is_phishing,
    department,
    region,
    role,
    threat_severity,
    url_length,
    has_https,
    has_ip_address,
    abnormal_form_action,
    iframe_or_frame,
    right_click_disabled,
    case
        when is_phishing = 1 then 1
        else 0
    end as threat_detected_flag,
    current_timestamp as dbt_updated_at
from events


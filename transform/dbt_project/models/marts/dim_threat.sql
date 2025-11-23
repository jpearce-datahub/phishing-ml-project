{{ config(materialized='table') }}

with threat_data as (
    select
        threat_id,
        url_length,
        num_dots,
        subdomain_level,
        path_level,
        has_https,
        has_ip_address,
        num_sensitive_words,
        has_random_string,
        hostname_length,
        path_length,
        query_length,
        pct_ext_hyperlinks,
        pct_ext_resource_urls,
        abnormal_form_action,
        iframe_or_frame,
        missing_title,
        right_click_disabled,
        popup_window,
        is_phishing,
        case
            when is_phishing = 1 and (
                has_ip_address = 1 or
                abnormal_form_action = 1 or
                iframe_or_frame = 1 or
                right_click_disabled = 1
            ) then 'high'
            when is_phishing = 1 then 'medium'
            else 'low'
        end as threat_severity
    from {{ ref('stg_threat_features') }}
)

select
    threat_id,
    url_length,
    num_dots,
    subdomain_level,
    path_level,
    has_https,
    has_ip_address,
    num_sensitive_words,
    has_random_string,
    hostname_length,
    path_length,
    query_length,
    pct_ext_hyperlinks,
    pct_ext_resource_urls,
    abnormal_form_action,
    iframe_or_frame,
    missing_title,
    right_click_disabled,
    popup_window,
    is_phishing,
    threat_severity,
    current_timestamp as dbt_updated_at
from threat_data


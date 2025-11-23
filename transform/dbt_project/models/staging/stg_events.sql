{{ config(materialized='view') }}

with source_data as (
    select
        event_id,
        user_id,
        timestamp::timestamp as event_timestamp,
        event_type,
        threat_id,
        is_phishing,
        metadata->>'url_length'::integer as url_length,
        metadata->>'num_dots'::integer as num_dots,
        metadata->>'subdomain_level'::integer as subdomain_level,
        metadata->>'path_level'::integer as path_level,
        metadata->>'has_https'::integer as has_https,
        metadata->>'has_ip_address'::integer as has_ip_address,
        metadata->>'num_sensitive_words'::integer as num_sensitive_words,
        metadata->>'has_random_string'::integer as has_random_string,
        metadata->>'hostname_length'::integer as hostname_length,
        metadata->>'path_length'::integer as path_length,
        metadata->>'query_length'::integer as query_length,
        metadata->>'pct_ext_hyperlinks'::float as pct_ext_hyperlinks,
        metadata->>'pct_ext_resource_urls'::float as pct_ext_resource_urls,
        metadata->>'abnormal_form_action'::integer as abnormal_form_action,
        metadata->>'iframe_or_frame'::integer as iframe_or_frame,
        metadata->>'missing_title'::integer as missing_title,
        metadata->>'right_click_disabled'::integer as right_click_disabled,
        metadata->>'popup_window'::integer as popup_window,
        user_metadata->>'department' as department,
        user_metadata->>'region' as region,
        user_metadata->>'role' as role,
        date(timestamp::timestamp) as event_date
    from {{ source('raw', 'events') }}
    where timestamp is not null
)

select * from source_data


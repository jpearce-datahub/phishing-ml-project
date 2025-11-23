{{ config(materialized='view') }}

with source_data as (
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
        is_phishing
    from {{ ref('stg_events') }}
    where threat_id is not null
)

select * from source_data


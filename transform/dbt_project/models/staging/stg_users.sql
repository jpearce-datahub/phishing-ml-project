{{ config(materialized='view') }}

with source_data as (
    select distinct
        user_id,
        department,
        region,
        role
    from {{ ref('stg_events') }}
)

select * from source_data


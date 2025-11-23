-- Test: Ensure no null event_ids in fact_events
select count(*) as null_count
from {{ ref('fact_events') }}
where event_id is null

-- Expected: 0


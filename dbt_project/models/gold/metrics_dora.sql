with merged_prs as (
    select
        repo,
        pr_number,
        created_at,
        merged_at,
        datediff(hour, created_at, merged_at) as lead_time_hours
    from {{ ref('silver_pull_requests') }}
    where merged_at is not null
)

select
    repo,
    count(*) as merged_pr_count,
    avg(cast(lead_time_hours as float)) as avg_lead_time_hours,
    min(lead_time_hours) as min_lead_time_hours,
    max(lead_time_hours) as max_lead_time_hours,
    cast(getutcdate() as datetime2) as evaluated_at
from merged_prs
group by repo

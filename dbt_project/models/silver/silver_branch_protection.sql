with bronze as (
    select * from {{ ref('bronze_github_events') }}
    where message_type = 'branch_protection'
),

deduplicated as (
    select
        repo,
        scraped_at,
        payload,
        row_number() over (
            partition by repo
            order by scraped_at desc
        ) as rn
    from bronze
)

select
    repo,
    case when json_value(payload, '$.required_pull_request_reviews') is not null
         then 1 else 0 end as requires_pr_reviews,
    case when json_value(payload, '$.enforce_admins.enabled') = 'true'
         then 1 else 0 end as enforces_admins
from deduplicated
where rn = 1

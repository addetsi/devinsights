with prs as (
    select * from {{ ref('silver_pull_requests') }}
),

repo_pr_stats as (
    select
        repo,
        count(*) as total_prs,
        count(case when state = 'closed' then 1 end) as closed_prs
    from prs
    group by repo
)

select
    repo,
    total_prs,
    closed_prs,
    case
        when total_prs > 0 then 'PASS'
        else 'FAIL'
    end as has_pr_activity,
    cast(getutcdate() as datetime2) as evaluated_at
from repo_pr_stats

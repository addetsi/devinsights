with repos as (
    select * from {{ ref('silver_repos') }}
),

pr_stats as (
    select
        repo,
        count(*) as total_prs,
        count(case when state = 'open' then 1 end) as open_prs
    from {{ ref('silver_pull_requests') }}
    group by repo
)

select
    r.repo,
    r.stars,
    r.forks,
    r.language,
    r.open_issues,
    coalesce(p.total_prs, 0) as total_prs,
    coalesce(p.open_prs, 0) as open_prs,
    r.scraped_at
from repos r
left join pr_stats p on r.repo = p.repo

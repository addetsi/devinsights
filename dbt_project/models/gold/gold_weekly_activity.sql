with commits as (
    select
        repo,
        datefromparts(year(commit_date), month(commit_date), 1) as month_bucket,
        datepart(year, commit_date) as yr,
        datepart(week, commit_date) as wk,
        commit_date
    from {{ ref('silver_commits') }}
    where commit_date is not null
),

weekly_commits as (
    select
        repo,
        yr,
        wk,
        count(*) as commits_per_week
    from commits
    group by repo, yr, wk
),

weekly_prs as (
    select
        repo,
        datepart(year, created_at) as yr,
        datepart(week, created_at) as wk,
        count(*) as prs_opened_per_week
    from {{ ref('silver_pull_requests') }}
    where created_at is not null
    group by repo, datepart(year, created_at), datepart(week, created_at)
)

select
    coalesce(c.repo, p.repo) as repo,
    coalesce(c.yr, p.yr) as yr,
    coalesce(c.wk, p.wk) as wk,
    coalesce(c.commits_per_week, 0) as commits_per_week,
    coalesce(p.prs_opened_per_week, 0) as prs_opened_per_week
from weekly_commits c
full outer join weekly_prs p
    on c.repo = p.repo and c.yr = p.yr and c.wk = p.wk

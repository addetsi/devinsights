with releases as (
    select
        repo,
        published_at,
        datepart(year, published_at) as yr,
        datepart(week, published_at) as wk
    from {{ ref('silver_releases') }}
    where published_at is not null
)

select
    repo,
    count(*) as total_releases,
    count(distinct concat(yr, '-', wk)) as active_weeks,
    cast(count(*) as float) / nullif(count(distinct concat(yr, '-', wk)), 0) as releases_per_active_week,
    max(published_at) as latest_release,
    cast(getutcdate() as datetime2) as evaluated_at
from releases
group by repo

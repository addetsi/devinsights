with bronze as (
    select * from {{ ref('bronze_github_events') }}
    where message_type = 'repo'
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
    cast(scraped_at as datetime2) as scraped_at,
    cast(json_value(payload, '$.stargazers_count') as int) as stars,
    cast(json_value(payload, '$.forks_count') as int) as forks,
    json_value(payload, '$.language') as language,
    json_value(payload, '$.default_branch') as default_branch,
    cast(json_value(payload, '$.open_issues_count') as int) as open_issues
from deduplicated
where rn = 1

with bronze as (
    select * from {{ ref('bronze_github_events') }}
    where message_type = 'pull_request'
),

deduplicated as (
    select
        repo,
        scraped_at,
        payload,
        json_value(payload, '$.number') as pr_number,
        row_number() over (
            partition by repo, json_value(payload, '$.number')
            order by scraped_at desc
        ) as rn
    from bronze
)

select
    repo,
    cast(pr_number as int) as pr_number,
    json_value(payload, '$.state') as state,
    json_value(payload, '$.user.login') as author,
    cast(json_value(payload, '$.created_at') as datetime2) as created_at,
    try_cast(json_value(payload, '$.merged_at') as datetime2) as merged_at,
    cast(scraped_at as datetime2) as scraped_at
from deduplicated
where rn = 1

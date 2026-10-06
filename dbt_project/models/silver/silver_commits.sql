with bronze as (
    select * from {{ ref('bronze_github_events') }}
    where message_type = 'commit'
),

deduplicated as (
    select
        repo,
        scraped_at,
        payload,
        json_value(payload, '$.sha') as sha,
        row_number() over (
            partition by repo, json_value(payload, '$.sha')
            order by scraped_at desc
        ) as rn
    from bronze
)

select
    repo,
    sha,
    json_value(payload, '$.commit.author.name') as author,
    try_cast(json_value(payload, '$.commit.author.date') as datetime2) as commit_date
from deduplicated
where rn = 1

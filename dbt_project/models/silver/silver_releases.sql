with bronze as (
    select * from {{ ref('bronze_github_events') }}
    where message_type = 'release'
),

deduplicated as (
    select
        repo,
        scraped_at,
        payload,
        json_value(payload, '$.id') as release_id,
        row_number() over (
            partition by repo, json_value(payload, '$.id')
            order by scraped_at desc
        ) as rn
    from bronze
)

select
    repo,
    cast(release_id as bigint) as release_id,
    json_value(payload, '$.tag_name') as tag_name,
    try_cast(json_value(payload, '$.published_at') as datetime2) as published_at
from deduplicated
where rn = 1

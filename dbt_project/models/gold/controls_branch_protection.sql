select
    repo,
    requires_pr_reviews,
    enforces_admins,
    case when requires_pr_reviews = 1 then 'PASS' else 'FAIL' end as branch_protection_status,
    cast(getutcdate() as datetime2) as evaluated_at
from {{ ref('silver_branch_protection') }}

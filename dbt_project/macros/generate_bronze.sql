{% macro generate_bronze(table_name) %}

{%- set table_config = var('bronze_tables')[table_name] -%}
{%- set source_name = table_config['source_name'] -%}
{%- set columns = table_config['columns'] -%}

with source as (
    select * from {{ source(source_name, table_name)}}
)

select
{% for col in columns %}
    {{ col }}{% if not loop.last %}, {% endif %}
{% endfor %}
from source

{% endmacro %}

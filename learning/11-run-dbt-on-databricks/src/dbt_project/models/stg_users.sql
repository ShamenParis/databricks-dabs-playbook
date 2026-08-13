{{ config(materialized='table') }}

SELECT
    id,
    name,
    current_timestamp() AS processed_at
FROM main.demo.raw_dbt_users
WHERE status = 'active'
{{ config(materialized='table') }}

WITH date_series AS (
    SELECT 
        generate_series(
            (SELECT MIN(DATE(message_timestamp)) FROM {{ ref('stg_telegram_messages') }})::date,
            (SELECT MAX(DATE(message_timestamp)) FROM {{ ref('stg_telegram_messages') }})::date + INTERVAL '30 days',
            '1 day'::interval
        ) as date
)

SELECT
    -- Create date key as YYYYMMDD integer
    EXTRACT(YEAR FROM date)::integer * 10000 + 
    EXTRACT(MONTH FROM date)::integer * 100 + 
    EXTRACT(DAY FROM date)::integer as date_key,
    
    date as full_date,
    EXTRACT(DOW FROM date)::integer as day_of_week,
    TO_CHAR(date, 'Day') as day_name,
    EXTRACT(WEEK FROM date)::integer as week_of_year,
    EXTRACT(MONTH FROM date)::integer as month,
    TO_CHAR(date, 'Month') as month_name,
    EXTRACT(QUARTER FROM date)::integer as quarter,
    EXTRACT(YEAR FROM date)::integer as year,
    CASE WHEN EXTRACT(DOW FROM date) IN (0, 6) THEN TRUE ELSE FALSE END as is_weekend,
    
    CURRENT_TIMESTAMP as loaded_at

FROM date_series
ORDER BY date
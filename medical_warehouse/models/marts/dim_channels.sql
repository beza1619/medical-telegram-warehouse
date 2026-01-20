{{ config(materialized='table') }}

WITH channel_stats AS (
    SELECT 
        channel_name,
        COUNT(*) as total_posts,
        AVG(views) as avg_views,
        SUM(CASE WHEN has_media THEN 1 ELSE 0 END) as posts_with_images,
        MIN(message_timestamp) as first_post_date,
        MAX(message_timestamp) as last_post_date
    FROM {{ ref('stg_telegram_messages') }}
    GROUP BY channel_name
)

SELECT 
    -- Generate surrogate key (simple hash for SQLite compatibility)
    ABS(HASH(channel_name)) as channel_key,
    channel_name,
    CASE 
        WHEN channel_name LIKE '%pharma%' THEN 'Pharmaceutical'
        WHEN channel_name LIKE '%cosmetic%' THEN 'Cosmetics' 
        ELSE 'Medical'
    END as channel_type,
    total_posts,
    ROUND(avg_views, 2) as avg_views,
    posts_with_images,
    first_post_date,
    last_post_date,
    CURRENT_TIMESTAMP as loaded_at
FROM channel_stats
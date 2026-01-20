{{ config(materialized='table') }}

WITH messages_with_keys AS (
    SELECT 
        m.message_id,
        ABS(HASH(m.channel_name)) as channel_key,
        DATE(m.message_timestamp) as message_date,
        m.message_text,
        LENGTH(TRIM(m.message_text)) as message_length,
        m.views as view_count,
        m.forwards as forward_count,
        m.has_media,
        m.image_path,
        m.message_timestamp,
        m.scraped_at
    FROM {{ ref('stg_telegram_messages') }} m
)

SELECT 
    message_id,
    channel_key,
    message_date,
    message_text,
    message_length,
    view_count,
    forward_count,
    has_media,
    image_path,
    message_timestamp,
    scraped_at,
    CURRENT_TIMESTAMP as loaded_at
FROM messages_with_keys
WHERE message_text IS NOT NULL
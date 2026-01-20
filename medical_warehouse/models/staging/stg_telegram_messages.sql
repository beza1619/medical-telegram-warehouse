{{ config(materialized='view') }}

SELECT 
    message_id,
    channel_name,
    -- Convert string date to timestamp
    CASE 
        WHEN message_date LIKE '%T%' THEN CAST(message_date AS TIMESTAMP)
        ELSE CAST(message_date || 'T00:00:00' AS TIMESTAMP)
    END as message_timestamp,
    message_text,
    CASE WHEN has_media = 1 THEN TRUE ELSE FALSE END as has_media,
    views,
    forwards,
    image_path,
    scraped_at
FROM {{ source('raw', 'telegram_messages') }}
WHERE message_text IS NOT NULL 
  AND TRIM(message_text) != ''
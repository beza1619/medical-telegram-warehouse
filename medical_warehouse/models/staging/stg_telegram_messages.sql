{{ config(materialized='view') }}

WITH raw_data AS (
    SELECT 
        message_id,
        channel_name,
        -- Convert string date to timestamp
        CASE 
            WHEN message_date LIKE '%T%' THEN datetime(message_date)
            ELSE datetime(message_date || 'T00:00:00')
        END as message_datetime,
        message_text,
        has_media,
        views,
        forwards,
        image_path,
        scraped_at
    FROM main.raw_telegram_messages
)

SELECT 
    message_id,
    channel_name,
    message_datetime,
    DATE(message_datetime) as message_date,
    message_text,
    -- Clean message text
    TRIM(message_text) as cleaned_text,
    LENGTH(TRIM(message_text)) as message_length,
    has_media,
    views,
    forwards,
    image_path,
    scraped_at
FROM raw_data
WHERE message_text IS NOT NULL 
  AND TRIM(message_text) != ''
-- Test: No messages should have future dates
SELECT 
    message_id,
    channel_name,
    message_timestamp
FROM {{ ref('stg_telegram_messages') }}
WHERE message_timestamp > CURRENT_TIMESTAMP
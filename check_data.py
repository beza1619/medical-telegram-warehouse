import sqlite3
import pandas as pd

conn = sqlite3.connect('medical_warehouse.db')

# Show first 5 messages
print("=== First 5 Messages ===")
df = pd.read_sql_query("SELECT * FROM raw_telegram_messages LIMIT 5", conn)
print(df[['message_id', 'channel_name', 'views', 'has_media']])

# Show summary
print("\n=== Summary by Channel ===")
summary = pd.read_sql_query("""
    SELECT 
        channel_name,
        COUNT(*) as total_messages,
        AVG(views) as avg_views,
        SUM(has_media) as messages_with_images
    FROM raw_telegram_messages
    GROUP BY channel_name
""", conn)
print(summary)

conn.close()
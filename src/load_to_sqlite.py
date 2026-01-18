import json
import os
import sqlite3

def load_json_to_sqlite():
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('medical_warehouse.db')
        cursor = conn.cursor()
        
        # Create table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw_telegram_messages (
            message_id INTEGER PRIMARY KEY,
            channel_name TEXT,
            message_date TEXT,
            message_text TEXT,
            has_media INTEGER,
            views INTEGER,
            forwards INTEGER,
            image_path TEXT,
            scraped_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """)
        print("✅ Created raw_telegram_messages table")
        
        # Load JSON files
        json_dir = "data/raw/telegram_messages"
        total_loaded = 0
        
        # Check if directory exists
        if not os.path.exists(json_dir):
            print(f"❌ Directory not found: {json_dir}")
            print("Current working directory:", os.getcwd())
            print("Available in data/raw/:", os.listdir("data/raw/") if os.path.exists("data/raw/") else "No data/raw folder")
            return
        
        # List all date folders
        for date_folder in os.listdir(json_dir):
            date_path = os.path.join(json_dir, date_folder)
            
            if os.path.isdir(date_path):
                print(f"📁 Processing date: {date_folder}")
                
                for json_file in os.listdir(date_path):
                    if json_file.endswith('.json'):
                        file_path = os.path.join(date_path, json_file)
                        print(f"   📂 Loading: {json_file}")
                        
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                messages = json.load(f)
                                
                            for msg in messages:
                                cursor.execute("""
                                INSERT OR IGNORE INTO raw_telegram_messages 
                                (message_id, channel_name, message_date, message_text, 
                                 has_media, views, forwards, image_path)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                                """, (
                                    msg['message_id'],
                                    msg['channel_name'],
                                    msg['message_date'],
                                    msg['message_text'],
                                    1 if msg['has_media'] else 0,
                                    msg['views'],
                                    msg['forwards'],
                                    msg['image_path']
                                ))
                                total_loaded += 1
                                
                        except Exception as e:
                            print(f"   ❌ Error loading {json_file}: {e}")
        
        conn.commit()
        conn.close()
        
        if total_loaded > 0:
            print(f"✅ Successfully loaded {total_loaded} messages to medical_warehouse.db")
        else:
            print("⚠️ No messages were loaded. Check your data directory.")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    load_json_to_sqlite()
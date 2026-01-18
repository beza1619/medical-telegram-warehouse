import asyncio
from telethon import TelegramClient
import os
from dotenv import load_dotenv

load_dotenv()

async def main():
    client = TelegramClient(
        'test_session',
        int(os.getenv('TELEGRAM_API_ID')),
        os.getenv('TELEGRAM_API_HASH')
    )
    
    await client.start()
    print("✅ Connection successful! Telegram client is ready.")
    print(f"Logged in as: {await client.get_me()}")
    await client.disconnect()

asyncio.run(main())
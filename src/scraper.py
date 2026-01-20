import asyncio
import json
import os
from datetime import datetime
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TelegramScraper:
    def __init__(self):
        self.api_id = int(os.getenv('TELEGRAM_API_ID'))
        self.api_hash = os.getenv('TELEGRAM_API_HASH')
        self.client = None
        
    async def start_client(self):
        """Initialize Telegram client"""
        self.client = TelegramClient('scraper_session', self.api_id, self.api_hash)
        await self.client.start()
        logger.info("Telegram client started successfully")
        
    async def scrape_channel(self, channel_username, limit=10):
        """Scrape messages from a channel"""
        messages_data = []
        
        try:
    
   async def scrape_channel(self, channel_username, limit=50):
    """Scrape messages from a channel with detailed logging"""
    messages_data = []
    
    try:
        logger.info(f"START scraping channel: {channel_username}", extra={'channel': channel_username})
        
        async for message in self.client.iter_messages(channel_username, limit=limit):
            # ... existing message processing code ...
            
        logger.info(f"COMPLETE scraped {len(messages_data)} messages from {channel_username}", 
                   extra={'channel': channel_username})
        
    except Exception as e:
        error_type = type(e).__name__
        logger.error(f"FAILED scraping {channel_username}: {error_type} - {str(e)}", 
                    extra={'channel': channel_username})
        
    return messages_data
    
    async def run_scraping(self):
        """Main scraping function"""
        await self.start_client()
        
        # Channels to scrape
    channels = [
    'lobelia4cosmetics',    # Existing
    'tikvahpharma',         # Existing
    'CheMed123',            # Missing - Add this
    'ethiopharma',          # Ethiopian pharmacy channel
    'pharmacyaddis',        # Ethiopian channel
    'addispharmacy'         # Ethiopian channel
]
        
        for channel in channels:
            logger.info(f"Starting to scrape: {channel}")
            messages = await self.scrape_channel(channel, limit=10)  # Start with 10
            if messages:
                self.save_to_json(messages, channel)
            await asyncio.sleep(2)  # Avoid rate limiting
        
        await self.client.disconnect()
        logger.info("Scraping completed!")

async def main():
    scraper = TelegramScraper()
    await scraper.run_scraping()

if __name__ == "__main__":
    asyncio.run(main())
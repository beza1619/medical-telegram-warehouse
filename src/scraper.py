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
            async for message in self.client.iter_messages(channel_username, limit=limit):
                message_info = {
                    'message_id': message.id,
                    'channel_name': channel_username,
                    'message_date': message.date.isoformat() if message.date else None,
                    'message_text': message.text or '',
                    'has_media': message.media is not None,
                    'views': message.views or 0,
                    'forwards': message.forwards or 0,
                    'image_path': None
                }
                
                # Download image if available
                if message.media and isinstance(message.media, MessageMediaPhoto):
                    image_path = await self.download_image(message, channel_username)
                    message_info['image_path'] = image_path
                
                messages_data.append(message_info)
                logger.info(f"Scraped message {message.id} from {channel_username}")
                
        except Exception as e:
            logger.error(f"Error scraping {channel_username}: {str(e)}")
            
        return messages_data
    
    async def download_image(self, message, channel_name):
        """Download image from message"""
        try:
            date_str = datetime.now().strftime('%Y-%m-%d')
            image_dir = f"data/raw/images/{channel_name}/{date_str}"
            os.makedirs(image_dir, exist_ok=True)
            
            image_path = f"{image_dir}/{message.id}.jpg"
            await message.download_media(file=image_path)
            logger.info(f"Downloaded image: {image_path}")
            return image_path
            
        except Exception as e:
            logger.error(f"Failed to download image: {str(e)}")
            return None
    
    def save_to_json(self, messages, channel_name):
        """Save scraped data to JSON file"""
        try:
            date_str = datetime.now().strftime('%Y-%m-%d')
            json_dir = f"data/raw/telegram_messages/{date_str}"
            os.makedirs(json_dir, exist_ok=True)
            
            file_path = f"{json_dir}/{channel_name}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(messages, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Saved {len(messages)} messages to {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Failed to save JSON: {str(e)}")
            return None
    
    async def run_scraping(self):
        """Main scraping function"""
        await self.start_client()
        
        # Channels to scrape
        channels = ['lobelia4cosmetics', 'tikvahpharma']
        
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
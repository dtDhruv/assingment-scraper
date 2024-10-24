import telegram
import os
import asyncio
from dotenv import load_dotenv
from new_assignment_scrape import ads_assignment_scrape
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()

scheduler = AsyncIOScheduler(timezone="UTC")

BOT_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = telegram.Bot(token=BOT_TOKEN)

async def send_message():
    latest_assignmnet = ads_assignment_scrape()
    await bot.send_message(chat_id=CHAT_ID, text=latest_assignmnet)
    print("Message sent!")

def main():
    scheduler.add_job(send_message, 'interval', hours=12)

    try:
        scheduler.start()
        print("Scheduler started")
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Scheduler stopped")

if __name__ == "__main__":
    main()
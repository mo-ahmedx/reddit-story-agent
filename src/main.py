import asyncio
import logging
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from reddit import RedditScraper
from scorer import DramaScorer
from database import db_manager
from telegram_bot import TelegramNotifier

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

scraper = RedditScraper()
scorer = DramaScorer()
notifier = TelegramNotifier()

async def job():
    logging.info("Starting Scraping Cycle...")
    await db_manager.connect()
    
    try:
        stories = scraper.get_hot_stories()
        logging.info(f"Found {len(stories)} stories meeting threshold.")

        for story in stories:
            # Check if already processed
            if await db_manager.is_story_processed(story['id']):
                continue

            logging.info(f"Analyzing: {story['title'][:50]}...")
            
            # Analyze with AI
            analysis = await scorer.analyze_story(story['title'], story['body'])
            
            # Filter: Only send if Drama Score >= 7
            if analysis.get('score', 0) >= 7:
                await notifier.send_alert(story, analysis)
                await db_manager.save_story(
                    reddit_id=story['id'],
                    title=story['title'],
                    score=analysis['score'],
                    subreddit=story['subreddit'],
                    url=story['url']
                )
                logging.info(f"Sent high-potential story: {story['id']}")
            else:
                # Log it in DB anyway so we don't scan it again
                await db_manager.save_story(
                    reddit_id=story['id'],
                    title=story['title'],
                    score=analysis['score'],
                    subreddit=story['subreddit'],
                    url=story['url']
                )

    except Exception as e:
        logging.error(f"Error in main loop: {e}")
    finally:
        await db_manager.disconnect()

def run_sync_job():
    asyncio.run(job())

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    # Initial run
    run_sync_job()
    # Schedule every 6 hours
    scheduler.add_job(run_sync_job, 'interval', hours=6)
    
    logging.info("Story Arc Bot Started. Frequency: 6 Hours.")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
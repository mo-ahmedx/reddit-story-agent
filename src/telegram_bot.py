import os
from telegram import Bot
from telegram.constants import ParseMode
from dotenv import load_dotenv

load_dotenv()

class TelegramNotifier:
    def __init__(self):
        self.bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

    async def send_alert(self, story_data, analysis):
        archetypes_str = ", ".join(analysis.get("archetypes", ["Unknown"]))
        
        message = (
            f"🚨 **NEW STORY ARC ALERT** 🚨\n\n"
            f"📍 **Subreddit:** r/{story_data['subreddit']}\n"
            f"🔥 **Drama Score:** {analysis['score']}/10\n"
            f"📖 **Title:** {story_data['title']}\n\n"
            f"🎭 **Archetypes:** {archetypes_str}\n"
            f"📝 **Summary:** {analysis.get('summary', 'No summary provided.')}\n\n"
            f"🔗 **Link:** [Read on Reddit]({story_data['url']})"
        )

        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=False
            )
        except Exception as e:
            print(f"Telegram Error: {e}")
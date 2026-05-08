import os
from prisma import Prisma

# Wrapper to handle database connection and fallbacks
class DatabaseManager:
    def __init__(self):
        # Neon usually requires ?sslmode=require. 
        # If DATABASE_URL is missing, Prisma will use the one in .env or throw an error.
        self.db = Prisma()

    async def connect(self):
        if not self.db.is_connected():
            await self.db.connect()

    async def disconnect(self):
        if self.db.is_connected():
            await self.db.disconnect()

    async def is_story_processed(self, reddit_id: str) -> bool:
        story = await self.db.sentstory.find_unique(where={"reddit_id": reddit_id})
        return story is not None

    async def save_story(self, reddit_id: str, title: str, score: int, subreddit: str, url: str):
        await self.db.sentstory.create(
            data={
                "reddit_id": reddit_id,
                "title": title,
                "score": score,
                "subreddit": subreddit,
                "url": url
            }
        )

db_manager = DatabaseManager()
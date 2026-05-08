import os
import praw
from dotenv import load_dotenv

load_dotenv()

class RedditScraper:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent="StoryArcBot/1.0 by /u/YourUsername",
        )
        self.subreddits = [
            "AmITheAsshole", "relationship_advice", "tifu", 
            "confessions", "legaladvice", "Marriage", 
            "parenting", "trueoffmychest"
        ]

    def get_hot_stories(self):
        target_subs = "+".join(self.subreddits)
        posts = self.reddit.subreddit(target_subs).hot(limit=50)
        
        filtered_posts = []
        for post in posts:
            # Criteria: 500+ Upvotes, 50+ Comments, 300+ chars, No META
            if (post.score >= 500 and 
                post.num_comments >= 50 and 
                len(post.selftext) >= 300 and 
                "[META]" not in post.title.upper()):
                
                filtered_posts.append({
                    "id": post.id,
                    "title": post.title,
                    "body": post.selftext,
                    "url": post.full_link if hasattr(post, 'full_link') else f"https://reddit.com{post.permalink}",
                    "subreddit": post.subreddit.display_name
                })
        return filtered_posts
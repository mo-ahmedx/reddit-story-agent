import os
import json
import time
import logging
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class DramaScorer:
    def __init__(self):
        # Initialize the new GenAI Client
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_id = "gemini-1.5-flash"
        
        self.persona = (
            "You are a drama analyst for a YouTube storytelling channel. "
            "Rate the following Reddit post for its drama and storytelling potential on a scale of 1 to 10. "
            "Respond ONLY in valid JSON format with keys: 'score' (int), 'archetypes' (list of strings), 'summary' (string)."
        )

    async def analyze_story(self, title, body):
        # 15 requests per minute throttle (staying safe with 5 seconds)
        time.sleep(5) 
        
        prompt = f"{self.persona}\n\nTitle: {title}\nStory: {body}"
        
        try:
            # New SDK call format
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            # The new SDK returns text directly or via parsed methods
            return json.loads(response.text)
            
        except Exception as e:
            logging.error(f"Gemini API Error: {e}")
            return {
                "score": 0, 
                "archetypes": ["Error"], 
                "summary": "AI failed to process this story."
            }

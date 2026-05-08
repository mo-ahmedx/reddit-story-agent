import os
import json
import time
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class DramaScorer:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.persona = (
            "You are a drama analyst for a YouTube storytelling channel. "
            "Rate the following Reddit post for its drama and storytelling potential on a scale of 1 to 10. "
            "Respond ONLY in valid JSON format with keys: 'score' (int), 'archetypes' (list of strings), 'summary' (string)."
        )

    async def analyze_story(self, title, body):
        # 15 requests per minute throttle (4 seconds between calls)
        time.sleep(4) 
        
        prompt = f"{self.persona}\n\nTitle: {title}\nStory: {body}"
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"Gemini Error: {e}")
            return {"score": 0, "archetypes": [], "summary": "Error analyzing story."}
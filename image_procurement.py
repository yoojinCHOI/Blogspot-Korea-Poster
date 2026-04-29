import logging
import requests
import random
import urllib.parse
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageProcurement:
    def __init__(self):
        self.access_key = Config.UNSPLASH_ACCESS_KEY
        if not self.access_key or self.access_key.strip().lower() in ["your_unsplash_api_key_here", "none", "null", ""]:
            logger.warning("UNSPLASH_ACCESS_KEY is missing. Stable fallback images will be used.")
        self.base_url = "https://api.unsplash.com/search/photos"

    def get_image_url(self, keyword: str) -> str:
        if not self.access_key or self.access_key.strip().lower() in ["your_unsplash_api_key_here", "none", "null", ""]:
            # Fallback to Pollinations AI, which is free and very reliable
            safe_kw = urllib.parse.quote(keyword if keyword else "finance")
            rand_seed = random.randint(1, 999999)
            return f"https://image.pollinations.ai/prompt/{safe_kw}?width=800&height=400&nologo=true&seed={rand_seed}"
            
        params = {
            "query": keyword,
            "per_page": 10,
            "orientation": "landscape"
        }
        headers = {
            "Authorization": f"Client-ID {self.access_key}"
        }
        try:
            logger.info(f"Searching Unsplash for: {keyword}")
            resp = requests.get(self.base_url, params=params, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            if data and data.get("results") and len(data["results"]) > 0:
                random_result = random.choice(data["results"])
                raw_url = random_result["urls"]["regular"]
                return raw_url
            else:
                logger.warning(f"No Unsplash results for keyword: '{keyword}'")
                safe_kw = urllib.parse.quote(keyword if keyword else "finance")
                rand_seed = random.randint(1, 999999)
                return f"https://image.pollinations.ai/prompt/{safe_kw}?width=800&height=400&nologo=true&seed={rand_seed}"
        except Exception as e:
            logger.error(f"Unsplash API error for keyword '{keyword}': {e}")
            safe_kw = urllib.parse.quote(keyword if keyword else "finance")
            rand_seed = random.randint(1, 999999)
            return f"https://image.pollinations.ai/prompt/{safe_kw}?width=800&height=400&nologo=true&seed={rand_seed}"

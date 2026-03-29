import logging
import requests
import random
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageProcurement:
    def __init__(self):
        self.access_key = Config.UNSPLASH_ACCESS_KEY
        if not self.access_key or self.access_key.strip().lower() in ["your_unsplash_api_key_here", "none", "null", ""]:
            logger.warning("UNSPLASH_ACCESS_KEY is missing. LoremFlickr free images will be used.")
        self.base_url = "https://api.unsplash.com/search/photos"

    def get_image_url(self, keyword: str) -> str:
        """
        Fetches an image URL from Unsplash based on the given keyword.
        Returns a placeholder image if the API fails or no key is provided.
        """
        if not self.access_key or self.access_key.strip().lower() in ["your_unsplash_api_key_here", "none", "null", ""]:
            # Fallback to a highly reliable free image service without API keys (LoremFlickr)
            clean_keyword = keyword.replace(' ', '').replace('-', '')
            rand_seed = random.randint(1, 10000)
            return f"https://loremflickr.com/800/400/{clean_keyword}?random={rand_seed}"
            
        params = {
            "query": keyword,
            "per_page": 1,
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
                raw_url = data["results"][0]["urls"]["regular"]
                return raw_url
            else:
                logger.warning(f"No Unsplash results for keyword: '{keyword}'")
                clean_keyword = keyword.replace(' ', '').replace('-', '')
                rand_seed = random.randint(1, 10000)
                return f"https://loremflickr.com/800/400/{clean_keyword}?random={rand_seed}"
        except Exception as e:
            logger.error(f"Unsplash API error for keyword '{keyword}': {e}")
            clean_keyword = keyword.replace(' ', '').replace('-', '')
            rand_seed = random.randint(1, 10000)
            return f"https://loremflickr.com/800/400/{clean_keyword}?random={rand_seed}"

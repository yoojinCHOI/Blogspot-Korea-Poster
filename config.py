import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local testing)
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
BLOGGER_BLOG_ID = os.getenv("BLOGGER_BLOG_ID")

class Config:
    GEMINI_API_KEY = GEMINI_API_KEY
    UNSPLASH_ACCESS_KEY = UNSPLASH_ACCESS_KEY
    BLOGGER_BLOG_ID = BLOGGER_BLOG_ID

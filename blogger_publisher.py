import os
import logging
from config import Config
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/blogger']

class BloggerPublisher:
    def __init__(self):
        self.blog_id = Config.BLOGGER_BLOG_ID
        self.service = self._authenticate()
        
    def _authenticate(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            
        # If there are no valid credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    logger.error(f"Failed to refresh token: {e}. Please delete token.json and re-authenticate.")
                    raise
            else:
                flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
                # This will open a browser to authenticate
                creds = flow.run_local_server(port=0)
                
            # Save the credentials for the next run
            with open('token.json', 'w') as token_file:
                token_file.write(creds.to_json())

        return build('blogger', 'v3', credentials=creds)

    def publish_post(self, title: str, html_body: str, publish_date=None, labels=None) -> dict:
        """
        publish_date (str): RFC 3339 formatted date-time string (e.g. '2023-12-01T10:00:00Z')
                            If None, it publishes immediately.
        """
        if not self.blog_id or self.blog_id == "your_blogger_blog_id_here":
            raise ValueError("BLOGGER_BLOG_ID is not set in environment or config.")

        body = {
            "title": title,
            "content": html_body,
            "labels": labels or []
        }
        
        if publish_date:
            body["published"] = publish_date

        try:
            logger.info(f"Publishing post: {title}")
            posts = self.service.posts()
            request = posts.insert(blogId=self.blog_id, body=body, isDraft=False)
            response = request.execute()
            logger.info(f"Post published successfully: {response.get('url')}")
            return response
        except Exception as e:
            logger.error(f"Failed to publish post to blogger: {e}")
            return None

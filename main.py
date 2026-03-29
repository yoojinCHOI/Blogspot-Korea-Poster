import time
import logging
from datetime import datetime, timedelta, timezone

from config import Config
from topic_planner import TopicPlanner
from content_generator import ContentGenerator
from image_procurement import ImageProcurement
from blogger_publisher import BloggerPublisher

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Daily Blogspot Auto-Poster Pipeline (10 Posts/Day, Korean)...")
    
    try:
        planner = TopicPlanner()
        generator = ContentGenerator()
        image_api = ImageProcurement()
        publisher = BloggerPublisher()
    except Exception as e:
        logger.error(f"Failed to initialize modules. Please check credentials. Error: {e}")
        return

    # 1. 하루 10개 주제 생성 지시 (변경점)
    topics = planner.generate_topics(count=10)
    if not topics:
        logger.error("Failed to generate topics. Exiting.")
        return

    logger.info(f"Generated {len(topics)} topics successfully. Beginning pipeline...")

    # 스케줄 시간 계산 로직 유지
    base_time = datetime.now(timezone.utc) + timedelta(minutes=30)
    schedule_interval_mins = int((24 * 60) / len(topics))

    success_count = 0

    # 2. 메인 글쓰기 루프
    for i, topic in enumerate(topics):
        logger.info(f"\n=========================================")
        logger.info(f"Processing [{i+1}/{len(topics)}]: {topic}")
        logger.info(f"=========================================")
        
        # A. Content Generation
        article_data = generator.generate_article(topic)
        if not article_data:
            logger.warning(f"Skipping topic due to content generation failure: {topic}")
            continue
            
        title = article_data.get('title', topic)
        html_body = article_data.get('html_body', f'<p>Content error for: {topic}</p>')
        image_keywords = article_data.get('image_search_keywords', [])
        hashtags = article_data.get('hashtags', [])

        # B. Image Procurement (Insert into HTML)
        for idx, keyword in enumerate(image_keywords):
            img_url = image_api.get_image_url(keyword)
            # 깔끔하게 가운데 정렬한 이미지 코드 치환
            img_tag = f'<div style="text-align: center; margin: 20px 0;"><img src="{img_url}" alt="{keyword}" style="max-width: 100%; height: auto; border-radius: 8px;"></div>'
            placeholder = f"[IMAGE_PLACEHOLDER_{idx}]"
            html_body = html_body.replace(placeholder, img_tag)

        # C. 본문 하단에 관람객이 볼 수 있는 '가시성 해시태그' 추가 기능
        if hashtags:
            hashtag_html = "<br><hr><div style='color: gray; padding: 10px 0;'>" + " ".join([f"#{t}" for t in hashtags]) + "</div>"
            html_body += hashtag_html

        # D. Schedule Publish & 블로그스팟 자체 라벨(Label) 연동
        publish_time = base_time + timedelta(minutes=i * schedule_interval_mins)
        publish_date_str = publish_time.isoformat()
        
        labels = hashtags[:10]  # 최대 10개까지만 블로그 공식 카테고리 태그로 등록

        resp = publisher.publish_post(title=title, html_body=html_body, publish_date=publish_date_str, labels=labels)
        
        if resp:
            success_count += 1
            logger.info(f"✅ Successfully scheduled: '{title}' for {publish_date_str}")
        else:
            logger.error(f"❌ Failed to publish: '{title}'")
            
        # 블로그 서버 제재 회피를 위한 대기시간
        time.sleep(3)

    logger.info(f"\nPipeline Completed! Successfully scheduled {success_count}/{len(topics)} posts for today.")

if __name__ == "__main__":
    main()

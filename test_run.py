import sys
import time
from topic_planner import TopicPlanner
from content_generator import ContentGenerator
from image_procurement import ImageProcurement
from blogger_publisher import BloggerPublisher

def run_test():
    print("🚀 [1단계] 테스트용 블로그스팟 자동 포스팅을 1개 시작합니다...")
    try:
        planner = TopicPlanner()
        generator = ContentGenerator()
        images = ImageProcurement()
        publisher = BloggerPublisher()
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        sys.exit(1)

    print("📝 [2단계] 한국어 경제/주식/보험 주제 기획 중...")
    topics = planner.generate_topics(count=1)
    if not topics:
        print("❌ 실패")
        return
    
    topic = topics[0]
    print(f"✅ 선정된 주제: {topic}")

    print("✍️  [3단계] 1500자 이상의 한국형 SEO 본문을 생성 중입니다... (약 15-30초 소요)")
    article = generator.generate_article(topic)
    if not article:
        print("❌ 실패")
        return
    
    title = article.get('title', topic)
    html_body = article.get('html_body', "")
    image_keywords = article.get('image_search_keywords', [])
    hashtags = article.get('hashtags', [])

    print("📸 [4단계] 무료 스톡 이미지를 본문에 삽입 중입니다...")
    for idx, keyword in enumerate(image_keywords):
        img_url = images.get_image_url(keyword)
        img_tag = f'<div style="text-align: center; margin: 20px 0;"><img src="{img_url}" alt="{keyword}" style="max-width: 100%; border-radius: 8px;"></div>'
        html_body = html_body.replace(f"[IMAGE_PLACEHOLDER_{idx}]", img_tag)

    if hashtags:
        # 본문 맨 하단에 눈에 보이는 해시태그 예쁘게 삽입
        hashtag_html = "<br><hr><div style='color: gray; padding: 10px 0;'>" + " ".join([f"#{t}" for t in hashtags]) + "</div>"
        html_body += hashtag_html

    print("🌐 [5단계] 구글 블로그스팟 서버로 즉시 전송합니다...")
    labels = hashtags[:10]
    
    # publish_date=None 이면 예약이 아닌 즉시 발행(Draft=False) 모드로 작동
    resp = publisher.publish_post(title=title, html_body=html_body, publish_date=None, labels=labels)
    
    if resp:
        print(f"🎉 테스트 블로그 발송 대성공! 즉시 확인해보세요: {resp.get('url')}")
        print("👉 이제 깃허브에 코드를 올려주시면 내일부터 10개의 파이프라인이 매일 작동합니다!")
    else:
        print("❌ 퍼블리시 실패")

if __name__ == "__main__":
    run_test()

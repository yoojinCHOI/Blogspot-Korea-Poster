import json
import logging
from google import genai
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentGenerator:
    def __init__(self):
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY가 없습니다.")
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
        self.model_name = 'gemini-2.5-flash'

    def generate_article(self, topic: str) -> dict:
        prompt = f"""
당신은 완벽한 상위 노출 방식을 아는 최우수 경제/주식/보험 전문 블로그 카피라이터입니다.
아래의 주제로 한국인 직장인이 읽기 편하고 검색엔진(SEO)이 가장 선호하는 1500자(한국어) 이상의 깊이 있는 블로그 본문을 작성해주세요.

[작성 주제]
"{topic}"

[필수 준수 사항]
1. 타겟 독자 및 문체: 20~50대 한국인 직장인 대상. 신뢰감 있고 친절한 존댓말(~습니다, ~해요) 사용.
2. 할루시네이션(거짓 정보) 엄격 금지: 경제 지표, 종목 추천, 확정 수익 명시 등 사실과 다르거나 법적 문제가 될 수 있는 추측성 발언은 절대 삼가고, "객관적인 개념과 정보 전달" 위주로 서술하세요. 특정 종목을 매수하라고 강요하지 마세요.
3. SEO 최적화: 
   - 글의 뼈대는 반드시 <h2>, <h3> HTML 태그를 사용해 소제목 구조로 완벽히 구성하세요. (마크다운 ## 사용 금지, 순수 HTML 태그 사용)
   - 문단 내에서 사람들이 많이 검색할 만한 핵심 전문 용어나 키워드는 <b> 태그를 입혀 굵게 처리하세요.
4. 이미지 삽입 위치:
   본문 문단들 사이사이에 정확히 3~4개의 이미지 삽입 코드를 아래 문자열 그대로 넣어주세요. (줄바꿈 포함)
   [IMAGE_PLACEHOLDER_0]
   [IMAGE_PLACEHOLDER_1]
   [IMAGE_PLACEHOLDER_2]
   [IMAGE_PLACEHOLDER_3] (4장일 경우)
5. 면책 조항(Disclaimer) 강제 삽입:
   전체 HTML 본문 내용의 맨 마지막 줄에 반드시 아래 문구를 <p> 태그와 <b> 태그를 활용해 그대로 삽입하세요.
   "<br><br><hr><p><b>※ 본 포스팅은 정보 제공을 목적으로 하며, 투자의 최종 책임은 본인에게 있습니다.</b></p>"
6. 출력 포맷:
   전체 출력을 엄격히 아래 JSON 스키마만을 따르도록 하세요. (마크다운 백틱 제외)

{{
  "title": "검색에 유리한 시선강탈 포스팅 제목",
  "html_body": "위 조건이 모두 반영된 전체 HTML 본문 코딩 문자열 (면책조항 필연적 포함)",
  "image_search_keywords": ["keyword 1", "keyword 2", "keyword 3"],
  "hashtags": ["경제", "삼성전자", "ETF", "부동산"]
}}
* image_search_keywords 속성은 무조건 '영문'으로 3~4개 채웁니다 (본문의 상황에 맞는 무료 스톡 사진 검색용 영어 단어).
* hashtags 속성은 블로그 노출 유입을 위해, 본문 내용과 연관된 '한국어 키워드'를 띄어쓰기 없이 5~10개 사이로 추출하세요.
"""
        logger.info(f"주제에 대한 본문 작성 중: {topic}")
        response = self.client.models.generate_content(
            model=self.model_name, 
            contents=prompt,
            config={'response_mime_type': 'application/json'}
        )
        text_output = response.text.strip()
        
        try:
            article_data = json.loads(text_output)
            logger.info(f"본문 작성을 성공적으로 마쳤습니다: {topic}")
            return article_data
        except json.JSONDecodeError as e:
            logger.error(f"제미나이 결과 JSON 파싱 실패: {e}")
            return None

import json
import logging
from google import genai
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TopicPlanner:
    def __init__(self):
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY가 없습니다. .env 파일을 확인해주세요.")
        
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
        self.model_name = 'gemini-2.5-flash-lite'

    def generate_topics(self, count=10) -> list:
        prompt = f"""
당신은 한국인들을 주 타겟으로 하는 웹사이트의 경제, 주식, 보험 전문 수석 콘텐츠 기획자입니다.
오늘 방문자들의 클릭을 유도할 수 있는 매우 흥미롭고 유익한 블로그 포스팅 주제 (제목) {count}개를 선정해주세요.

주제는 반드시 다음 3가지 핵심 테마에 고루 분포되어야 합니다:
1. 거시/생활 경제 (예: 금리 인하 여파, 환율 전망, 청년/직장인 경제 꿀팁 등)
2. 국내외 주식 & 투자 (예: 인기 ETF 분석, 미국 배당주, 시황 분석, 초보자 투자 개념 등)
3. 보험 및 절세 (예: 실손보험, 연금저축, 세액공제, 혜택 챙기기 가이드 등)

모든 주제는 반드시 100% 한국어로 작성되어야 하며, 구글/네이버 검색 노출에 유리한 핵심 키워드가 포함되어야 합니다.

결과는 다른 어떤 마크다운 코드나 설명 없이 아래의 예시와 같이 오직 JSON 배열(Array) 형식의 문자열 리스트로만 출력하세요.
예시:
[
  "미국 국채 금리 인하가 국내 증시에 미치는 진짜 영향",
  "20대 사회초년생이 반드시 알아야 할 실손의료보험 가입 꿀팁"
]
"""
        logger.info(f"제미나이 AI에게 {count}개의 경제 주제 기획을 요청합니다...")
        response = self.client.models.generate_content(
            model=self.model_name, 
            contents=prompt,
            config={'response_mime_type': 'application/json'}
        )
        text_output = response.text.strip()
        
        try:
            topics = json.loads(text_output)
            logger.info(f"성공적으로 {len(topics)}개의 한국어 주제를 기획했습니다.")
            return topics
        except json.JSONDecodeError as e:
            logger.error(f"주제 출력 결과를 JSON으로 파싱 실패했습니다: {e}")
            return []

if __name__ == "__main__":
    planner = TopicPlanner()
    topics = planner.generate_topics()
    for i, t in enumerate(topics, 1):
        print(f"{i}. {t}")

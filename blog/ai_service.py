import logging
from django.conf import settings
from typing import List

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# 로거 설정
logger = logging.getLogger('ai_service')

# AI 서비스 관련 예외
class AIServiceError(Exception):
    pass

# OpenAI API 서비스 클래스
class OpenAIService:
    def __init__(self):
        self.model = "gpt-4o-mini"
        self.max_tokens = 1000
        self.temperature = 0.7
        
        # API 키 확인
        if not hasattr(settings, 'OPENAI_API_KEY') or not settings.OPENAI_API_KEY:
            logger.warning("OpenAI API 키가 설정되지 않았습니다. 더미 모드로 작동합니다.")
            self.dummy_mode = True
            return
        
        if not OPENAI_AVAILABLE:
            logger.warning("OpenAI 라이브러리가 설치되지 않았습니다. 더미 모드로 작동합니다.")
            self.dummy_mode = True
            return
        
        try:
            # OpenAI 클라이언트 초기화
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
            self.dummy_mode = False
            logger.info("OpenAI API 클라이언트 초기화 완료")
        except Exception as e:
            logger.error(f"OpenAI 클라이언트 초기화 실패: {e}")
            self.dummy_mode = True
    
    # OpenAI API 요청 처리
    def _make_request(self, messages: List[dict], **kwargs) -> str:
        if self.dummy_mode:
            raise AIServiceError("AI 서비스를 사용할 수 없습니다. 관리자에게 문의하세요.")

        try:
            response = self.client.chat.completions.create(
                model=kwargs.get('model', self.model),
                messages=messages,
                max_tokens=kwargs.get('max_tokens', self.max_tokens),
                temperature=kwargs.get('temperature', self.temperature),
            )
            content = response.choices[0].message.content.strip()

            # 사용량 로깅
            if hasattr(response, 'usage') and response.usage:
                usage = response.usage
                logger.info(f"OpenAI API 사용량 - 입력: {usage.prompt_tokens}, "
                            f"출력: {usage.completion_tokens}, "
                            f"총합: {usage.total_tokens}")

            return content

        except Exception as e:
            error_msg = str(e)
            logger.error(f"OpenAI API 요청 실패: {error_msg}")

            if "rate_limit" in error_msg.lower():
                raise AIServiceError("API 사용량 한도를 초과했습니다. 잠시 후 다시 시도해주세요.")
            elif "authentication" in error_msg.lower():
                raise AIServiceError("API 인증에 실패했습니다.")
            elif "insufficient_quota" in error_msg.lower():
                raise AIServiceError("API 크레딧이 부족합니다.")
            else:
                raise AIServiceError("AI 서비스 일시 오류입니다. 다시 시도해주세요.")

    # 글 내용을 바탕으로 제목 추천
    def generate_title_suggestions(self, content: str, count: int = 5) -> List[str]:    
        if len(content) > 1000:
            content = content[:1000] + "..."
        
        messages = [
            {
                "role": "system",
                "content": "당신은 한국어 블로그 제목을 추천하는 전문가입니다. 매력적이고 클릭하고 싶은 제목을 한국어로 제안해주세요."
            },
            {
                "role": "user",
                "content": f"""
다음 글 내용을 바탕으로 {count}개의 매력적인 한국어 제목을 추천해주세요.
각 제목은 한 줄씩, 번호나 특수문자 없이 작성해주세요.

글 내용:
{content}

조건:
- 50자 이내로 작성
- 궁금증을 유발하는 제목
- 감정적 어필이 있는 제목
- 한국어로만 작성
- SEO에 도움이 되는 키워드 포함
"""
            }
        ]
        
        try:
            response = self._make_request(messages, max_tokens=200)
            titles = [title.strip() for title in response.split('\n') if title.strip()]
            
            # 빈 제목이나 번호가 포함된 제목 제거
            clean_titles = []
            for title in titles:
                if title and not title[0].isdigit() and len(title) > 5:
                    clean_titles.append(title)
            
            return clean_titles[:count] if clean_titles else ["AI 추천 제목을 생성할 수 없습니다"]
        
        except Exception as e:
            logger.error(f"제목 추천 생성 실패: {e}")
            return [f"📝 {content[:20]}...에 대한 완벽 가이드", f"🚀 {content[:15]}... 시작하기"]
    
    # 글 자동완성
    def generate_content_completion(self, partial_content: str, style: str = "friendly") -> str:
        style_prompts = {
            "friendly": "친근하고 대화하는 듯한 톤으로",
            "professional": "전문적이고 격식있는 톤으로",
            "casual": "캐주얼하고 편안한 톤으로",
            "informative": "정보 전달에 집중하는 톤으로"
        }
        
        style_instruction = style_prompts.get(style, style_prompts["friendly"])
        
        messages = [
            {
                "role": "system",
                "content": f"당신은 한국어 블로그 글쓰기를 도와주는 AI 어시스턴트입니다. {style_instruction} 글을 자연스럽게 이어서 작성해주세요."
            },
            {
                "role": "user",
                "content": f"""
다음 글을 자연스럽게 이어서 한국어로 작성해주세요:

{partial_content}

조건:
- 2-3 문단 정도로 작성
- 기존 내용과 자연스럽게 연결
- 읽기 쉽고 흥미로운 내용
- 한국어로만 작성
- 실용적이고 도움이 되는 정보 포함
"""
            }
        ]
        
        try:
            completion = self._make_request(messages, max_tokens=500)
            return completion if completion else "자동완성을 생성할 수 없습니다."
        
        except Exception as e:
            logger.error(f"내용 자동완성 생성 실패: {e}")
            return "이어서 설명하면, 이 주제에 대해 더 깊이 있게 다뤄보겠습니다. 실무에서 유용한 팁들을 공유하겠습니다."
    
    # 제목과 내용을 바탕으로 태그 추천
    def generate_tags(self, title: str, content: str, max_tags: int = 5) -> List[str]:
        
        if len(content) > 800:
            content = content[:800] + "..."
        
        messages = [
            {
                "role": "system",
                "content": "당신은 한국어 블로그 태그를 추천하는 전문가입니다. 글의 주제와 내용을 분석하여 적절한 태그를 제안해주세요."
            },
            {
                "role": "user",
                "content": f"""
다음 블로그 글에 적합한 태그 {max_tags}개를 추천해주세요.

제목: {title}

내용:
{content}

조건:
- 각 태그는 한 줄씩, 번호 없이 작성
- 한글과 영어 모두 가능
- 검색에 도움이 되는 키워드
- 글의 주제와 직접적으로 관련
- 간결하고 명확한 단어 (2-10자)
- 해시태그 없이 단어만
"""
            }
        ]
        
        try:
            response = self._make_request(messages, max_tokens=150)
            tags = [tag.strip().replace('#', '') for tag in response.split('\n') if tag.strip()]
            
            # 빈 태그나 너무 긴 태그 제거
            clean_tags = []
            for tag in tags:
                if tag and 2 <= len(tag) <= 15 and not tag[0].isdigit():
                    clean_tags.append(tag)
            
            return clean_tags[:max_tags] if clean_tags else ["기술", "블로그", "개발"]
        
        except Exception as e:
            logger.error(f"태그 추천 생성 실패: {e}")
            return ["Python", "Django", "웹개발", "프로그래밍"]
    
    # 글 요약 생성
    def generate_summary(self, content: str, max_length: int = 200) -> str:
        
        messages = [
            {
                "role": "system",
                "content": "당신은 한국어 글 요약 전문가입니다. 주어진 글의 핵심 내용을 간결하고 명확하게 요약해주세요."
            },
            {
                "role": "user",
                "content": f"""
다음 글을 {max_length}자 이내로 한국어로 요약해주세요:

{content}

조건:
- 글의 핵심 메시지 포함
- 읽기 쉽고 명확한 문장
- 원문의 톤 유지
- 한국어로만 작성
- {max_length}자 이내
"""
            }
        ]
        
        try:
            summary = self._make_request(messages, max_tokens=300)
            
            # 길이 제한
            if len(summary) > max_length:
                summary = summary[:max_length-3] + "..."
            
            return summary if summary else "요약을 생성할 수 없습니다."
        
        except Exception as e:
            logger.error(f"요약 생성 실패: {e}")
            return "이 글의 핵심 내용을 요약한 정보입니다."

# 싱글톤 인스턴스
try:
    ai_service = OpenAIService()
    logger.info("AI 서비스 초기화 완료")
except Exception as e:
    logger.error(f"AI 서비스 초기화 실패: {e}")
    ai_service = None

# 제목 추천 가져오기
def get_title_suggestions(content: str, count: int = 3) -> List[str]:
    if not ai_service:
        return ["제목을 생성할 수 없습니다"]
    return ai_service.generate_title_suggestions(content, count)

# 내용 자동완성 가져오기
def get_content_completion(partial_content: str, style: str = "friendly") -> str:
    if not ai_service:
        return "자동완성을 사용할 수 없습니다."
    return ai_service.generate_content_completion(partial_content, style)

# 태그 추천 가져오기
def get_tag_suggestions(title: str, content: str, max_tags: int = 5) -> List[str]:
    if not ai_service:
        return ["태그", "추천", "불가"]
    return ai_service.generate_tags(title, content, max_tags)

# 내용 요약 가져오기
def get_content_summary(content: str, max_length: int = 200) -> str:
    if not ai_service:
        return "요약을 사용할 수 없습니다."
    return ai_service.generate_summary(content, max_length)
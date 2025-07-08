import json
import time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .ai_service import get_title_suggestions, get_content_completion, get_tag_suggestions, get_content_summary
from .models import AIUsageLog
import logging

logger = logging.getLogger(__name__)

# 제목 추천
@method_decorator([login_required, csrf_exempt], name='dispatch')
class TitleSuggestionView(View):    
    def post(self, request):
        logger.info(f"제목 추천 요청 - 사용자: {request.user.username}")
        
        try:
            data = json.loads(request.body)
            content = data.get('content', '').strip()
            
            if not content:
                return JsonResponse({
                    'success': False,
                    'error': '내용을 입력해주세요.'
                })
            
            if len(content) < 20:
                return JsonResponse({
                    'success': False,
                    'error': f'더 많은 내용을 작성한 후 제목을 추천받아보세요. (현재: {len(content)}자, 최소: 50자)'
                })
            
            # AI 제목 추천 요청
            logger.info(f"OpenAI API 제목 추천 요청 시작 - 내용 길이: {len(content)}자")
            start_time = time.time()
            
            titles = get_title_suggestions(content, count=4)
            
            end_time = time.time()
            logger.info(f"OpenAI API 제목 추천 완료 - 소요시간: {end_time - start_time:.2f}초")
            
            if titles:
                # AI 사용량 로깅
                AIUsageLog.objects.create(
                    user=request.user,
                    feature_type='title_suggest',
                    tokens_used=len(content) // 4
                )
                
                # 사용자 AI 사용량 증가
                request.user.ai_usage_count += 1
                request.user.save()
                
                logger.info(f"제목 추천 성공 - {len(titles)}개 생성")
                
                return JsonResponse({
                    'success': True,
                    'titles': titles,
                    'message': f'AI가 {len(titles)}개의 제목을 추천했습니다!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': '제목 추천에 실패했습니다. 다시 시도해주세요.'
                })
                
        except json.JSONDecodeError:
            logger.error("JSON 파싱 오류")
            return JsonResponse({
                'success': False,
                'error': '요청 형식이 올바르지 않습니다.'
            })
        except Exception as e:
            logger.error(f"제목 추천 API 오류: {e}")
            return JsonResponse({
                'success': False,
                'error': f'서버 오류가 발생했습니다: {str(e)}'
            })

# 내용 자동완성 API
@method_decorator([login_required, csrf_exempt], name='dispatch')
class ContentCompletionView(View):
    def post(self, request):
        logger.info(f"자동완성 요청 - 사용자: {request.user.username}")
        
        try:
            data = json.loads(request.body)
            content = data.get('content', '').strip()
            style = data.get('style', 'friendly')
            
            if not content:
                return JsonResponse({
                    'success': False,
                    'error': '내용을 입력해주세요.'
                })
            
            if len(content) < 30:
                return JsonResponse({
                    'success': False,
                    'error': f'더 많은 내용을 작성한 후 자동완성을 사용해보세요. (현재: {len(content)}자, 최소: 30자)'
                })
            
            # AI 자동완성 요청
            logger.info(f"OpenAI API 자동완성 요청 시작 - 내용 길이: {len(content)}자, 스타일: {style}")
            start_time = time.time()
            
            completion = get_content_completion(content, style)
            
            end_time = time.time()
            logger.info(f"OpenAI API 자동완성 완료 - 소요시간: {end_time - start_time:.2f}초")
            
            if completion:
                # AI 사용량 로깅
                AIUsageLog.objects.create(
                    user=request.user,
                    feature_type='autocomplete',
                    tokens_used=len(content + completion) // 4
                )
                
                request.user.ai_usage_count += 1
                request.user.save()
                
                logger.info(f"자동완성 성공 - {len(completion)}자 생성")
                
                return JsonResponse({
                    'success': True,
                    'completion': completion,
                    'message': 'AI가 글을 이어서 작성했습니다!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': '자동완성에 실패했습니다. 다시 시도해주세요.'
                })
                
        except Exception as e:
            logger.error(f"자동완성 API 오류: {e}")
            return JsonResponse({
                'success': False,
                'error': f'서버 오류가 발생했습니다: {str(e)}'
            })

# 태그 추천 API
@method_decorator([login_required, csrf_exempt], name='dispatch')
class TagSuggestionView(View):
    def post(self, request):
        logger.info(f"태그 추천 요청 - 사용자: {request.user.username}")
        
        try:
            data = json.loads(request.body)
            title = data.get('title', '').strip()
            content = data.get('content', '').strip()
            
            if not title and not content:
                return JsonResponse({
                    'success': False,
                    'error': '제목이나 내용을 입력해주세요.'
                })
            
            # AI 태그 추천 요청
            logger.info(f"OpenAI API 태그 추천 요청 시작")
            start_time = time.time()
            
            tags = get_tag_suggestions(title, content, max_tags=5)
            
            end_time = time.time()
            logger.info(f"OpenAI API 태그 추천 완료 - 소요시간: {end_time - start_time:.2f}초")
            
            if tags:
                # AI 사용량 로깅
                AIUsageLog.objects.create(
                    user=request.user,
                    feature_type='tag_suggest',
                    tokens_used=len(title + content) // 4
                )
                
                request.user.ai_usage_count += 1
                request.user.save()
                
                logger.info(f"태그 추천 성공 - {len(tags)}개 생성")
                
                return JsonResponse({
                    'success': True,
                    'tags': tags,
                    'message': f'AI가 {len(tags)}개의 태그를 추천했습니다!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': '태그 추천에 실패했습니다. 다시 시도해주세요.'
                })
                
        except Exception as e:
            logger.error(f"태그 추천 API 오류: {e}")
            return JsonResponse({
                'success': False,
                'error': f'서버 오류가 발생했습니다: {str(e)}'
            })

# 요약 생성 API
@method_decorator([login_required, csrf_exempt], name='dispatch')
class SummaryGenerationView(View):
    def post(self, request):
        logger.info(f"요약 생성 요청 - 사용자: {request.user.username}")
        
        try:
            data = json.loads(request.body)
            content = data.get('content', '').strip()
            
            if not content:
                return JsonResponse({
                    'success': False,
                    'error': '내용을 입력해주세요.'
                })
            
            if len(content) < 200:
                return JsonResponse({
                    'success': False,
                    'error': f'요약하기에는 내용이 너무 짧습니다. (현재: {len(content)}자, 최소: 200자)'
                })
            
            # AI 요약 생성 요청
            logger.info(f"OpenAI API 요약 생성 요청 시작 - 내용 길이: {len(content)}자")
            start_time = time.time()
            
            summary = get_content_summary(content, max_length=200)
            
            end_time = time.time()
            logger.info(f"OpenAI API 요약 생성 완료 - 소요시간: {end_time - start_time:.2f}초")
            
            if summary:
                # AI 사용량 로깅
                AIUsageLog.objects.create(
                    user=request.user,
                    feature_type='summary',
                    tokens_used=len(content + summary) // 4
                )
                
                request.user.ai_usage_count += 1
                request.user.save()
                
                logger.info(f"요약 생성 성공 - {len(summary)}자 생성")
                
                return JsonResponse({
                    'success': True,
                    'summary': summary,
                    'message': 'AI가 글을 요약했습니다!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': '요약 생성에 실패했습니다. 다시 시도해주세요.'
                })
                
        except Exception as e:
            logger.error(f"요약 생성 API 오류: {e}")
            return JsonResponse({
                'success': False,
                'error': f'서버 오류가 발생했습니다: {str(e)}'
            })

# 사용자 AI 사용량 통계
@login_required
def ai_usage_stats(request):
    try:
        user_usage = AIUsageLog.objects.filter(user=request.user)
        
        stats = {
            'total_usage': request.user.ai_usage_count,
            'title_suggestions': user_usage.filter(feature_type='title_suggest').count(),
            'autocompletions': user_usage.filter(feature_type='autocomplete').count(),
            'tag_suggestions': user_usage.filter(feature_type='tag_suggest').count(),
            'summaries': user_usage.filter(feature_type='summary').count(),
        }
        
        logger.info(f"AI 사용량 통계 조회 - 사용자: {request.user.username}, 총 사용량: {stats['total_usage']}")
        
        return JsonResponse({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        logger.error(f"AI 사용량 통계 오류: {e}")
        return JsonResponse({
            'success': False,
            'error': '통계를 가져오는데 실패했습니다.'
        })
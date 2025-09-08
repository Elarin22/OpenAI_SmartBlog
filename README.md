# Smart Blog

## Overview
Smart Blog는 OpenAI GPT-4 API를 활용한 AI 기반 블로그 플랫폼으로, 사용자가 더 쉽고 효과적으로 글을 작성할 수 있도록 다양한 AI 도구를 제공합니다.

---

## Project Goals
- AI 기반 글쓰기 도구로 콘텐츠 작성 효율성 향상
- 실시간 상호작용을 통한 사용자 참여도 증대
- 소셜 기능으로 커뮤니티 활성화
- 반응형 디자인으로 모든 디바이스 호환성 확보

---

## Key Features
- **AI 글쓰기 도우미**: 제목 추천, 자동완성, 태그 제안, 요약 생성
- **실시간 상호작용**: AJAX 기반 댓글, 좋아요, 팔로우 시스템
- **소셜 기능**: 팔로우/팔로워, 프로필 시스템
- **반응형 디자인**: Bootstrap 5 기반 모던 UI
- **보안**: CSRF 보호, 권한 기반 접근 제어

---

## Technologies
- **Backend**: Django, Python, SQLite3
- **Authentication**: Django Auth, Custom User Model
- **AI Integration**: OpenAI GPT-4 API
- **Frontend**: Bootstrap 5, HTML/CSS, JavaScript (AJAX)
- **Storage**: Django Media & Static Files
- **Mobile Testing**: ngrok, QR Code Generator

---

## URL 구조

**Main**
| 메서드 | 엔드포인트 | 설명 |
|--------|-----|-------------|
| GET | `/` | 메인 페이지 (블로그 목록) |
| GET | `/admin/` | 관리자 페이지 |

**Blog**
| 메서드 | 엔드포인트 | 설명 |
|--------|-----|-------------|
| GET | `/blog/` | 게시글 목록 |
| GET | `/blog/write/` | 게시글 작성 페이지 |
| POST | `/blog/write/` | 게시글 작성 처리 |
| GET | `/blog/<int:pk>/` | 게시글 상세보기 |
| GET | `/blog/<int:pk>/edit/` | 게시글 수정 페이지 |
| POST | `/blog/<int:pk>/edit/` | 게시글 수정 처리 |
| POST | `/blog/<int:pk>/delete/` | 게시글 삭제 |

**Comment**
| 메서드 | 엔드포인트 | 설명 |
|--------|-----|-------------|
| POST | `/blog/comment/<int:post_id>/create/` | 댓글 작성 |
| POST | `/blog/comment/<int:comment_id>/delete/` | 댓글 삭제 |
| POST | `/blog/comment/<int:comment_id>/update/` | 댓글 수정 |
| GET | `/blog/comments/<int:post_id>/` | 댓글 목록 조회 |

**Like**
| 메서드 | 엔드포인트 | 설명 |
|--------|-----|-------------|
| POST | `/blog/like/<int:post_id>/` | 좋아요 토글 |

**AI Features**
| 메서드 | 엔드포인트 | 설명 |
|--------|-----|-------------|
| POST | `/blog/ai/suggest-title/` | AI 제목 추천 |
| POST | `/blog/ai/complete-content/` | AI 내용 자동완성 |
| POST | `/blog/ai/suggest-tags/` | AI 태그 추천 |
| POST | `/blog/ai/generate-summary/` | AI 요약 생성 |
| GET | `/blog/ai/usage-stats/` | AI 사용량 통계 |

**Account**
| 메서드 | 엔드포인트 | 설명 |
|--------|-----|-------------|
| GET | `/accounts/signup/` | 회원가입 페이지 |
| POST | `/accounts/signup/` | 회원가입 처리 |
| GET | `/accounts/login/` | 로그인 페이지 |
| POST | `/accounts/login/` | 로그인 처리 |
| POST | `/accounts/logout/` | 로그아웃 |
| GET | `/accounts/profile/` | 내 프로필 |
| GET | `/accounts/profile/<int:user_id>/` | 사용자 프로필 |
| GET | `/accounts/profile/update/` | 프로필 수정 페이지 |
| POST | `/accounts/profile/update/` | 프로필 수정 처리 |
| GET | `/accounts/password/change/` | 비밀번호 변경 페이지 |
| POST | `/accounts/password/change/` | 비밀번호 변경 처리 |

**Follow**
| 메서드 | 엔드포인트 | 설명 |
|--------|-----|-------------|
| POST | `/accounts/follow/<int:user_id>/` | 팔로우 토글 |
| GET | `/accounts/followers/<int:user_id>/` | 팔로워 목록 |
| GET | `/accounts/following/<int:user_id>/` | 팔로잉 목록 |

---

## System Architecture

### AI Integration
OpenAI GPT-4 API를 통한 스마트 글쓰기 기능을 제공하며, 제목 추천, 내용 자동완성, 태그 제안, 요약 생성 등의 기능과 사용량 추적 시스템을 포함합니다.

### Database Models
- **CustomUser**: 확장된 사용자 정보 및 AI 사용 횟수 추적
- **Post**: 게시글, AI 생성 요약, 태그 및 조회수 관리
- **Comment**: 계층형 댓글 시스템
- **Follow**: 팔로우/팔로워 관계 관리
- **Like**: 좋아요 시스템
- **AIUsageLog**: AI 기능 사용량 통계

---

## Unique Features
- **AI 글쓰기 도우미**: OpenAI GPT-4를 활용한 제목 추천, 자동완성, 태그 제안
- **실시간 상호작용**: AJAX 기반 댓글, 좋아요, 팔로우 시스템
- **계층형 댓글**: 대댓글 기능으로 깊이 있는 토론 지원
- **AI 사용량 추적**: 사용자별 AI 기능 이용 통계
- **반응형 UI**: 모바일 친화적 디자인

---

## Developer
**개발자**: S.H.H (Smart Blog)
- GitHub: [@Hyeoni-729](https://github.com/Hyeoni-729)
- 전체 시스템 설계 및 개발
- AI 통합 및 프론트엔드 구현

---

## 핵심 기능 코드 구현

### 1. AI 기반 제목 추천 시스템

**AI 서비스 클래스** (`blog/ai_service.py`)
```python
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

글 내용: {content}
"""
        }
    ]
    
    response = self._make_request(messages, max_tokens=200)
    titles = [title.strip() for title in response.split('\n') if title.strip()]
    return titles[:count] if titles else ["AI 추천 제목을 생성할 수 없습니다"]
```

**AI API 뷰** (`blog/ai_views.py`)
```python
@method_decorator([login_required, csrf_exempt], name='dispatch')
class TitleSuggestionView(View):    
    def post(self, request):
        try:
            data = json.loads(request.body)
            content = data.get('content', '').strip()
            
            if len(content) < 20:
                return JsonResponse({'success': False, 'error': '더 많은 내용을 입력해주세요.'})
            
            titles = get_title_suggestions(content, count=4)
            
            # AI 사용량 로깅
            AIUsageLog.objects.create(
                user=request.user,
                feature_type='title_suggest',
                tokens_used=len(content) // 4
            )
            
            return JsonResponse({'success': True, 'titles': titles})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
```

### 2. 실시간 좋아요 시스템

**모델 메서드** (`blog/models.py`)
```python
class Post(models.Model):
    # 좋아요 토글 (좋아요/취소)
    def toggle_like(self, user):
        if not user.is_authenticated:
            return False, 0
        
        like, created = Like.objects.get_or_create(user=user, post=self)
        if not created:
            # 이미 좋아요한 경우 -> 취소
            like.delete()
            return False, self.get_like_count()
        else:
            # 새로 좋아요
            return True, self.get_like_count()
    
    def get_like_count(self):
        return self.likes.count()
```

**AJAX 좋아요 처리** (`blog/views.py`)
```python
@method_decorator([login_required, csrf_exempt], name='dispatch')
class LikeToggleView(View):
    def post(self, request, post_id):
        try:
            post = get_object_or_404(Post, id=post_id)
            is_liked, like_count = post.toggle_like(request.user)
            
            return JsonResponse({
                'success': True,
                'is_liked': is_liked,
                'like_count': like_count
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
```

### 3. 계층형 댓글 시스템

**댓글 모델** (`blog/models.py`)
```python
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)  # 대댓글
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
```

**댓글 작성 뷰**
```python
@method_decorator([login_required, csrf_exempt], name='dispatch')
class CommentCreateView(View):
    def post(self, request, post_id):
        try:
            data = json.loads(request.body)
            post = get_object_or_404(Post, id=post_id)
            
            comment = Comment.objects.create(
                post=post,
                author=request.user,
                content=data.get('content'),
                parent_id=data.get('parent_id')  # 대댓글인 경우
            )
            
            return JsonResponse({
                'success': True,
                'comment_id': comment.id,
                'author': comment.author.username,
                'content': comment.content,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M')
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
```

### 4. 팔로우 시스템

**팔로우 모델** (`accounts/models.py`)
```python
class CustomUser(AbstractUser):
    def toggle_follow(self, user):
        if user == self or not user:
            return False, 0
        
        follow, created = Follow.objects.get_or_create(follower=self, following=user)
        if not created:
            # 이미 팔로우한 경우 -> 언팔로우
            follow.delete()
            return False, user.get_follower_count()
        else:
            # 새로 팔로우
            return True, user.get_follower_count()
    
    def get_follower_count(self):
        return self.followers.count()
```

### 5. 게시글 검색 및 필터링

**고급 검색 쿼리** (`blog/views.py`)
```python
def get_queryset(self):
    queryset = Post.objects.select_related("author").prefetch_related("tags", "likes").annotate(likes_count=Count('likes'))
    
    # 검색 기능
    search_query = self.request.GET.get("search")
    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(tags__name__icontains=search_query)
        ).distinct()
    
    # 정렬 옵션
    sort_by = self.request.GET.get("sort", "latest")
    if sort_by == "likes":
        queryset = queryset.order_by("-likes_count", "-created_at")
    elif sort_by == "views":
        queryset = queryset.order_by("-views", "-created_at")
    
    return queryset
```

---

## Installation & Setup
```bash
# 프로젝트 클론
git clone [repository-url]
cd SmartBlog

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# 환경변수 설정 (.env 파일 생성)
OPENAI_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here

# 데이터베이스 마이그레이션
python manage.py makemigrations
python manage.py migrate

# 서버 실행
python manage.py runserver
```

### Mobile Access with QR Code
개발 중인 웹 애플리케이션을 모바일 기기에서 쉽게 테스트할 수 있도록 ngrok 터널링과 QR 코드 생성 기능을 제공합니다.

#### 작동 원리
1. **ngrok 터널링**: 로컬 개발 서버를 외부에서 접근 가능한 HTTPS URL로 터널링
2. **QR 코드 생성**: ngrok URL을 QR 코드로 변환하여 터미널에 표시
3. **모바일 접속**: QR 코드 스캔으로 즉시 모바일 브라우저에서 접속

#### 사용 방법
```bash
# 1. Django 서버 실행
python manage.py runserver 8000

# 2. ngrok으로 터널링 (새 터미널 창에서)
./ngrok http 8000

# 3. QR 코드 생성 및 표시 (또 다른 터미널에서)
python qr_generator.py
```

#### 장점
- **실시간 테스트**: 코드 변경 사항을 모바일에서 즉시 확인
- **반응형 테스트**: 다양한 모바일 디바이스에서 UI/UX 검증
- **터치 인터랙션**: 모바일 환경에서의 사용성 테스트
- **네트워크 테스트**: 실제 모바일 네트워크 환경에서의 성능 확인

---

## Development Timeline
프로젝트는 약 6일간 개발되었으며, 기획부터 배포까지 체계적인 개발 프로세스를 통해 완성되었습니다.

- **기획 및 설계**: 요구사항 분석, UI/UX 설계, 데이터베이스 모델링
- **백엔드 개발**: Django 설정, 인증 시스템, 블로그 CRUD, AI 통합
- **프론트엔드 개발**: 반응형 템플릿, AJAX 상호작용 구현
- **테스트 및 배포**: 기능 테스트, 문서화, 최종 배포
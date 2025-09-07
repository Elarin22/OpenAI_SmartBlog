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

## System Architecture

### Core Applications
- **smartblog/**: 메인 프로젝트 설정 및 URL 라우팅
- **accounts/**: 사용자 인증, 프로필 관리, 팔로우 시스템
- **blog/**: 블로그 CRUD, AI 통합, 댓글/좋아요 시스템

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
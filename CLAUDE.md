# CLAUDE.md

## 프로젝트 개요

RealWorld 스펙을 준수하는 Conduit API (Medium.com 클론). Litestar ASGI 프레임워크 기반 백엔드.

- **스택**: Litestar + SQLAlchemy (async) + PostgreSQL 16 + msgspec
- **인증**: JWT (litestar-jwt) + Argon2 패스워드 해싱
- **Python**: 3.13, 패키지 매니저 uv
- **품질 도구**: ruff (린트/포맷), ty (타입 체크), pytest (테스트)

## 아키텍처

```
Conduit/
├── main.py                 ← Litestar 앱 인스턴스 (라우트 등록, DB lifespan, CORS, OpenAPI)
├── settings.py             ← 환경 변수 기반 설정 (DB_URL, JWT_SECRET 등)
├── exception_handlers.py   ← ValidationException 핸들러
├── auth/
│   ├── jwt_auth.py         ← JWT 인증 설정 (litestar-jwt)
│   └── password_helper.py  ← Argon2 해싱/검증
├── routes/                 ← API 컨트롤러 (Litestar Controller 상속)
│   ├── article_controller.py
│   ├── profile_controller.py
│   ├── tag_controller.py
│   └── user_controller.py
├── db/                     ← SQLAlchemy 쿼리 모듈 (비즈니스 로직 분리)
│   ├── models.py           ← ORM 모델 (User, Article, Comment, Tag, ArticleTag, UserFavorite, UserFollow)
│   ├── article_queries.py
│   ├── comment_queries.py
│   ├── favorite_queries.py
│   ├── tag_queries.py
│   └── user_queries.py
└── schemas/                ← msgspec 기반 요청/응답 스키마
    ├── request_schemas.py
    └── response_schemas.py
```

### 코드 배치 규칙

- **라우트 핸들러** → `routes/` 컨트롤러에 배치
- **DB 쿼리/비즈니스 로직** → `db/` 쿼리 모듈에 분리 (컨트롤러에 직접 쿼리 작성 금지)
- **요청/응답 타입** → `schemas/`에 정의
- **설정값** → `settings.py`에서 환경 변수로 관리

## 개발 환경

### 사전 요구사항

Docker, Make

### 환경 설정

```bash
cp .env.example .env
```

### 주요 명령어

| 명령어 | 용도 |
|--------|------|
| `make up` | 앱 서버 시작 (localhost:8000) |
| `make test` | 테스트 실행 (Docker Compose로 PostgreSQL + pytest) |
| `make lint` | ruff check + ruff format + ty check |
| `make down` | 컨테이너 중지 |
| `make reset-db` | DB 초기화 후 재시작 |
| `make ruff` | ruff check --fix && ruff format |
| `make ty` | ty check |

### 테스트 실행 방식

`make test`는 Docker Compose로 PostgreSQL을 새로 띄우고 (`down-v` → `build` → `run test`) pytest를 실행한다. 테스트는 실제 DB에 연결하여 실행되며, fixture는 `tests/conftest.py`에서 session scope로 관리한다.

## 테스트 현황

| 컨트롤러 | 테스트 파일 | 상태 |
|----------|------------|------|
| article_controller | test_article_controller.py | ✅ 있음 (unhappy path) |
| profile_controller | test_profile_controller.py | ✅ 있음 (unhappy path) |
| user_controller | test_user_controller.py | ✅ 있음 (unhappy path) |
| tag_controller | — | ❌ 없음 |

- **Happy path**: Postman 컬렉션(`Conduit.postman_collection.json`)으로만 커버, 자동화 테스트 없음
- **갭**: tag 컨트롤러 테스트 부재, happy path 자동화 부재, DB 쿼리 모듈 단위 테스트 없음

## 편집 가이드라인

- RealWorld 스펙을 준수할 것 — API 응답 형식, 엔드포인트 경로는 스펙에 정의됨
- `asyncio_mode = "auto"` — 테스트에서 async/await 자동 처리
- ruff lint에 isort(`I`) 규칙 포함 — import 정렬 자동 적용
- 이 문서(CLAUDE.md)를 코드 구조 변경 시 함께 업데이트할 것

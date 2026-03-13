## 1. CLAUDE.md 파일 생성 및 프로젝트 개요

- [ ] 1.1 프로젝트 루트에 CLAUDE.md 파일 생성
- [ ] 1.2 프로젝트 개요 섹션 작성 (Litestar + SQLAlchemy + PostgreSQL 스택, RealWorld Conduit API 목적, Python 3.13)

## 2. 아키텍처 맵

- [ ] 2.1 Conduit/ 디렉토리 구조 트리 작성 (routes, db, schemas, auth, settings)
- [ ] 2.2 각 모듈의 역할과 파일 배치 규칙 기술 (라우트→routes/, 쿼리→db/, 스키마→schemas/)

## 3. 개발 환경 및 명령어

- [ ] 3.1 환경 설정 가이드 작성 (.env.example → .env 복사, Docker 필수)
- [ ] 3.2 주요 Make 명령어 정리 (up, test, lint, down, reset-db)

## 4. 테스트 현황 및 갭 분석

- [ ] 4.1 현재 테스트 커버리지 현황 기술 (3/4 컨트롤러: article, profile, user)
- [ ] 4.2 테스트 갭 명시 (tag 컨트롤러 테스트 부재, happy path 자동화 부재, Postman 컬렉션 의존)

## 5. 코드 컨벤션 및 편집 가이드라인

- [ ] 5.1 코드 스타일 규칙 기술 (ruff 린트/포맷, ty 타입 체크, asyncio_mode=auto)
- [ ] 5.2 편집 가이드라인 작성 (RealWorld 스펙 준수, DB 쿼리 분리 패턴, 문서 업데이트 규칙)

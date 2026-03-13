## Why

이 프로젝트에는 AI 코딩 도구(Claude Code)가 참조할 수 있는 컨텍스트 문서가 없다. CLAUDE.md 없이 작업하면 Claude Code가 프로젝트의 아키텍처, 컨벤션, 실행 방법을 모른 채 코드를 생성하게 되어 품질이 떨어진다. 이후 테스트 구현과 CI/CD 구축을 위한 기반으로서 지금 문서화가 필요하다.

## What Changes

- 프로젝트 루트에 `CLAUDE.md` 신규 생성 — Claude Code가 이 프로젝트를 이해하기 위한 핵심 컨텍스트 문서
- 프로젝트 개요 (Litestar + SQLAlchemy + PostgreSQL 스택, RealWorld 스펙 준수)
- 아키텍처 맵 (`Conduit/` 하위 모듈 구조: routes, db, schemas, auth, settings)
- 개발 환경 및 명령어 (Docker 기반 `make up/test/lint`, `.env` 설정)
- 테스트 현황 및 갭 분석 (3/4 컨트롤러만 테스트 존재, happy path 자동화 부재)
- 코드 컨벤션 및 편집 가이드라인 (ruff + ty, DB 쿼리 분리 패턴, RealWorld 스펙 준수 규칙)

## Capabilities

### New Capabilities
- `claude-context`: Claude Code가 프로젝트를 이해하고 올바른 코드를 생성할 수 있도록 하는 CLAUDE.md 컨텍스트 문서

### Modified Capabilities

(없음 — 기존 기능 변경 없이 문서만 추가)

## Impact

- **신규 파일**: `CLAUDE.md` (프로젝트 루트)
- **코드 변경**: 없음 — 순수 문서 추가
- **의존성 변경**: 없음
- **후속 작업에 미치는 영향**: 이 문서가 이후 테스트 구현, CI/CD 구축 작업에서 Claude Code의 컨텍스트로 활용됨
## Context

litestar-realworld는 Litestar ASGI 프레임워크로 구현한 RealWorld Conduit API다. 현재 README.md에 기본적인 스택 설명과 Getting Started가 있지만, AI 코딩 도구가 참조할 수 있는 구조화된 컨텍스트 문서는 없다.

현재 상태:
- 소스 코드: `Conduit/` 하위 21개 Python 파일 (routes 4개, db 5개, schemas 2개, auth 2개)
- 테스트: `tests/test_routes/` 하위 3개 파일 (article, profile, user — tag 누락)
- 인프라: Docker Compose (app, test, postgres 서비스), Makefile
- 품질 도구: ruff (린트/포맷), ty (타입 체크), pytest (테스트)

## Goals / Non-Goals

**Goals:**
- Claude Code가 이 프로젝트에서 즉시 올바른 코드를 생성할 수 있도록 충분한 컨텍스트 제공
- 이후 테스트 구현, CI/CD 구축 작업의 기반 문서 역할
- 프로젝트 컨벤션을 명시하여 AI 생성 코드의 일관성 보장

**Non-Goals:**
- README.md 대체 또는 수정 — README는 사람용, CLAUDE.md는 AI용으로 목적이 다름
- 코드 변경 — 이 change는 순수 문서 추가만 수행
- 튜토리얼이나 상세 API 문서 작성 — CLAUDE.md는 컨텍스트 문서이지 레퍼런스가 아님

## Decisions

### 1. 단일 CLAUDE.md 파일로 구성 (분할하지 않음)

프로젝트 규모가 작다 (Python 파일 21개). 섹션별로 분할하면 오히려 관리 부담이 늘고, Claude Code가 여러 파일을 읽어야 해서 컨텍스트 효율이 떨어진다.

**대안 검토**: `.claude/` 디렉토리에 여러 md 파일로 분할 → 이 규모에서는 과도한 구조화

### 2. 한국어로 작성 (기술 용어만 영문 병기)

워크숍 참가자 전원이 한국어 사용자이며, 워크숍 커리큘럼 프로젝트 전체가 한국어 기반이다. Claude Code는 한국어 CLAUDE.md를 문제 없이 이해한다.

**대안 검토**: 영문 작성 → 워크숍 맥락과 불일치

### 3. 테스트 갭 분석을 명시적으로 포함

이후 2단계(테스트 구현)에서 Claude Code가 "어디부터 테스트를 짜야 하는지" 즉시 판단할 수 있어야 한다. 현재 tag 컨트롤러 테스트 부재, happy path 자동화 부재를 명시한다.

**대안 검토**: 테스트 현황 생략 → 2단계 진입 시 다시 코드 분석 필요, 비효율

### 4. Make 명령어 중심으로 실행 가이드 작성

이 프로젝트는 Docker 기반이며 Makefile이 모든 명령어를 감싸고 있다. Docker Compose 명령어를 직접 나열하는 것보다 Make 타겟으로 안내하는 게 간결하고 실수가 줄어든다.

## Risks / Trade-offs

- **[문서 노후화 리스크]** → 코드가 변경되면 CLAUDE.md도 업데이트해야 한다. 완화: CLAUDE.md에 "이 문서를 코드 변경 시 함께 업데이트할 것" 가이드라인 포함
- **[과도한 정보 리스크]** → 너무 길면 Claude Code의 컨텍스트 윈도우를 불필요하게 소비한다. 완화: 1-2페이지 이내로 유지, 코드에서 직접 읽을 수 있는 내용은 생략
- **[한국어 처리 리스크]** → 일부 AI 도구가 한국어 맥락을 영어보다 덜 정확하게 처리할 수 있음. 완화: Claude Code는 한국어 성능이 충분하며, 기술 용어는 영문 병기
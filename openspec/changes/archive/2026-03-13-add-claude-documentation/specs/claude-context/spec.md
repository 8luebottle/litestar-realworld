## ADDED Requirements

### Requirement: 프로젝트 개요 섹션
CLAUDE.md는 프로젝트의 이름, 목적, 기술 스택(Litestar, SQLAlchemy, PostgreSQL, msgspec)을 명시해야 한다(SHALL). RealWorld 스펙을 준수하는 Conduit API임을 명확히 기술해야 한다(MUST).

#### Scenario: Claude Code가 프로젝트를 처음 만났을 때
- **WHEN** Claude Code가 이 프로젝트에서 처음 작업을 시작할 때
- **THEN** CLAUDE.md의 프로젝트 개요를 읽고 스택과 목적을 즉시 파악할 수 있어야 한다

### Requirement: 아키텍처 맵 섹션
CLAUDE.md는 Conduit/ 하위 디렉토리 구조(routes, db, schemas, auth)와 각 모듈의 역할을 기술해야 한다(SHALL). 코드를 어디에 배치해야 하는지 판단할 수 있는 수준이어야 한다(MUST).

#### Scenario: 새로운 API 엔드포인트 추가 시
- **WHEN** Claude Code가 새로운 API 엔드포인트를 추가하라는 요청을 받을 때
- **THEN** 아키텍처 맵을 참조하여 라우트는 routes/, DB 쿼리는 db/, 스키마는 schemas/에 배치해야 한다

#### Scenario: 기존 코드 수정 시
- **WHEN** Claude Code가 기존 기능을 수정하라는 요청을 받을 때
- **THEN** 아키텍처 맵을 통해 관련 파일의 위치를 즉시 찾을 수 있어야 한다

### Requirement: 개발 환경 및 명령어 섹션
CLAUDE.md는 Docker 기반 개발 환경 설정 방법과 주요 Make 명령어(up, test, lint, down)를 기술해야 한다(SHALL). .env 설정 필요성을 명시해야 한다(MUST).

#### Scenario: 테스트 실행 시
- **WHEN** Claude Code가 테스트를 실행해야 할 때
- **THEN** CLAUDE.md에서 `make test` 명령어와 Docker Compose 기반 실행 방식을 확인할 수 있어야 한다

#### Scenario: 린트/타입 체크 실행 시
- **WHEN** Claude Code가 코드 품질 검사를 실행해야 할 때
- **THEN** `make lint` (ruff + ty) 명령어를 확인할 수 있어야 한다

### Requirement: 테스트 현황 섹션
CLAUDE.md는 현재 테스트 커버리지 현황과 갭을 기술해야 한다(SHALL). 어떤 컨트롤러에 테스트가 있고 없는지, happy path vs unhappy path 커버리지 상태를 명시해야 한다(MUST).

#### Scenario: 테스트 추가 작업 시
- **WHEN** Claude Code가 테스트를 추가하라는 요청을 받을 때
- **THEN** 테스트 현황을 참조하여 누락된 영역(tag 컨트롤러, happy path)을 우선 대상으로 식별할 수 있어야 한다

### Requirement: 코드 컨벤션 및 편집 가이드라인 섹션
CLAUDE.md는 코드 스타일(ruff), 타입 체크(ty), DB 쿼리 분리 패턴, RealWorld 스펙 준수 규칙을 기술해야 한다(SHALL). 프로젝트의 기존 패턴을 벗어나는 코드 생성을 방지해야 한다(MUST).

#### Scenario: 새로운 코드 생성 시
- **WHEN** Claude Code가 새로운 코드를 생성할 때
- **THEN** 편집 가이드라인을 따라 프로젝트 컨벤션에 맞는 코드를 생성해야 한다

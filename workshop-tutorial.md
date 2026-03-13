# Vibe Coding Migration Tutorial

기존 프로젝트에 AI 협업 환경을 구축하는 단계별 튜토리얼.
Litestar RealWorld (Conduit API) 프로젝트를 예시로 진행한다.

---

## Phase 1: 문서화 — AI가 프로젝트를 이해하게 만들기

### Step 1-1: CLAUDE.md 생성

```bash
# Claude Code에서 /init 실행
/init
```

**사용한 프롬프트**: `/init`

**결과물**: 프로젝트 루트에 `CLAUDE.md` 생성됨

**확인할 것**:
- 빌드/테스트 명령어가 정확한지 (`make up`, `make test`, `make lint`)
- 프로젝트 구조 설명이 실제와 일치하는지
- 누락된 컨텍스트가 있으면 직접 보완

**팁**: CLAUDE.md는 모든 세션에서 자동 로드되므로, 정확도가 중요하다. 잘못된 정보는 AI가 잘못된 코드를 생성하게 만든다.

### Step 1-2: 작업 계획 수립 & GitHub 이슈 등록

**사용한 프롬프트**:
```
이 프로젝트에 바이브 코딩을 도입하기 위한 작업 계획을 세워줘.
다음 4가지 영역을 에픽으로 하여 각각의 에픽에 대해 심층 인터뷰를 진행하고
그 결과에 따라 세부 계획을 작성해줘.

1. 문서화 — OpenSpec으로 프로젝트 스펙 문서화 + 스킬 생성
2. 테스트 구현 — 단위 테스트, E2E 테스트, 린트, Makefile 통합
3. CI/CD 파이프라인 — pre-commit hook, pre-push hook
4. 전환 계획서 — generate-plan 스킬로 migration-plan.md 생성
```

**결과물**: 4개 에픽 이슈가 GitHub에 등록됨

**문제 해결**: 포크 레포에서 Issues가 비활성화되어 있었음 → `gh repo edit --enable-issues`로 해결

**팁**:
- 이슈를 먼저 등록하면 이후 커밋에 이슈 번호를 넣어 추적할 수 있다
- "이슈 #3을 해결해줘"처럼 구체적 지시가 가능해진다
- 이슈 등록 전 반드시 내용을 검토할 것 — AI가 자동 등록하면 원치 않는 이슈가 생길 수 있다

### Step 1-3: OpenSpec 문서화

**사용한 프롬프트**:
```
OpenSpec을 사용해서 현재 프로젝트를 문서화 해줘.
각각의 파일은 클로드 스킬에서 참조하기 쉽게 200라인을 넘지 않도록 나눠서 작성해줘.
```

**워크플로우**: `/opsx:propose` → `/opsx:apply` → `/opsx:archive`

**결과물**:
```
openspec/specs/
├── user-auth/spec.md          (64 lines, 5 requirements, 12 scenarios)
├── profiles/spec.md           (42 lines, 3 requirements, 8 scenarios)
├── articles/spec.md           (79 lines, 6 requirements, 15 scenarios)
├── comments-and-favorites/spec.md (64 lines, 5 requirements, 12 scenarios)
└── tags/spec.md               (12 lines, 1 requirement, 2 scenarios)
```

**기능 분리 기준**:
- RealWorld 스펙의 엔드포인트 그룹핑과 일치
- comments와 favorites는 articles에 종속된 하위 리소스이므로 하나로 묶음
- 각 Scenario를 WHEN/THEN 형식으로 작성 → 테스트 케이스로 직접 변환 가능

**팁**: 컨트롤러 단위(4개)가 아닌 기능 단위(5개)로 분리하면 스펙이 비대해지지 않는다.

### Step 1-4: 문서 → 스킬 전환

**사용한 프롬프트**:
```
이 문서들을 활용해서 프로젝트에 유용한 스킬을 만들어줘.
스킬 작성은 Claude Code 공식 스킬 가이드를 따르고,
먼저 어떤 스킬이 이 프로젝트에 유용할지 제안해줘.
```

**결과물**: 3개 스킬 생성
| 스킬 | 용도 |
|------|------|
| `test-from-spec` | OpenSpec 시나리오 → pytest 테스트 자동 생성 |
| `add-endpoint` | RealWorld 스펙에 맞는 새 엔드포인트 추가 |
| `validate-spec` | 스펙과 코드 구현 일치 여부 검증 |

**팁**: 문서는 AI가 "읽는 것", 스킬은 AI가 "활용하는 것" — 문서화 후 반드시 스킬로 전환

---

## Phase 2: 테스트 구현 — AI 작업의 안전망 만들기

### Step 2-1: 단위 테스트 생성

**사용한 프롬프트**:
```
이 프로젝트에 단위 테스트를 작성해줘.
단위테스트는 OpenSpec으로 생성된 핵심 요구사항을 커버해야 해.
테스트 Best Practice를 참고하여 진행해줘.
```

**적용한 Best Practices**:
- 테스트 격리: `uuid4().hex[:8]`로 고유 데이터 생성, 테스트 간 의존성 제거
- Arrange-Act-Assert 패턴
- 하나의 테스트 = 하나의 동작 검증
- session scope client 유지 (DB 연결 비용), 데이터는 고유값으로 격리

**결과물**: 5개 테스트 파일 신규 생성
```
tests/test_routes/
├── test_user_happy_path.py              (5 tests)
├── test_article_happy_path.py           (9 tests)
├── test_comments_favorites_happy_path.py (7 tests)
├── test_profile_happy_path.py           (5 tests)
└── test_tag_controller.py               (3 tests)  ← 완전 신규
```

**문제 해결**: Litestar는 POST → 201, DELETE → 204를 기본 반환함. `HTTP_200_OK` 대신 `HTTP_201_CREATED`, `HTTP_204_NO_CONTENT` 사용.

**팁**: 프레임워크의 기본 HTTP 상태 코드를 먼저 파악하고 테스트를 작성할 것

### Step 2-2: E2E 테스트 생성

**사용한 프롬프트**:
```
핵심 사용자 시나리오에 대한 E2E 테스트를 작성해줘.
```

**결과물**: `test_e2e_scenarios.py` (3 tests)
- `test_full_user_lifecycle`: 등록 → 로그인 → 조회 → 업데이트
- `test_article_publish_and_interact`: 글 작성 → 팔로우 → 피드 → 댓글 → 즐겨찾기 → 삭제
- `test_article_update_flow`: 작성 → 수정 → 수정 확인

### Step 2-3: 린트 설정 & Step 2-4: Makefile 통합

**기존 설정**: ruff (린트/포맷) + ty (타입 체크) 이미 존재

**추가한 것**: `make check` 타겟 (lint + test 통합)

```makefile
check: lint test
```

**최종 Makefile 명령어**:
| 명령어 | 용도 |
|--------|------|
| `make test` | 테스트 실행 (Docker) |
| `make lint` | ruff + ty |
| `make check` | lint + test 통합 실행 |
| `make ruff` | ruff check --fix && format |

---

## Phase 3: CI/CD — 품질 게이트 구축

### Step 3-1: pre-commit hook

**설정**: `.git/hooks/pre-commit`
- `make lint` 실행 → 실패 시 커밋 차단
- `make test` 실행 → 실패 시 커밋 차단

### Step 3-2: pre-push hook

**설정**: `.git/hooks/pre-push`
- `make test` 실행 → 실패 시 푸시 차단

**중요**: Git Hooks가 커밋을 막으면 `--no-verify`로 우회하지 말고 테스트를 수정할 것.

---

## 최종 결과

| 항목 | Before | After |
|------|--------|-------|
| AI 컨텍스트 | 없음 | CLAUDE.md + OpenSpec 5개 스펙 |
| 스킬 | 없음 | 3개 (test-from-spec, add-endpoint, validate-spec) |
| 테스트 | 55개 (unhappy만) | 93개 (happy + unhappy + E2E) |
| 커버리지 영역 | 3/4 컨트롤러 | 4/4 컨트롤러 + E2E 시나리오 |
| 품질 게이트 | 없음 | pre-commit (lint+test), pre-push (test) |
| 실행 명령어 | `make test` only | `make test`, `make lint`, `make check` |

---

## 다른 프로젝트에 적용할 때의 팁

1. **CLAUDE.md부터 시작**: `/init`으로 생성 후 반드시 검토. 이것이 모든 AI 작업의 기반
2. **이슈 먼저 등록**: 작업 추적과 AI 지시에 모두 유용
3. **스펙 → 테스트 순서**: 스펙이 있어야 올바른 테스트를 생성할 수 있음
4. **프레임워크 특성 파악**: HTTP 상태 코드, 인증 방식 등 프레임워크 기본 동작을 먼저 이해
5. **Docker 환경 고려**: 로컬 도구와 Docker 내부 도구의 경로 차이에 주의
6. **Git Hooks는 우회하지 말 것**: 품질 게이트의 의미를 지키는 것이 핵심

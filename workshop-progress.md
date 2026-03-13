# 바이브 코딩 워크숍 진행 가이드

> 이 문서는 `litestar-realworld` 프로젝트 디렉토리에서 Claude Code 세션을 열고, 각 단계의 프롬프트를 순서대로 실행하기 위한 가이드입니다.

## 사전 준비 (완료)

다음 항목은 이미 완료되었습니다:

- [x] 프로젝트 클론 (`git clone https://github.com/Isgotkowitz/litestar-realworld`)
- [x] OpenSpec 초기화 (`openspec init --tools claude`)
- [x] CLAUDE.md 생성 (프로젝트 루트)
- [x] GitHub 이슈 등록 (#7 문서화, #8 테스트, #9 CI/CD, #10 전환 계획서)
- [x] OpenSpec change `add-claude-documentation` 생성 (proposal, specs, design, tasks 완료)

---

## 주의사항

- 반드시 `litestar-realworld` 디렉토리에서 Claude Code를 실행할 것
- 각 단계 완료 후 `/compact` 또는 `/clear`로 컨텍스트를 정리하면 좋음
- YOLO 모드: `claude --dangerously-skip-permissions` (실습 전용)

---

## Step 1-4: OpenSpec 프로젝트 기능 문서화 (이슈 #7)

### 목적
프로젝트의 모든 기능을 스펙 문서로 작성한다. 이 스펙이 이후 테스트 작성과 전환 계획서의 **단일 진실 공급원(Source of Truth)**이 된다.

### 프롬프트

```
/opsx:propose "project-feature-specs"
```

> `/opsx:propose`가 자동으로 proposal → specs → design → tasks를 생성합니다.
> 생성 과정에서 질문이 나오면 다음을 참고하여 답변하세요:
> - 문서화 범위: 인증, 글(CRUD), 댓글, 태그, 프로필, 팔로우, 즐겨찾기 — 전체 기능
> - 각 spec.md는 200라인 이내로 작성
> - WHEN/THEN 시나리오 포함

### 완료 후 확인

```bash
openspec status --change "project-feature-specs"
```

모든 아티팩트가 `done`이면 apply로 진행:

```
/opsx:apply "project-feature-specs"
```

### apply 완료 후 아카이브

```
/opsx:archive "project-feature-specs"
```

> archive를 실행하면 `changes/`의 스펙이 `openspec/specs/`로 병합되어 Source of Truth가 됩니다.

---

## Step 1-5: 문서 → 스킬 전환 (이슈 #7)

### 목적
문서는 AI가 읽는 것, 스킬은 AI가 활용하는 것. 문서화된 스펙을 Claude Code 스킬로 전환한다.

### 프롬프트

```
이 문서들을 활용해서 프로젝트에 유용한 스킬을 만들어줘. 스킬 작성은 Claude Code 공식 스킬 가이드를 따르고, 먼저 어떤 스킬이 이 프로젝트에 유용할지 제안해줘. 스킬이 참조하는 문서들은 200라인을 넘지 않도록 해줘.
```

### 완료 후 확인
- `.claude/skills/` 하위에 스킬 파일 생성 확인
- 이슈 #7 닫기: `gh issue close 7`

---

## Step 2-1: 단위 테스트 생성 (이슈 #8)

### 목적
OpenSpec 스펙 기반으로 단위 테스트를 작성한다. 스펙에 정의된 시나리오가 테스트 케이스가 된다.

### 프롬프트

```
이 프로젝트에 단위 테스트를 작성해줘. 단위테스트는 OpenSpec 으로 생성된 핵심 요구사항을 커버해야 해. 단위 테스트 구현을 위한 심층 인터뷰를 진행하고 인터뷰 내용에 기반해서 테스트 코드를 작성해줘.
```

### 검증 패턴 (Human-in-the-loop)
AI가 테스트 작성 → 사람이 검토 → 승인 후 실행 → 결과 확인 → 수정 요청

---

## Step 2-2: E2E 테스트 생성 (이슈 #8)

### 목적
핵심 사용자 시나리오(회원가입→로그인→글작성→댓글→즐겨찾기)를 E2E 테스트로 작성한다.

### 프롬프트

```
핵심 사용자 시나리오에 대한 E2E 테스트를 작성해줘. 심층 인터뷰를 통해 테스트 사양을 정의해줘. 테스트 구현 후에는 테스트가 실제로 시나리오를 검증하는지 함께 검토해줘.
```

---

## Step 2-3: 린트 설정 (이슈 #8)

### 목적
프로젝트의 기존 코드 스타일을 분석하여 린트 규칙을 확정한다.

### 프롬프트

```
이 프로젝트에 맞는 린트를 설정해줘. 프로젝트의 기존 코드 스타일을 분석해서 규칙을 결정해줘.
```

---

## Step 2-4: Makefile 통합 (이슈 #8)

### 목적
테스트와 린트 명령어를 Makefile로 통합하여 `make test`, `make lint`, `make check`로 실행 가능하게 한다.

### 프롬프트

```
테스트와 린트 명령어를 Makefile로 통합해줘.
```

### 완료 후 확인

```bash
make test && make lint
```

- 이슈 #8 닫기: `gh issue close 8`

---

## Step 3-1: pre-commit hook (이슈 #9)

### 목적
커밋할 때마다 린트 체크와 단위 테스트가 자동 실행되도록 한다.

### 프롬프트

```
pre-commit hook을 설정해줘. 커밋할 때마다 린트 체크와 단위 테스트가 자동 실행되도록 해줘. Makefile의 make check 타겟을 활용해줘.
```

---

## Step 3-2: pre-push hook (이슈 #9)

### 목적
푸시할 때 E2E 테스트와 커버리지 체크가 실행되도록 한다.

### 프롬프트

```
pre-push hook을 설정해줘. 푸시할 때 E2E 테스트와 커버리지 체크(80% 이상)가 실행되도록 해줘.
```

---

## Step 3-3: 동작 확인 (이슈 #9)

### 프롬프트

```bash
# pre-commit 확인
git add -A && git commit -m "test: verify pre-commit hook"

# pre-push 확인
git push
```

> Git Hooks가 커밋을 막으면 `--no-verify`로 우회하지 말고 테스트를 수정하세요.

- 이슈 #9 닫기: `gh issue close 9`

---

## Step 4-1: 튜토리얼 문서 작성

### 목적
Claude Code 세션 로그를 기반으로 워크숍 전체 과정을 재현 가능한 튜토리얼로 변환한다.

### 프롬프트

```
~/.claude/projects/ 에서 이 프로젝트의 세션 로그를 찾아서 분석해줘. 오늘 워크숍에서 진행한 전체 과정을 바이브 코딩 마이그레이션 튜토리얼로 작성해줘. 튜토리얼에는 다음 내용이 포함되어야 해:
- 각 단계에서 사용한 프롬프트 원문
- AI의 주요 응답과 생성된 산출물
- 문제가 발생했을 때 어떻게 해결했는지
- 다른 프로젝트에 적용할 때의 팁
```

---

## Step 4-2: 전환 계획서 생성 (이슈 #10)

### 사전 준비

```bash
mkdir -p .claude/skills/generate-plan
# 강사 안내에 따라 3개 파일을 복사:
# SKILL.md, output-template.md, project-guidelines.md
```

### 프롬프트

```
이 프로젝트에 대한 바이브 코딩 전환 계획서를 만들어줘. generate-plan 스킬을 사용해서 진행해줘.
```

> 스킬이 자동으로 Phase 0(코드 스캔) → Phase 1(심층 인터뷰 3~5라운드) → Phase 2(분석 요약) → Phase 3(migration-plan.md 생성)을 진행합니다.
> **인터뷰 응답이 계획서 품질을 결정합니다. Phase 1 인터뷰까지는 반드시 완료하세요.**

- 이슈 #10 닫기: `gh issue close 10`

---

## 마무리: 작업 저장

### 프롬프트

```
오늘 워크숍에서 작업한 모든 변경사항을 커밋해줘. 커밋 메시지는 각 단계별로 의미 있게 나눠서 작성해줘. 변경사항이 많으면 논리적 단위로 분리해서 여러 커밋으로 만들어줘.
```

# Vibe Coding Migration Plan

**프로젝트**: litestar-realworld (Conduit API)
**작성일**: 2026-03-13
**상태**: Phase 1~3 완료, Phase 4 진행 중

---

## 1. 현재 상태 분석

### 1.1 프로젝트 개요
- **스택**: Litestar + SQLAlchemy (async) + PostgreSQL 16 + msgspec
- **규모**: Python 파일 21개, ORM 모델 7개, 컨트롤러 4개
- **인프라**: Docker Compose (app, test, postgres), Makefile

### 1.2 AI 협업 준비도 (Before)
| 항목 | 상태 |
|------|------|
| AI 컨텍스트 문서 | ❌ 없음 |
| 기능 스펙 | ❌ 코드가 곧 스펙 |
| 테스트 자동화 | 🔶 unhappy path만 (55개) |
| CI/CD | ❌ 없음 |
| 코드 품질 도구 | ✅ ruff + ty 설정됨 |

### 1.3 AI 협업 준비도 (After)
| 항목 | 상태 |
|------|------|
| AI 컨텍스트 문서 | ✅ CLAUDE.md |
| 기능 스펙 | ✅ OpenSpec 5개 영역 (20 requirements, 49 scenarios) |
| 테스트 자동화 | ✅ 93개 (happy + unhappy + E2E) |
| CI/CD | ✅ pre-commit + pre-push hooks |
| Claude Code 스킬 | ✅ 3개 (test-from-spec, add-endpoint, validate-spec) |

---

## 2. 마이그레이션 로드맵

### Phase 1: 문서화 (완료 ✅)
- [x] CLAUDE.md 생성 및 검증
- [x] OpenSpec으로 5개 기능 영역 스펙 문서화
- [x] Claude Code 스킬 3개 생성
- [x] GitHub 이슈 에픽 등록

**소요 시간**: ~30분
**핵심 산출물**: CLAUDE.md, openspec/specs/*.md, .claude/skills/*

### Phase 2: 테스트 (완료 ✅)
- [x] Happy path 단위 테스트 (29개 추가)
- [x] Tag 컨트롤러 테스트 (3개, 완전 신규)
- [x] E2E 시나리오 테스트 (3개)
- [x] Makefile 통합 (check = lint + test)

**소요 시간**: ~20분
**핵심 산출물**: 5개 테스트 파일, Makefile check 타겟

### Phase 3: CI/CD (완료 ✅)
- [x] pre-commit hook (lint + test)
- [x] pre-push hook (test)

**소요 시간**: ~5분
**핵심 산출물**: .git/hooks/pre-commit, .git/hooks/pre-push

### Phase 4: 지속적 개선 (진행 중)
- [x] 워크숍 튜토리얼 작성
- [x] 전환 계획서 생성
- [ ] 팀 내 바이브 코딩 파일럿 시작
- [ ] 커버리지 80% 목표 달성
- [ ] GitHub Actions CI 파이프라인 추가

---

## 3. 팀 도입 가이드

### 3.1 즉시 적용 가능한 항목
1. **CLAUDE.md**: 모든 팀 프로젝트에 `/init`으로 생성
2. **OpenSpec 스펙**: 핵심 기능 1개부터 시작
3. **테스트 자동화**: `test-from-spec` 스킬로 스펙 → 테스트 변환

### 3.2 단계적 도입 권장 순서
```
Week 1: CLAUDE.md 생성 + 기존 코드 이해
Week 2: 핵심 기능 1개 OpenSpec 문서화
Week 3: 해당 기능 테스트 자동화
Week 4: Git Hooks 설정 + 전체 팀 공유
```

### 3.3 주의사항
- **AI 결과물 검증**: AI가 생성한 코드/테스트는 반드시 사람이 검토
- **스펙 우선**: 코드 변경 전 스펙을 먼저 업데이트
- **점진적 도입**: 전체를 한번에 바꾸지 말고 기능 단위로 점진 적용
- **Git Hooks 우회 금지**: `--no-verify`는 품질 게이트를 무력화함

---

## 4. 리스크와 대응

| 리스크 | 영향도 | 대응 |
|--------|--------|------|
| 스펙-코드 불일치 | 높음 | `validate-spec` 스킬로 정기 검증 |
| AI 환각 (hallucination) | 높음 | 테스트 자동화로 검증, 스펙 기반 작업 |
| 문서 노후화 | 중간 | 코드 변경 시 스펙 함께 업데이트 규칙 |
| 팀원 저항 | 중간 | 파일럿 → 성공 사례 공유 → 확대 |
| Docker 환경 차이 | 낮음 | Makefile로 명령어 통일 |

---

## 5. 성공 지표

| 지표 | 현재 | 목표 (3개월) |
|------|------|-------------|
| 테스트 수 | 93개 | 150개+ |
| 테스트 커버리지 | ~60% | 80%+ |
| AI 생성 코드 채택률 | - | 70%+ |
| 코드 리뷰 시간 | - | 30% 감소 |
| 버그 발생률 | - | 20% 감소 |

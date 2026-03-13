---
name: validate-spec
description: 코드 변경 후 OpenSpec 스펙과 구현이 일치하는지 검증
user_invocable: true
---

# validate-spec

OpenSpec 스펙과 현재 코드 구현의 일치 여부를 검증합니다.

## 입력

`/validate-spec {capability}` 형식으로 호출합니다.
- capability: `user-auth`, `profiles`, `articles`, `comments-and-favorites`, `tags` 중 하나
- 생략 시 모든 스펙을 검증

## 절차

1. `openspec/specs/{capability}/spec.md` 읽기
2. 스펙의 각 Requirement와 Scenario를 코드와 대조:
   - 엔드포인트 존재 여부 (`Conduit/routes/`)
   - HTTP 메서드와 경로 일치
   - 인증 요구사항 (exclude_from_auth 설정)
   - 에러 응답 코드 (404, 403, 422 등)
   - 응답 형식 (response schema)
3. 불일치 항목을 보고:
   - **스펙에 있으나 코드에 없음** → 구현 필요
   - **코드에 있으나 스펙에 없음** → 스펙 업데이트 필요
   - **동작이 다름** → 코드 또는 스펙 수정 필요
4. 검증 결과 요약 출력

## 출력 형식

```
## 검증 결과: {capability}

### ✅ 일치 (N개)
- Requirement: {name} — 모든 시나리오 일치

### ⚠️ 불일치 (N개)
- Requirement: {name}
  - Scenario: {name} — {불일치 내용}

### 📝 권장 조치
- {조치 항목}
```

## 참조 문서

- 스펙: `openspec/specs/*/spec.md`
- 라우트: `Conduit/routes/`
- 스키마: `Conduit/schemas/`

---
name: add-endpoint
description: RealWorld 스펙에 맞는 새 API 엔드포인트를 route + query + schema 세트로 추가
user_invocable: true
---

# add-endpoint

새 API 엔드포인트를 프로젝트 아키텍처에 맞게 추가합니다.

## 입력

`/add-endpoint` 호출 후 어떤 엔드포인트를 추가할지 설명합니다.

## 절차

1. 사용자 요구사항 확인 (엔드포인트 경로, HTTP 메서드, 기능)
2. 관련 OpenSpec 스펙 확인 (`openspec/specs/*/spec.md`)
3. 아키텍처 규칙에 따라 코드 생성:
   - **Route handler** → `Conduit/routes/{controller}_controller.py`
   - **DB query** → `Conduit/db/{module}_queries.py` (컨트롤러에 직접 쿼리 작성 금지)
   - **Request schema** → `Conduit/schemas/request_schemas.py` (msgspec Struct)
   - **Response schema** → `Conduit/schemas/response_schemas.py` (msgspec Struct, camelCase rename)
   - **DB model** → `Conduit/db/models.py` (필요 시)
4. RealWorld 스펙 준수 확인:
   - 응답 형식: `{ resource: { ...fields } }` wrapper 패턴
   - 인증: JWT Bearer token, `exclude_from_auth=True` for public endpoints
   - 에러: 404 (NotFoundException), 403 (PermissionDeniedException), 422 (HTTPException)
5. `make ruff`로 린트 확인
6. 관련 OpenSpec 스펙 업데이트 제안

## 참조 문서

- 아키텍처: `CLAUDE.md` (코드 배치 규칙)
- 스펙: `openspec/specs/*/spec.md`
- 기존 패턴 참조: `Conduit/routes/article_controller.py`

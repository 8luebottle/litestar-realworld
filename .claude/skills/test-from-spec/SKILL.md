---
name: test-from-spec
description: OpenSpec 스펙의 시나리오를 기반으로 pytest 테스트 코드를 자동 생성
user_invocable: true
---

# test-from-spec

OpenSpec 스펙 파일의 Scenario를 pytest 테스트로 변환합니다.

## 입력

`/test-from-spec {capability}` 형식으로 호출합니다.
- capability: `user-auth`, `profiles`, `articles`, `comments-and-favorites`, `tags` 중 하나
- 생략 시 모든 스펙에 대해 테스트 생성

## 절차

1. `openspec/specs/{capability}/spec.md`를 읽어 모든 Scenario를 파싱
2. 기존 테스트 파일 확인 (`tests/test_routes/`)
3. 각 Scenario의 WHEN/THEN을 pytest 테스트 함수로 변환
4. 테스트 코드 규칙:
   - 파일: `tests/test_routes/test_{controller}_controller.py`
   - fixture: `tests/conftest.py`의 session scope fixture 활용
   - async def 사용 (asyncio_mode = "auto")
   - `httpx.AsyncClient` 기반 (Litestar AsyncTestClient)
   - 기존 unhappy path 테스트와 중복되지 않게 작성
5. 생성된 테스트를 `make test`로 실행하여 검증

## 참조 문서

- 스펙: `openspec/specs/*/spec.md`
- 기존 테스트: `tests/test_routes/`
- 테스트 설정: `tests/conftest.py`
- 프로젝트 컨텍스트: `CLAUDE.md`

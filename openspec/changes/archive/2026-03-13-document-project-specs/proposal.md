## Why

이 프로젝트에는 RealWorld 스펙에 기반한 기능별 상세 명세가 없다. 현재 코드가 곧 스펙이지만, AI 도구가 테스트를 생성하거나 기능을 확장할 때 "무엇이 올바른 동작인지" 판단할 기준이 없다. OpenSpec으로 기능별 스펙을 문서화하면, 이후 테스트 구현과 CI/CD 구축의 단일 진실 공급원(Source of Truth)이 된다.

## What Changes

- RealWorld Conduit API의 5개 핵심 기능 영역을 OpenSpec 스펙으로 문서화
- 각 스펙은 200라인 이내로 유지하여 클로드 스킬에서 참조하기 쉽게 분리
- `openspec/specs/` 디렉토리에 기능별 `spec.md` 생성

## Capabilities

### New Capabilities
- `user-auth`: 사용자 등록, 로그인, 현재 사용자 조회, 프로필 업데이트, JWT 인증
- `profiles`: 사용자 프로필 조회, 팔로우/언팔로우
- `articles`: 글 CRUD, 글 목록 조회 (필터링/페이지네이션), 피드
- `comments-and-favorites`: 댓글 CRUD, 글 즐겨찾기/해제
- `tags`: 태그 목록 조회

### Modified Capabilities

(없음 — 기존 스펙 없이 신규 문서화)

## Impact

- **신규 파일**: `openspec/specs/` 하위 5개 기능별 `spec.md`
- **코드 변경**: 없음 — 순수 문서 추가
- **의존성 변경**: 없음
- **후속 작업**: 이 스펙이 단위 테스트·E2E 테스트 작성과 스킬 생성의 기반이 됨

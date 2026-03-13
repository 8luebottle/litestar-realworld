## ADDED Requirements

### Requirement: 태그 목록 조회
시스템은 등록된 모든 태그의 목록을 조회할 수 있어야 한다(SHALL). 인증 없이 접근 가능하다(MUST).

#### Scenario: 태그 목록 조회 성공
- **WHEN** `GET /api/tags` 요청 시
- **THEN** 200 응답과 `{ tags: ["tag1", "tag2", ...] }` 반환

#### Scenario: 태그가 없을 때
- **WHEN** 등록된 태그가 없는 상태에서 `GET /api/tags` 요청 시
- **THEN** 200 응답과 `{ tags: [] }` 반환

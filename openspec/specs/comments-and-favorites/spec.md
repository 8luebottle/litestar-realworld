## ADDED Requirements

### Requirement: 댓글 작성
인증된 사용자는 글에 댓글을 작성할 수 있어야 한다(SHALL). 댓글 본문(body)은 필수이다(MUST).

#### Scenario: 댓글 작성 성공
- **WHEN** 인증된 사용자가 `POST /api/articles/{slug}/comments`에 `{ comment: { body } }`를 포함하여 요청 시
- **THEN** 200 응답과 `{ comment: { id, createdAt, updatedAt, body, author } }` 반환

#### Scenario: 존재하지 않는 글에 댓글 작성
- **WHEN** 존재하지 않는 slug의 글에 댓글 작성 요청 시
- **THEN** 404 응답 반환

### Requirement: 댓글 목록 조회
시스템은 글의 댓글 목록을 조회할 수 있어야 한다(SHALL). 인증 없이 접근 가능하다(MUST). 인증된 사용자가 요청하면 댓글 작성자의 팔로우 여부를 포함해야 한다(SHALL).

#### Scenario: 댓글 목록 조회 성공
- **WHEN** `GET /api/articles/{slug}/comments` 요청 시
- **THEN** 200 응답과 `{ comments: [{ id, createdAt, updatedAt, body, author }] }` 반환

#### Scenario: 댓글 없는 글 조회
- **WHEN** 댓글이 없는 글에 `GET /api/articles/{slug}/comments` 요청 시
- **THEN** 200 응답과 `{ comments: [] }` 반환

#### Scenario: 존재하지 않는 글의 댓글 조회
- **WHEN** 존재하지 않는 slug로 `GET /api/articles/{slug}/comments` 요청 시
- **THEN** 404 응답 반환

### Requirement: 댓글 삭제
인증된 사용자는 자신이 작성한 댓글을 삭제할 수 있어야 한다(SHALL). 다른 사용자의 댓글은 삭제할 수 없다(MUST).

#### Scenario: 댓글 삭제 성공
- **WHEN** 댓글 작성자가 `DELETE /api/articles/{slug}/comments/{id}` 요청 시
- **THEN** 댓글이 삭제됨

#### Scenario: 다른 사용자의 댓글 삭제 시도
- **WHEN** 댓글 작성자가 아닌 사용자가 `DELETE /api/articles/{slug}/comments/{id}` 요청 시
- **THEN** 403 응답 반환

#### Scenario: 존재하지 않는 댓글 삭제
- **WHEN** 존재하지 않는 id로 `DELETE /api/articles/{slug}/comments/{id}` 요청 시
- **THEN** 404 응답 반환

### Requirement: 글 즐겨찾기
인증된 사용자는 글을 즐겨찾기할 수 있어야 한다(SHALL). 즐겨찾기 후 `favorited: true`와 증가된 `favoritesCount`를 반환해야 한다(MUST).

#### Scenario: 즐겨찾기 성공
- **WHEN** 인증된 사용자가 `POST /api/articles/{slug}/favorite` 요청 시
- **THEN** 200 응답과 `favorited: true`, `favoritesCount`가 1 증가한 글 정보 반환

#### Scenario: 존재하지 않는 글 즐겨찾기
- **WHEN** 존재하지 않는 slug로 `POST /api/articles/{slug}/favorite` 요청 시
- **THEN** 404 응답 반환

### Requirement: 글 즐겨찾기 해제
인증된 사용자는 즐겨찾기한 글을 해제할 수 있어야 한다(SHALL). 해제 후 `favorited: false`와 감소된 `favoritesCount`를 반환해야 한다(MUST).

#### Scenario: 즐겨찾기 해제 성공
- **WHEN** 인증된 사용자가 `DELETE /api/articles/{slug}/favorite` 요청 시
- **THEN** 200 응답과 `favorited: false`, `favoritesCount`가 1 감소한 글 정보 반환

#### Scenario: 존재하지 않는 글 즐겨찾기 해제
- **WHEN** 존재하지 않는 slug로 `DELETE /api/articles/{slug}/favorite` 요청 시
- **THEN** 404 응답 반환

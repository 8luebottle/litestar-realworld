## ADDED Requirements

### Requirement: 프로필 조회
시스템은 사용자명으로 프로필을 조회할 수 있어야 한다(SHALL). 인증 없이도 조회 가능하다(MUST). 인증된 사용자가 요청하면 팔로우 여부(`following`)를 포함해야 한다(SHALL).

#### Scenario: 비인증 사용자가 프로필 조회
- **WHEN** 인증 없이 `GET /api/profiles/{username}` 요청 시
- **THEN** 200 응답과 `{ profile: { username, bio, image, following: false } }` 반환

#### Scenario: 인증된 사용자가 팔로우 중인 프로필 조회
- **WHEN** 인증된 사용자가 팔로우 중인 사용자의 `GET /api/profiles/{username}` 요청 시
- **THEN** 200 응답과 `{ profile: { username, bio, image, following: true } }` 반환

#### Scenario: 인증된 사용자가 팔로우하지 않는 프로필 조회
- **WHEN** 인증된 사용자가 팔로우하지 않는 사용자의 `GET /api/profiles/{username}` 요청 시
- **THEN** 200 응답과 `{ profile: { username, bio, image, following: false } }` 반환

#### Scenario: 존재하지 않는 사용자 프로필 조회
- **WHEN** 존재하지 않는 username으로 `GET /api/profiles/{username}` 요청 시
- **THEN** 404 응답과 "No profile with username='{username}' found" 에러 반환

### Requirement: 사용자 팔로우
인증된 사용자는 다른 사용자를 팔로우할 수 있어야 한다(SHALL). 팔로우 성공 시 `following: true`인 프로필을 반환해야 한다(MUST).

#### Scenario: 팔로우 성공
- **WHEN** 인증된 사용자가 `POST /api/profiles/{username}/follow` 요청 시
- **THEN** 200 응답과 `{ profile: { username, bio, image, following: true } }` 반환

#### Scenario: 존재하지 않는 사용자 팔로우
- **WHEN** 존재하지 않는 username으로 `POST /api/profiles/{username}/follow` 요청 시
- **THEN** 404 응답 반환

### Requirement: 사용자 언팔로우
인증된 사용자는 팔로우 중인 사용자를 언팔로우할 수 있어야 한다(SHALL). 언팔로우 성공 시 `following: false`인 프로필을 반환해야 한다(MUST).

#### Scenario: 언팔로우 성공
- **WHEN** 인증된 사용자가 `DELETE /api/profiles/{username}/follow` 요청 시
- **THEN** 200 응답과 `{ profile: { username, bio, image, following: false } }` 반환

#### Scenario: 존재하지 않는 사용자 언팔로우
- **WHEN** 존재하지 않는 username으로 `DELETE /api/profiles/{username}/follow` 요청 시
- **THEN** 404 응답 반환

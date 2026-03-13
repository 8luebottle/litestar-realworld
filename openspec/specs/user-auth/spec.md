## ADDED Requirements

### Requirement: 사용자 등록
시스템은 이메일, 사용자명, 비밀번호로 새 사용자를 등록할 수 있어야 한다(SHALL). 비밀번호는 Argon2로 해싱하여 저장해야 한다(MUST). 등록 성공 시 JWT 토큰을 포함한 사용자 정보를 반환해야 한다(MUST).

#### Scenario: 등록 성공
- **WHEN** 유효한 email, username, password로 `POST /api/users` 요청 시
- **THEN** 201 응답과 함께 `{ user: { email, username, bio, image, token } }` 반환

#### Scenario: 이메일 중복
- **WHEN** 이미 등록된 이메일로 `POST /api/users` 요청 시
- **THEN** 422 응답과 "Username or email already in use" 에러 메시지 반환

#### Scenario: 사용자명 중복
- **WHEN** 이미 등록된 사용자명으로 `POST /api/users` 요청 시
- **THEN** 422 응답과 "Username or email already in use" 에러 메시지 반환

### Requirement: 사용자 로그인
시스템은 이메일과 비밀번호로 사용자를 인증할 수 있어야 한다(SHALL). 인증 성공 시 JWT 토큰을 포함한 사용자 정보를 반환해야 한다(MUST). Argon2 rehash가 필요한 경우 자동으로 수행해야 한다(SHALL).

#### Scenario: 로그인 성공
- **WHEN** 올바른 email, password로 `POST /api/users/login` 요청 시
- **THEN** 200 응답과 함께 `{ user: { email, username, bio, image, token } }` 반환

#### Scenario: 존재하지 않는 이메일
- **WHEN** 등록되지 않은 이메일로 `POST /api/users/login` 요청 시
- **THEN** 404 응답 반환

#### Scenario: 잘못된 비밀번호
- **WHEN** 올바른 이메일, 잘못된 비밀번호로 `POST /api/users/login` 요청 시
- **THEN** 404 응답 반환

### Requirement: 현재 사용자 조회
인증된 사용자는 자신의 정보를 조회할 수 있어야 한다(SHALL). JWT 토큰으로 인증하며 `GET /api/user` 엔드포인트를 사용한다.

#### Scenario: 인증된 사용자 조회
- **WHEN** 유효한 JWT 토큰으로 `GET /api/user` 요청 시
- **THEN** 200 응답과 함께 현재 사용자의 `{ user: { email, username, bio, image, token } }` 반환

#### Scenario: 인증 없이 조회
- **WHEN** JWT 토큰 없이 `GET /api/user` 요청 시
- **THEN** 401 응답 반환

### Requirement: 사용자 정보 업데이트
인증된 사용자는 자신의 email, username, password, image, bio를 업데이트할 수 있어야 한다(SHALL). 부분 업데이트를 지원해야 한다(MUST).

#### Scenario: 프로필 업데이트 성공
- **WHEN** 유효한 JWT 토큰으로 변경할 필드를 포함하여 `PUT /api/user` 요청 시
- **THEN** 200 응답과 함께 업데이트된 사용자 정보 반환

#### Scenario: 중복 이메일/사용자명으로 업데이트
- **WHEN** 다른 사용자가 사용 중인 email 또는 username으로 `PUT /api/user` 요청 시
- **THEN** 422 응답과 "Cannot use a username or email that is already in use" 에러 반환

### Requirement: JWT 인증
시스템은 `Authorization: Bearer <token>` 헤더로 JWT 인증을 수행해야 한다(MUST). 토큰 만료 시간은 15분이다(SHALL). 인증이 필요 없는 엔드포인트는 `exclude_from_auth`로 제외한다.

#### Scenario: 유효한 토큰
- **WHEN** 유효한 JWT 토큰이 Authorization 헤더에 포함된 요청 시
- **THEN** 요청이 정상 처리되고 `request.user`에 User 객체가 설정됨

#### Scenario: 만료된 토큰
- **WHEN** 만료된 JWT 토큰으로 인증이 필요한 엔드포인트에 요청 시
- **THEN** 401 응답 반환

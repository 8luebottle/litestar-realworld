## ADDED Requirements

### Requirement: 글 목록 조회
시스템은 글 목록을 조회할 수 있어야 한다(SHALL). 인증 없이 접근 가능하다(MUST). author, favorited, tag 필터와 limit/offset 페이지네이션을 지원해야 한다(SHALL).

#### Scenario: 전체 글 목록 조회
- **WHEN** `GET /api/articles` 요청 시
- **THEN** 200 응답과 `{ articles: [...], articlesCount }` 반환 (기본 limit=20, offset=0)

#### Scenario: 작성자로 필터링
- **WHEN** `GET /api/articles?author={username}` 요청 시
- **THEN** 해당 작성자의 글만 반환

#### Scenario: 즐겨찾기한 사용자로 필터링
- **WHEN** `GET /api/articles?favorited={username}` 요청 시
- **THEN** 해당 사용자가 즐겨찾기한 글만 반환

#### Scenario: 태그로 필터링
- **WHEN** `GET /api/articles?tag={tag}` 요청 시
- **THEN** 해당 태그를 포함한 글만 반환

#### Scenario: 페이지네이션
- **WHEN** `GET /api/articles?limit=5&offset=10` 요청 시
- **THEN** 10번째 이후 글 5개 반환

### Requirement: 글 피드 조회
인증된 사용자는 팔로우 중인 작성자들의 글 피드를 조회할 수 있어야 한다(SHALL). limit/offset 페이지네이션을 지원한다(SHALL).

#### Scenario: 피드 조회 성공
- **WHEN** 인증된 사용자가 `GET /api/articles/feed` 요청 시
- **THEN** 200 응답과 팔로우 중인 작성자들의 글 목록 반환

#### Scenario: 비인증 사용자 피드 접근
- **WHEN** 인증 없이 `GET /api/articles/feed` 요청 시
- **THEN** 401 응답 반환

### Requirement: 단일 글 조회
시스템은 slug로 단일 글을 조회할 수 있어야 한다(SHALL). 인증 없이 접근 가능하다(MUST). 응답에 body 필드를 포함해야 한다(MUST).

#### Scenario: 글 조회 성공
- **WHEN** `GET /api/articles/{slug}` 요청 시
- **THEN** 200 응답과 `{ article: { slug, title, description, body, tagList, createdAt, updatedAt, favorited, favoritesCount, author } }` 반환

#### Scenario: 존재하지 않는 글 조회
- **WHEN** 존재하지 않는 slug로 `GET /api/articles/{slug}` 요청 시
- **THEN** 404 응답 반환

### Requirement: 글 생성
인증된 사용자는 글을 생성할 수 있어야 한다(SHALL). title, description, body는 필수이며 tagList는 선택이다(MUST). slug는 title에서 자동 생성된다(SHALL).

#### Scenario: 글 생성 성공
- **WHEN** 인증된 사용자가 `POST /api/articles`에 title, description, body를 포함하여 요청 시
- **THEN** 200 응답과 생성된 글 정보 반환 (favoritesCount=0, favorited=false)

#### Scenario: 태그 포함 글 생성
- **WHEN** 인증된 사용자가 tagList를 포함하여 `POST /api/articles` 요청 시
- **THEN** 글이 생성되고 tagList에 지정한 태그들이 연결됨

### Requirement: 글 수정
인증된 사용자는 자신이 작성한 글을 수정할 수 있어야 한다(SHALL). title, description, body의 부분 업데이트를 지원한다(MUST).

#### Scenario: 글 수정 성공
- **WHEN** 글 작성자가 `PUT /api/articles/{slug}`에 변경할 필드를 포함하여 요청 시
- **THEN** 200 응답과 업데이트된 글 정보 반환

#### Scenario: 다른 사용자의 글 수정 시도
- **WHEN** 글 작성자가 아닌 사용자가 `PUT /api/articles/{slug}` 요청 시
- **THEN** 403 응답 반환

### Requirement: 글 삭제
인증된 사용자는 자신이 작성한 글을 삭제할 수 있어야 한다(SHALL). 삭제 시 연관된 댓글, 태그, 즐겨찾기도 cascade 삭제된다(MUST).

#### Scenario: 글 삭제 성공
- **WHEN** 글 작성자가 `DELETE /api/articles/{slug}` 요청 시
- **THEN** 글과 연관 데이터가 삭제됨

#### Scenario: 다른 사용자의 글 삭제 시도
- **WHEN** 글 작성자가 아닌 사용자가 `DELETE /api/articles/{slug}` 요청 시
- **THEN** 403 응답 반환

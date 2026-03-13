## Context

litestar-realworld는 RealWorld Conduit API를 Litestar 프레임워크로 구현한 프로젝트다. 현재 코드는 동작하지만 기능 명세가 문서화되어 있지 않다. AI 도구가 테스트를 생성하거나 기능을 확장할 때 참조할 스펙이 필요하다.

현재 상태:
- 4개 컨트롤러 (User, Article, Profile, Tag)
- 7개 ORM 모델 (User, Article, Comment, Tag, ArticleTag, UserFavorite, UserFollow)
- JWT 인증 (litestar-jwt)
- msgspec 기반 요청/응답 스키마

## Goals / Non-Goals

**Goals:**
- RealWorld 스펙에 기반한 5개 기능 영역의 상세 명세 작성
- 각 스펙 파일을 200라인 이내로 유지하여 스킬 참조에 최적화
- 테스트 케이스로 직접 변환 가능한 시나리오 정의

**Non-Goals:**
- 코드 변경 — 순수 문서화만 수행
- RealWorld 스펙 자체의 수정이나 확장
- 구현 세부사항 기술 — 스펙은 "무엇"을 정의, "어떻게"는 코드에 위임

## Decisions

### 1. 5개 기능 영역으로 분리

`user-auth`, `profiles`, `articles`, `comments-and-favorites`, `tags`로 분리한다. RealWorld 스펙의 엔드포인트 그룹핑과 일치시키되, comments와 favorites는 articles에 종속된 하위 리소스이므로 하나로 묶는다.

**대안 검토**: 컨트롤러 단위(4개)로 분리 → articles 컨트롤러에 댓글·즐겨찾기가 섞여 스펙이 비대해짐

### 2. 시나리오를 테스트 케이스로 매핑 가능하게 작성

각 Requirement의 Scenario를 WHEN/THEN 형식으로 작성하여, 이후 단위 테스트·E2E 테스트의 직접적인 입력으로 활용한다.

**대안 검토**: 자유 서술 형식 → 테스트 변환 시 다시 분석 필요

### 3. 한국어 작성, 기술 용어 영문 병기

CLAUDE.md와 동일한 언어 정책을 따른다. 워크숍 참가자 전원이 한국어 사용자이며, 엔드포인트/필드명 등 기술 용어는 영문 그대로 사용한다.

## Risks / Trade-offs

- **[스펙-코드 불일치 리스크]** → 코드를 직접 읽어 스펙을 작성하므로 현재 시점에서는 일치. 이후 코드 변경 시 스펙도 업데이트 필요
- **[200라인 제한으로 인한 세부사항 누락]** → 핵심 요구사항과 시나리오에 집중하고, 구현 세부사항은 코드에 위임
- **[RealWorld 스펙과의 차이]** → 현재 구현 기준으로 문서화하되, RealWorld 원본 스펙과 다른 부분은 명시

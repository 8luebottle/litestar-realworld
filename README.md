# ![RealWorld Example App](images/logo.png)

> ### [Litestar](https://litestar.dev) codebase containing real world examples (CRUD, auth, advanced patterns, etc) that adheres to the [RealWorld](https://github.com/gothinkster/realworld) spec and API.


### [Demo](https://demo.realworld.build/)&nbsp;&nbsp;&nbsp;&nbsp;[RealWorld](https://github.com/gothinkster/realworld)

This codebase demonstrates a fully fledged backend application built with **Litestar** including CRUD operations, authentication, routing, pagination, and more.

For more information on how this works with other frontends/backends, head over to the [RealWorld](https://github.com/gothinkster/realworld) repo.

# How it works

**Stack:**
- [Litestar](https://litestar.dev) - ASGI framework for routing and server
- [msgspec](https://jcristharif.com/msgspec/) - Fast serialization for request/response schemas
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM with PostgreSQL
- [pytest](https://pytest.org/) - Testing framework
- [ruff](https://github.com/astral-sh/ruff) - Linting and formatting
- [ty](https://github.com/astral-sh/ty) - Type checking

**Project structure:**
```
Conduit/
├── auth/       # Authentication logic
├── db/         # Database models and configuration
├── routes/     # API endpoints
├── schemas/    # Request/response schemas
├── exception_handlers.py  # Exception handlers
├── main.py     # Server startup logic
└── settings.py # Auth, server, and database settings

```

The test suite covers unhappy paths for each endpoint. Happy path testing uses the official [RealWorld Postman collection](Conduit.postman_collection.json).

# Getting started

**Prerequisites:** Docker and Make

1. **Set up environment variables:**
```shell
   cp .env.example .env
```

2. **Run tests:**
```shell
   make test
```

3. **Start the server:**
```shell
   make up
```

4. **Verify it's running:**
```shell
   make logs
```

The API will be available at `http://localhost:8000` (or check your `.env` for the configured port).

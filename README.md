# ![RealWorld Example App](images/logo.png)

> ### [Litestar](https://litestar.dev) codebase containing real world examples (CRUD, auth, advanced patterns, etc) that adheres to the [RealWorld](https://github.com/gothinkster/realworld) spec and API.


### [Demo](https://demo.realworld.build/)&nbsp;&nbsp;&nbsp;&nbsp;[RealWorld](https://github.com/gothinkster/realworld)


This codebase was created to demonstrate a fully fledged backend application built with **Litestar** including CRUD operations, authentication, routing, pagination, and more.

We've gone to great lengths to adhere to the **Litestar** community styleguides & best practices.

For more information on how to this works with other frontends/backends, head over to the [RealWorld](https://github.com/gothinkster/realworld) repo.


# How it works

This project uses the Litestar package to handle the routing and server creation. `msgspec` is used to define schemas for API requests and responses. SQLAlchemy is used to define the database models, and the database used in this project is PostgreSQL. There is a unit test suite which uses `pytest`, the codebase is formatted with `ruff` and type checked with `ty`.

The app lives within the `Conduit` directory, and is organized into `auth`, `db`, `routes`, and `schemas`.

The unit test suite is written to test the unhappy path of each API endpoint. To test the happy path, the excellent Postman tests provided by the Realworld project are used (see `Conduit.postman_collection.json`).


# Getting started

Ensure Docker and Make are installed. Create a `.env` file in the project's root directory to hold environment variables.

```shell
cat .env.example >> .env
```

To run tests, run:

```shell
make test
```

To run the server, run:
```shell
make up
```

To ensure the server has started correctly, run:
```shell
make logs
```

.PHONY: up down dev reload reset-db

up:
	docker compose up -d

down:
	docker compose down -v

reset-db:
	docker compose down -v
	docker compose up -d

dev:
	litestar run --reload

ruff:
	ruff check --fix && ruff format

reload: down up dev
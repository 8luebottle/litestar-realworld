.PHONY: up down build rebuild logs shell reset-db ruff ty

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

down-v:
	docker compose down -v

rebuild: down build up

logs:
	docker compose logs -f app

shell:
	docker compose exec app /bin/bash

reset-db: down-v up

ruff:
	ruff check --fix && ruff format

ty:
	ty check

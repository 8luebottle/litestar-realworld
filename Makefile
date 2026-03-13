.PHONY: up down build rebuild logs shell reset-db test

# App
build:
	docker compose build

up:
	docker compose up app -d

down:
	docker compose down --remove-orphans

down-v:
	docker compose down -v --remove-orphans

rebuild: down build up

# Test
test: down-v build
	docker compose run --rm test

# Other
logs:
	docker compose logs -f app

shell:
	docker compose exec app /bin/bash

reset-db: down-v build up


# CI
ruff:
	python3 -m ruff check --fix && python3 -m ruff format

ty:
	python3 -m ty check

lint: ruff ty

check: lint test

.PHONY: help up down logs shell migrate upgrade downgrade test test-clean env ui-install ui-start ui-dev ui-build ui-dev-start memgraph-image build jarvis

NEXT_PUBLIC_USER_ID=$(USER)
NEXT_PUBLIC_API_URL=http://localhost:8765

# Default target
help:
	@echo "Available commands:"
	@echo "  make env       - Copy .env.example to .env"
	@echo "  make up        - Start the containers"
	@echo "  make down      - Stop the containers"
	@echo "  make logs      - Show container logs"
	@echo "  make shell     - Open a shell in the api container"
	@echo "  make migrate   - Run database migrations"
	@echo "  make test      - Run tests in a new container"
	@echo "  make test-clean - Run tests and clean up volumes"
	@echo "  make ui-install - Install frontend dependencies"
	@echo "  make ui-start  - Start the frontend development server"
	@echo "  make ui-dev    - Install dependencies and start the frontend in dev mode"
	@echo "  make ui        - Install dependencies and start the frontend in production mode"
	@echo "  make memgraph-image - Pull Memgraph image for graph memory"

env:
	cd api && cp .env.example .env
	cd ui && cp .env.example .env

build: memgraph-image
	docker compose build

memgraph-image:
	docker pull memgraph/memgraph-mage:latest

up:
	NEXT_PUBLIC_USER_ID=$(USER) NEXT_PUBLIC_API_URL=$(NEXT_PUBLIC_API_URL) docker compose up

down:
	docker compose down -v
	rm -f api/openmemory.db

logs:
	docker compose logs -f

shell:
	docker compose exec api bash

upgrade:
	docker compose exec api alembic upgrade head

migrate:
	docker compose exec api alembic upgrade head

downgrade:
	docker compose exec api alembic downgrade -1

ui-dev:
	cd ui && NEXT_PUBLIC_USER_ID=$(USER) NEXT_PUBLIC_API_URL=$(NEXT_PUBLIC_API_URL) pnpm install && pnpm dev

jarvis: memgraph-image
	cp api/jarvis.env api/.env
	USER=joe NEXT_PUBLIC_USER_ID=joe NEXT_PUBLIC_API_URL=$(NEXT_PUBLIC_API_URL) docker compose up -d

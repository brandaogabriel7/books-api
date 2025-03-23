up:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
	$(MAKE) migrate

up-prod:
	docker compose up -d
	$(MAKE) migrate

down:
	docker compose down

rebuild:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build

rebuild-prod:
	docker compose up -d --build

logs:
	docker compose logs -f

logs-%:
	docker compose logs -f $(subst logs-,,$@)

format:
	docker compose exec web black .

test:
	docker compose exec web python -m pytest

shell-%:
	docker compose exec $(subst shell-,,$@) /bin/bash

migrate:
	docker compose exec web python manage.py migrate

seed-db: migrate
	docker compose exec web python manage.py seed_books

clean:
	docker compose down -v

help:
	@echo "Available commands:"
	@echo "  up               - Start all services"
	@echo "  up-prod          - Start all services in production mode"
	@echo "  down             - Stop all services"
	@echo "  rebuild          - Rebuild all services"
	@echo "  rebuild-prod     - Rebuild all services in production mode"
	@echo "  logs             - View logs for all services"
	@echo "  logs-<service>   - View logs for a specific service (e.g., logs-web)"
	@echo "  format           - Format code using Black"
	@echo "  test             - Run tests"
	@echo "  shell-<service>  - Open a shell in a specific service (e.g., shell-web)"
	@echo "  migrate          - Run migrations"
	@echo "  seed-db          - Seed the database with sample data"
	@echo "  clean            - Stop and remove all containers, networks, and volumes"
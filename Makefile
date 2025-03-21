up:
	docker compose up -d

up-dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

down:
	docker compose down

rebuild:
	docker compose up -d --build

rebuild-dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build

logs:
	docker compose logs -f

logs-%:
	docker compose logs -f $(subst logs-,,$@)

format:
	docker compose exec web black .

test:
	docker compose exec web python -m pytest

shell:
	docker compose exec web /bin/bash

migrate:
	docker compose exec web python manage.py migrate

clean:
	docker compose down -v

help:
	@echo "Available commands:"
	@echo "  up               - Start all services"
	@echo "  up-dev           - Start all services in development mode"
	@echo "  down             - Stop all services"
	@echo "  rebuild          - Rebuild and start all services"
	@echo "  rebuild-dev      - Rebuild and start all services in development mode"
	@echo "  logs             - View logs for all services"
	@echo "  logs-<service>   - View logs for a specific service (e.g., logs-web)"
	@echo "  format           - Format code using Black"
	@echo "  test             - Run tests"
	@echo "  shell            - Open a shell in the Django container"
	@echo "  migrate          - Run migrations"
	@echo "  clean            - Stop and remove all containers, networks, and volumes"

# Makefile for Django application with Docker Compose

# Start all services (Django, database, Redis)
up:
	docker-compose up -d

# Start all services (Django, database, Redis) in development mode
up-dev:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Stop all services
down:
	docker-compose down

# Rebuild and start all services
rebuild:
	docker-compose up -d --build

# Rebuild and start all services in development mode
rebuild-dev:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build

# View logs for all services
logs:
	docker-compose logs -f

# View logs for a specific service (e.g., django, db, redis)
logs-%:
	docker-compose logs -f $(subst logs-,,$@)

# Run Django management commands (e.g., make manage migrate)
manage:
	docker-compose exec web python manage.py $(filter-out $@,$(MAKECMDGOALS))

# Run tests
test:
	docker-compose exec web python -m pytest

# Open a shell in the Django container
shell:
	docker-compose exec web /bin/bash

# Run migrations
migrate:
	docker-compose exec web python manage.py migrate

# Create a superuser
createsuperuser:
	docker-compose exec web python manage.py createsuperuser

# Collect static files
collectstatic:
	docker-compose exec web python manage.py collectstatic --noinput

# Stop and remove all containers, networks, and volumes
clean:
	docker-compose down -v

# Help command to list all available commands
help:
	@echo "Available commands:"
	@echo "  up               - Start all services"
	@echo "  up-dev           - Start all services in development mode"
	@echo "  down             - Stop all services"
	@echo "  rebuild          - Rebuild and start all services"
	@echo "  rebuild-dev      - Rebuild and start all services in development mode"
	@echo "  logs             - View logs for all services"
	@echo "  logs-<service>   - View logs for a specific service (e.g., logs-django)"
	@echo "  manage <command> - Run Django management commands (e.g., make manage migrate)"
	@echo "  test             - Run tests"
	@echo "  shell            - Open a shell in the Django container"
	@echo "  migrate          - Run migrations"
	@echo "  createsuperuser  - Create a superuser"
	@echo "  collectstatic    - Collect static files"
	@echo "  clean            - Stop and remove all containers, networks, and volumes"

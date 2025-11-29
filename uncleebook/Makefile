.PHONY: help build-dev build-prod up-dev up-prod down-dev down-prod logs migrate shell test clean

help:
	@echo "Uncle E-Book Docker Commands"
	@echo "============================"
	@echo "Development Commands:"
	@echo "  make build-dev    - Build development Docker images"
	@echo "  make up-dev       - Start development environment"
	@echo "  make down-dev     - Stop development environment"
	@echo "  make logs-dev     - View development logs"
	@echo "  make shell-dev    - Access Django shell in dev container"
	@echo ""
	@echo "Production Commands:"
	@echo "  make build-prod   - Build production Docker images"
	@echo "  make up-prod      - Start production environment"
	@echo "  make down-prod    - Stop production environment"
	@echo "  make logs-prod    - View production logs"
	@echo "  make shell-prod   - Access Django shell in prod container"
	@echo ""
	@echo "Utility Commands:"
	@echo "  make migrate-dev  - Run migrations in development"
	@echo "  make migrate-prod - Run migrations in production"
	@echo "  make test         - Run tests"
	@echo "  make clean        - Clean up Docker resources"

# Development Commands
build-dev:
	docker-compose --profile dev build

up-dev:
	docker-compose --profile dev up -d
	@echo "Development server running at http://localhost:8000"

down-dev:
	docker-compose --profile dev down

logs-dev:
	docker-compose --profile dev logs -f web-dev

shell-dev:
	docker-compose --profile dev exec web-dev python manage.py shell

bash-dev:
	docker-compose --profile dev exec web-dev bash

migrate-dev:
	docker-compose --profile dev exec web-dev python manage.py makemigrations
	docker-compose --profile dev exec web-dev python manage.py migrate

# Production Commands
build-prod:
	docker-compose --profile prod build

up-prod:
	docker-compose --profile prod up -d
	@echo "Production server running behind Nginx at http://localhost"

down-prod:
	docker-compose --profile prod down

logs-prod:
	docker-compose --profile prod logs -f web-prod

shell-prod:
	docker-compose --profile prod exec web-prod python manage.py shell

bash-prod:
	docker-compose --profile prod exec web-prod bash

migrate-prod:
	docker-compose --profile prod exec web-prod python manage.py makemigrations
	docker-compose --profile prod exec web-prod python manage.py migrate

# Utility Commands
test:
	docker-compose --profile dev exec web-dev python manage.py test

createsuperuser-dev:
	docker-compose --profile dev exec web-dev python manage.py createsuperuser

createsuperuser-prod:
	docker-compose --profile prod exec web-prod python manage.py createsuperuser

clean:
	docker-compose --profile dev down -v
	docker-compose --profile prod down -v
	docker system prune -f

restart-dev:
	docker-compose --profile dev restart web-dev

restart-prod:
	docker-compose --profile prod restart web-prod

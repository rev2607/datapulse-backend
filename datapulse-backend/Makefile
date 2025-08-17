.PHONY: help install test run clean docker-build docker-run

help: ## Show this help message
	@echo "DataPulse Backend - Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements.txt
	pip install pytest black isort flake8 mypy

test: ## Run tests
	pytest tests/ -v

test-cov: ## Run tests with coverage
	pytest tests/ --cov=app --cov-report=html

run: ## Run the application
	python run.py

run-dev: ## Run the application in development mode
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

clean: ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +

format: ## Format code with black and isort
	black app/ tests/
	isort app/ tests/

lint: ## Run linting checks
	flake8 app/ tests/
	mypy app/

docker-build: ## Build Docker image
	docker build -t datapulse-backend .

docker-run: ## Run Docker container
	docker run -p 8000:8000 datapulse-backend

docker-stop: ## Stop Docker container
	docker stop $$(docker ps -q --filter ancestor=datapulse-backend)

setup: install ## Setup the project (install dependencies)
	@echo "Setup complete! Run 'make run' to start the application."

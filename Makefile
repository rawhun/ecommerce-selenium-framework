.PHONY: help install test test-smoke test-parallel test-headless clean report lint format

help:
	@echo "Available commands:"
	@echo "  make install        - Install dependencies"
	@echo "  make test          - Run all tests"
	@echo "  make test-smoke    - Run smoke tests only"
	@echo "  make test-parallel - Run tests in parallel"
	@echo "  make test-headless - Run tests in headless mode"
	@echo "  make report        - Generate and serve Allure report"
	@echo "  make lint          - Run code linting"
	@echo "  make format        - Format code with black and isort"
	@echo "  make clean         - Clean generated files"

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

test:
	pytest tests/ -v

test-smoke:
	pytest tests/ -m smoke -v

test-parallel:
	pytest tests/ -n auto -v

test-headless:
	pytest tests/ --headless -v

test-chrome:
	pytest tests/ --browser chrome -v

test-firefox:
	pytest tests/ --browser firefox -v

report:
	pytest tests/ --alluredir=reports/allure
	allure serve reports/allure

lint:
	flake8 pages/ tests/ utils/ --max-line-length=100
	black --check pages/ tests/ utils/
	isort --check-only pages/ tests/ utils/

format:
	black pages/ tests/ utils/
	isort pages/ tests/ utils/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf reports/
	rm -rf htmlcov/
	rm -rf .coverage
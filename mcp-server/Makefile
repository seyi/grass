# Makefile for GRASS GIS MCP Server

.PHONY: help install install-dev test test-verbose test-coverage clean lint format check

# Default target
help:
	@echo "GRASS GIS MCP Server - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install        Install package"
	@echo "  make install-dev    Install package with dev dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  make test           Run all tests"
	@echo "  make test-verbose   Run tests with verbose output"
	@echo "  make test-coverage  Run tests with coverage report"
	@echo "  make test-unit      Run only unit tests"
	@echo "  make test-integration Run only integration tests"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint           Run linters (ruff)"
	@echo "  make format         Format code with black"
	@echo "  make check          Run all quality checks"
	@echo "  make typecheck      Run type checking with mypy"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          Remove generated files"
	@echo "  make clean-test     Remove test artifacts"

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

# Testing
test:
	pytest

test-verbose:
	pytest -v

test-coverage:
	pytest --cov=grass_mcp_server --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/index.html"

test-unit:
	pytest -m unit

test-integration:
	pytest -m integration

test-watch:
	pytest-watch

# Code quality
lint:
	ruff check .

format:
	black .
	ruff check --fix .

typecheck:
	mypy grass_mcp_server.py --strict

check: lint typecheck test

# Cleanup
clean: clean-test clean-build clean-pyc

clean-test:
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -f .coverage
	rm -f coverage.xml

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

clean-pyc:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type f -name '*.pyo' -delete

# Development
run:
	python grass_mcp_server.py

# Documentation
docs:
	@echo "Documentation:"
	@echo "  README.md - Main documentation"
	@echo "  USAGE.md - Usage guide"
	@echo "  tests/README.md - Test documentation"

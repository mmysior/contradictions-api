# Justfile for contradictions-api

# Default recipe - show available commands
default:
    @just --list

# Start the backend development server
dev:
    cd backend && uv run python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Start the backend production server
start:
    cd backend && uv run python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Install backend dependencies
install:
    cd backend && uv sync

# Run linting with ruff
lint:
    cd backend && uv run ruff check .

# Run formatting with ruff
format:
    cd backend && uv run ruff format .

# Run type checking
typecheck:
    cd backend && uv run mypy .

# Start with Docker Compose
docker-up:
    docker-compose up --build

# Stop Docker Compose
docker-down:
    docker-compose down

# Clean up Docker
docker-clean:
    docker-compose down -v --rmi all

# Run health check
health:
    curl -f http://localhost:8000/api/v1/utils/health-check/ || curl -f http://localhost:8000/
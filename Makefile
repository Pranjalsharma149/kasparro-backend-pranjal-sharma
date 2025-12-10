.PHONY: up down test clean

# P0.3 Requirement: "make up" must start everything
up:
	docker-compose up --build -d

# P0.3 Requirement: "make down" must stop everything
down:
	docker-compose down

# P0.4 Requirement: "make test" must run tests
test:
	docker-compose run --rm app pytest

# Helper to see logs
logs:
	docker-compose logs -f
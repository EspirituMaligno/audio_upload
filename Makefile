build:
	docker build -t backend:latest -f deployment/Dockerfile .

up:
	docker compose -f deployment/docker-compose.yaml up -d

up db:
	docker compose -f deployment/docker-compose.yaml up -d db

down db:
	docker compose -f deployment/docker-compose.yaml down db

down:
	docker compose -f deployment/docker-compose.yaml down

stop:
	docker compose -f deployment/docker-compose.yaml stop

restart:
	docker compose -f deployment/docker-compose.yaml down && docker compose -f deployment/docker-compose.yaml up -d

makemigrations:
	docker exec -it backend-api bash -c 'alembic revision --autogenerate -m "$(arg)"'

migrate:
	docker exec -it backend-api bash -c 'alembic upgrade head'

migrate-to:
	docker exec -it backend-api bash -c 'alembic upgrade $(arg)'

migrate-downgrade:
	docker exec -it backend-api bash -c 'alembic downgrade -1'

enter:
	docker exec -it server bash

build:
	docker compose -f "docker-compose.yml" -p "ezgame-playlist" up --build -d
start:
	docker compose -p "ezgame-playlist" start
stop:
	docker compose -p "ezgame-playlist" stop
restart: stop start
up:
	docker compose -f "docker-compose.yml" -p "ezgame-playlist" up -d
clean-data:
	docker system prune -a --volumes
make-migration:
	alembic revision --autogenerate
run-migration:
	alembic upgrade head

link:
	flake8
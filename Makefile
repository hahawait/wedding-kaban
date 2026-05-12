.PHONY: up down dev install logs ps help

# Поднять PostgreSQL в фоне
up:
	docker-compose up -d

# Остановить PostgreSQL
down:
	docker-compose down

# Запустить бэкенд (uvicorn с hot-reload)
dev:
	cd backend && uv run --with-requirements requirements.txt uvicorn main:app --reload --port 8000

# Установить зависимости в виртуальное окружение uv
install:
	cd backend && uv venv && uv pip install -r requirements.txt

# Посмотреть логи PostgreSQL
logs:
	docker-compose logs -f postgres

# Статус контейнеров
ps:
	docker-compose ps

# Старт с нуля: поднять БД + запустить сервер
start: up dev

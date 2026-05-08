# Свадьба Кирилла и Лены 💍

## Запуск локально

### 1. Поднять PostgreSQL (через Docker)
```bash
docker-compose up -d
```

### 2. Создать .env
```bash
cp backend/.env.example backend/.env
# отредактировать backend/.env при необходимости
```

### 3. Запустить бэкенд (через uv)
```bash
cd backend
uv run --with fastapi --with uvicorn --with sqlalchemy --with psycopg2-binary --with python-dotenv --with httpx \
  uvicorn main:app --reload --port 8000
```

Или через requirements.txt:
```bash
cd backend
uv pip install -r requirements.txt
uv run uvicorn main:app --reload --port 8000
```

Сайт доступен на: http://localhost:8000

### API

| Метод | URL | Описание |
|-------|-----|----------|
| POST | /api/register | Зарегистрировать гостя (ФИО + email + пожелание) |
| GET | /api/guests | Список всех гостей |
| GET | /api/health | Проверка работы сервера |

### Пример запроса
```bash
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Иванов Иван", "email": "ivan@mail.ru", "wish": "Совет да любовь!"}'
```

## Email (Resend)

Для отправки писем нужен аккаунт на [resend.com](https://resend.com):
1. Зарегистрироваться → создать API ключ
2. Добавить ключ в `backend/.env` → `RESEND_API_KEY=re_...`
3. Верифицировать домен (или использовать `onboarding@resend.dev` для тестов)

Без ключа письма просто не отправляются — регистрация всё равно сохраняется в БД.

# Alakris Lead Capture

Backend-first мини-прототип API для создания и просмотра заявок.
Код сделан в том же стиле, что и пример проекта: FastAPI, async SQLAlchemy,
Pydantic-схемы, отдельные слои `api`, `crud`, `models`, `schemas`, `core`.

## Что реализовано

- `POST /leads/` — создание заявки.
- `GET /leads/` — просмотр всех заявок, новые сверху.
- `GET /health` — быстрая проверка запуска.
- SQLite-хранение в `data/leads.db`.
- Серверная валидация обязательных полей.
- Проверка правила: должен быть указан email или телефон.
- Проверка согласия на обработку данных.

## Как запустить

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

После запуска:

- Swagger: http://127.0.0.1:8000/docs
- Healthcheck: http://127.0.0.1:8000/health

## Как проверить

Создать заявку:

```bash
curl -X POST http://127.0.0.1:8000/leads/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ivan",
    "email": "ivan@example.com",
    "phone": null,
    "company": "Acme",
    "comment": "Need demo",
    "consent": true
  }'
```

Посмотреть заявки:

```bash
curl http://127.0.0.1:8000/leads/
```

Проверить валидацию:

```bash
curl -X POST http://127.0.0.1:8000/leads/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "I",
    "company": "Acme",
    "comment": "No contact",
    "consent": false
  }'
```

Ожидаемо вернётся ошибка валидации.

## Допущения

- Это backend-first вариант, поэтому отдельный frontend не добавлялся.
- Служебный просмотр реализован через `GET /leads/` и Swagger.
- SQLite достаточно для прототипа и легко заменяется на PostgreSQL через
  `DATABASE_URL`.
- Компания сделана обязательной, потому что менеджеру важно понимать контекст
  заявки.
- Авторизация не реализована по условию задания.

## Как защитить в production

- Закрыть `GET /leads/` авторизацией для менеджеров.
- Добавить rate limit и антиспам-защиту на `POST /leads/`.
- Перейти на PostgreSQL и миграции Alembic.
- Добавить аудит доступа к персональным данным.
- Нормализовать телефон и хранить политику согласия/версию privacy policy.
- Добавить логирование ошибок и мониторинг.

## Что не делал

- Реальную CRM, Telegram, email-уведомления.
- Авторизацию.
- Сложную архитектуру и лишние абстракции.
- Полноценные автотесты.

## Время

Оценка: 2–3 часа с учетом ручной проверки и README.

## AI-гигиена

AI использован как помощник для ускорения черновой реализации и README.
Итоговая структура простая и повторяет стиль предоставленного проекта; код можно
объяснить на интервью.

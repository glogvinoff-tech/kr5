# KR5 FastAPI Task Manager

Контрольная работа №5: FastAPI-приложение для управления задачами, контейнеризация и WebSocket-чаты.

## Структура проекта

- `app/` — FastAPI-приложение.
- `tests/` — интеграционные тесты.
- `Dockerfile` — образ для приложения.
- `docker-compose.yml` — запуск сервиса `api`.
- `requirements.txt` — зависимости.
- `.dockerignore` — файлы, не попадающие в контейнер.
- `README.md` — инструкция по запуску.
- `pyproject.toml` — конфигурация Python-проекта.

## Запуск локально

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Приложение будет доступно на `http://127.0.0.1:8000`.

## Запуск тестов

```powershell
pytest
```

## Docker

```powershell
docker compose up --build
```

Сервис будет доступен на `http://localhost:8000`.

## Основные маршруты

- `GET /health` — проверка статуса.
- `POST /tasks` — создать задачу.
- `GET /tasks` — получить задачи текущего пользователя.
- `GET /tasks/{task_id}` — получить задачу по ID.
- `PATCH /tasks/{task_id}/status` — изменить статус.
- `DELETE /tasks/{task_id}` — удалить свою задачу.
- `GET /users/me` — получить текущего пользователя.
- `GET /admin/stats` — статистика задач (требуется роль `admin`).
- `DELETE /admin/tasks/{task_id}` — удалить задачу как админ.
- `GET /rooms/{room_id}/users` — список пользователей комнаты.
- `WS /ws/rooms/{room_id}?username=<username>` — WebSocket-комната.

## Пример заголовков авторизации

- `X-User-Id: 10`
- `X-User-Role: user` или `admin`

## Примеры

```powershell
curl -X POST http://127.0.0.1:8000/tasks \
  -H "X-User-Id: 10" \
  -H "Content-Type: application/json" \
  -d '{"title":"Подготовить тесты","priority":4,"status":"todo"}'
```

```powershell
curl http://127.0.0.1:8000/tasks -H "X-User-Id: 10"
```

## Проверка WebSocket

Открыть WebSocket-соединение на:

```text
ws://127.0.0.1:8000/ws/rooms/python?username=alice
```

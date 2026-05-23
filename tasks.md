# Задачи для контрольной работы №5

## Выполнено
- Реализовано FastAPI-приложение для управления задачами.
- Добавлена авторизация через заголовок `X-User-Id`.
- Реализованы маршруты `/tasks`, `/users`, `/admin`, `/health`, `/rooms` и WebSocket `/ws/rooms/{room_id}`.
- Добавлена модульная структура: `app/main.py`, `app/routers/`, `app/dependencies.py`, `app/schemas.py`, `app/storage.py`.
- Написаны интеграционные тесты для API и WebSocket.
- Подготовлена контейнеризация через `Dockerfile` и `docker-compose.yml`.

## Задачи

- [x] `POST /tasks` — создать задачу с `owner_id` из заголовка.
- [x] `GET /tasks` — получить список задач текущего пользователя.
- [x] `GET /tasks/{task_id}` — получить задачу, только если она принадлежит текущему пользователю.
- [x] `PATCH /tasks/{task_id}/status` — изменить статус задачи.
- [x] `DELETE /tasks/{task_id}` — удалить свою задачу.
- [x] `GET /health` — проверка состояния приложения.
- [x] `GET /rooms/{room_id}/users` — список активных пользователей комнаты.
- [x] `WS /ws/rooms/{room_id}?username=` — чат с уведомлениями и ограничением длины сообщений.
- [x] `GET /admin/stats` — статистика задач (доступно только админу).
- [x] `DELETE /admin/tasks/{task_id}` — админ может удалить любую задачу.
- [x] Тесты: `tests/test_tasks.py`, `tests/test_dependencies_and_routing.py`, `tests/test_websocket.py`.

## Запуск

1. Установите зависимости:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Запустите приложение:
   ```powershell
   uvicorn app.main:app --reload
   ```
3. Запустите тесты:
   ```powershell
   pytest
   ```
4. Запустите Docker:
   ```powershell
   docker compose up --build
   ```

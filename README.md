# Backend
## Установка для разработки:
### Требования
1) Необходим установленный python3.11
2) Для управления зависимостями используется poetry
3) Наличие базы данных postgres
   - Cоединение к бд
   - (Альтернативно) Docker, docker-compose
### Установка
1) Установка зависимостей:
```bash
poetry install --no-root
pip install pre-commit
```
2) Накатывание миграций:
```bash
alembic upgrade head
```
3) Установка pre-commit:
```bash
pre-commit install
```
4) Создание `.env` (пример заполнения лежит в `.env.template`)
```bash
cat .env.template > .env
```
### Запуск
1) Запуск API сервиса для бота
```bash
poetry run uvicorn backend.app:app --host 0.0.0.0 --port 8000
```
2) Запуск бота
...
### Тестирование
```bash
pytest .
```

# Memo Bot
Бот-помощник, для ведения записок через популярные мессенджеры.
### Доступные мессенджеры
- [ВК](https://vk.com/club224069843)
- [Телеграмм](https://t.me/huscker_memo_bot)
### Планируется добавить
- Discord
- Slack
# Структура проекта
## Backend
## API Документация
Актуальную документацию можно просмотреть в [OpenAPI схеме](https://petstore.swagger.io/?url=https://raw.githubusercontent.com/cockmasters/memo-bot/master/docs/openapi.json)
## Установка для разработки:
### Требования
1) Необходим установленный python3.11
2) Для управления зависимостями используется poetry
3) Наличие базы данных postgres
   - Доступ к бд postgres
   - Доступ к бд redis
   - (Альтернативно) Docker, docker-compose
### Установка
1) Установка pre-commit:
```bash
pip install pre-commit
pre-commit install
```
2) Установка зависимостей:
```bash
cd backend/
poetry install --no-root
```
3) Накатывание миграций:
```bash
alembic upgrade head
```
4) Создание `.env` (пример заполнения лежит в `.env.template`)
```bash
cat ../.env.template > .env
```
### Запуск
```bash
poetry run uvicorn app:app --host 0.0.0.0 --port 8000
```
### Тестирование
1) Запуск всех тестов
```bash
pytest .
```
## Frontend
### VK-bot
#### Установка для разработки:
##### Требования
1) Необходим установленный python3.11
2) Для управления зависимостями используется poetry
3) Наличие базы данных postgres
   - Доступ к api backend сервера
##### Установка
1) Установка pre-commit:
```bash
pip install
pre-commit install
```
2) Установка зависимостей:
```bash
cd vk/
poetry install --no-root
cd ../
```
3) Создание `.env` (пример заполнения лежит в `.env.template`)
```bash
cat .env.template > .env
```
### Запуск
```bash
poetry run vk/__main__.py
```
### Telegram-bot
#### Установка для разработки:
##### Требования
1) Необходим установленный python3.11
2) Для управления зависимостями используется poetry
3) Наличие базы данных postgres
   - Доступ к api backend сервера
##### Установка
1) Установка pre-commit:
```bash
pip install
pre-commit install
```
2) Установка зависимостей:
```bash
cd telegram/
poetry install --no-root
cd ../
```
3) Создание `.env` (пример заполнения лежит в `.env.template`)
```bash
cat .env.template > .env
```
### Запуск
```bash
poetry run telegram/__main__.py
```
## Небольшая витрина функционала
1) Пример добавления записки в вк боте \
![vk_showcase.png](docs%2Fstatic%2Fvk_showcase.png)
2) Приветствие в тг боте \
![tg_showcase.png](docs%2Fstatic%2Ftg_showcase.png)

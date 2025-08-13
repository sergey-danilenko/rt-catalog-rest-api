# Тестовое REST API приложение: Renter's Tenant Catalog

## Описание проекта

Система для получения данных организации через REST API:
- Получение полной информации по организации через ее идентификатор.
- Поиск организации по ее названию.
- Получение всех организаций, находящихся в конкретном здании:
  * По идентификатору здания
  * По адресу здания
- Получение списка организаций, находящихся в заданном радиусе/прямоугольной области
относительно указанной точке на карте.
- Получение списка всех организаций, которые относятся к указанному виду деятельности
- Поиск организаций по виду деятельности с учетом вложенных деятельностей.
- Ограничение вложенности поиска 3 уровнями

---

## Технологии

- Python 3.11+
- FastAPI
- SQLite + SQLAlchemy + Alembic
- Docker + Docker-compose

---

## Предварительные шаги
1. Клонируйте репозиторий:

```bash
git clone https://github.com/sergey-danilenko/rt-catalog-rest-api.git
```
```bash
cd rt-catalog-rest-api
```
2. Перед дальнейшими шагами:
- Переименуйте файл <b>dist.env</b> на <b>.env></b>
- Переименуйте каталог <b>/config_dist/</b> на <b>/config/</b>
Внутри этого каталога настройте при необходимости файл: <b>config/config.yml</b>
```yml
app:
  name: Renter's Tenant Catalog
bot:
  token: YOUR BOT TOKEN
db:
  type: sqlite
  connector: aiosqlite
  dbname: rt_catalog.sqlite3
  echo: false
  pool_pre_ping: false
api:
  auth:
    static_key: YourStaticKey
```

---

## Локальная Установка

1. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
```
##### Для Linux/macOS
```bash
source venv/bin/activate
```
##### Для Windows
```bash
venv\Scripts\activate
```
2. Установите зависимости:
```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

3. Выполните миграции Alembic:
```bash
alembic upgrade head
```
4. Заполните базу данных тестовыми данными:
```bash
python -m test_data.fill_test_data
```
---

## Запуск приложения

1. Запустите приложение:
```bash
python -m app.__main__
```

2. Откройте браузер и перейдите по адресу:
http://localhost:8000/docs — Swagger UI
[Подробнее](#api-documentation)
---

## Запуск через докер
1. Соберите и запустите контейнеры с помощью Docker Compose:
```bash
docker-compose up -d --build app
```
⚠️ Первый запуск требует выполнения миграций и заполнения тестовых данных. Для этого:
2. Выполните миграции:
```bash
docker-compose run --rm migrations
```
3. Заполните базу тестовыми данными::
```bash
docker-compose run --rm fill_test_data
```
## Запуск приложения

1. Запустите приложение:
```bash
docker-compose up -d app
```

2. Откройте браузер и перейдите по адресу:
http://localhost:8001/docs — Swagger UI.
[Подробнее](#api-documentation)

---

#### Управление контейнером приложения:
- Остановить:
```bash
docker compose stop app
```
- Запустить:
```bash
docker compose start app
```
- Перезапустить:
```bash
docker compose restart app
```
- Полное отключение и удаление всех контейнеров:
```bash
docker compose down
```
---

#### Примечания
- Локально база данных создаётся и используется из файла ./rt_catalog.sqlite3 в корне проекта.
- В Docker-приложении база данных монтируется в контейнер по пути /app/rt_catalog.sqlite3.
- Для корректной работы приложению передаются переменные окружения, например APP_PATH=/app.
- Если требуется изменить порт, используйте переменную окружения EXPOSED_PORT в файле .env
- ⚠️ Контейнеры migrations и fill_test_data НЕ запускаются автоматически,
чтобы избежать повторного заполнения данных и миграций при каждом старте.

---

## API Документация {#api-documentation}

Вся документация API доступна в Swagger UI:

http://localhost:8000/docs 
или
http://localhost:8001/docs

Перед тестированием запросом необходимо авторизоваться, указав токен из <b>config.yaml</b>
```yml
static_key: YourStaticKey
```

---
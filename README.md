# Backend Movies API

## Описание проекта
API для управления коллекцией фильмов. Позволяет создавать, получать, обновлять и удалять фильмы. Все маршруты защищены авторизацией через JWT.  

Предметная область: фильмы и их база данных.

## Стек технологий
- Python 3.13
- FastAPI
- SQLAlchemy
- PostgreSQL
- Uvicorn
- python-jose (JWT)

## Установка и запуск проекта

1. Клонировать репозиторий:

```
git clone <repository-url>
cd backend_movies
```

2. Создать виртуальное окружение и активировать:

```
python -m venv .venv
source .venv/bin/activate  # Linux / macOS
.venv\Scripts\activate     # Windows
```

3. Установить зависимости:

```
pip install -r requirements.txt
```

4. Запустить сервер:
```
uvicorn main:app --reload
```

API будет доступен по адресу: `http://127.0.0.1:8000`

Swagger UI доступен по адресу: `http://127.0.0.1:8000/docs`

## Модели

**Movie**

* `id` (int, PK)
* `title` (str, 2-100 символов)
* `director` (str)
* `description` (str, необязательное)
* `release_year` (int)
* `rating` (float, 0 < rating < 10)
* `available` (bool)

**User** (фейковый)

* username: `admin`
* password: `1234`

## Маршруты API

### Авторизация

**POST /auth/login**
Тело запроса (JSON):

```
{
  "username": "admin",
  "password": "1234"
}
```

Ответ:

```
{
  "access_token": "<JWT token>",
  "token_type": "bearer"
}
```

---

### Фильмы

Все маршруты требуют заголовок:

```
Authorization: Bearer <JWT token>
```

#### GET /movies

Получение списка всех фильмов.

Ответ 200 OK:

```json
[
  {
    "id": 1,
    "title": "Inception",
    "director": "Christopher Nolan",
    "description": "Mind-bending thriller",
    "release_year": 2010,
    "rating": 8.8,
    "available": true
  }
]
```

#### GET /movies/{id}

Получение одного фильма по ID.

* 200 OK — фильм найден.
* 404 Not Found — фильм не найден.

#### POST /movies

Создание нового фильма.
Тело запроса (JSON):

```json
{
  "title": "Interstellar",
  "director": "Christopher Nolan",
  "description": "Space drama",
  "release_year": 2014,
  "rating": 8.7,
  "available": true
}
```

Ответ:

* 201 Created — фильм создан.
* 400 Bad Request — синтаксическая ошибка.
* 422 Unprocessable Entity — данные не проходят валидацию.

#### PUT /movies/{id}

Полное обновление фильма.
Тело запроса: все поля модели.

Ответ:

* 200 OK — обновлено.
* 404 Not Found — фильм не найден.
* 400 Bad Request — некорректный JSON.

#### PATCH /movies/{id}

Частичное обновление фильма.
Тело запроса: только поля, которые нужно обновить.

Ответ:

* 200 OK — обновлено.
* 404 Not Found — фильм не найден.
* 400 Bad Request — недопустимые поля или значения.

#### DELETE /movies/{id}

Удаление фильма.

Ответ:

* 200 OK / 204 No Content — удалено.
* 404 Not Found — фильм не найден.

---

## Формат ошибок

Все ошибки возвращаются в едином JSON формате:

```json
{
  "status": 400,
  "error": "Bad Request",
  "message": "Описание ошибки"
}
```

Обрабатываются следующие коды:

* **400 Bad Request** — некорректный JSON, неверный параметр пути или запроса.
* **401 Unauthorized** — отсутствует или неверный токен.
* **403 Forbidden** — нет прав на действие.
* **404 Not Found** — сущность не найдена.
* **405 Method Not Allowed** — неподдерживаемый HTTP метод.
* **422 Unprocessable Entity** — JSON корректный, но данные не проходят валидацию.
* **500 Internal Server Error** — ошибка на сервере или БД.

---

## Примеры запросов через curl

**Получение списка фильмов**

```bash
curl -X GET "http://127.0.0.1:8000/movies" \
-H "Authorization: Bearer <JWT token>"
```

**Создание фильма**

```bash
curl -X POST "http://127.0.0.1:8000/movies" \
-H "Authorization: Bearer <JWT token>" \
-H "Content-Type: application/json" \
-d '{
  "title": "Interstellar",
  "director": "Christopher Nolan",
  "description": "Space drama",
  "release_year": 2014,
  "rating": 8.7,
  "available": true
}'
```

---

## Структура проекта

```
backend_movies/
│
├─ main.py            # Основной файл FastAPI
├─ models.py          # SQLAlchemy модели
├─ schemas.py         # Pydantic схемы
├─ crud.py            # Функции для работы с БД
├─ database.py        # Подключение к БД
├─ auth.py            # Авторизация и JWT
├─ dependencies.py    # Depends для токена
├─ requirements.txt
└─ README.md
```

## Проверка авторизации

* Все маршруты фильмов требуют токен.
* Попытка обращения без токена или с неверным токеном вернёт 401 Unauthorized.

## Валидация

* Строковые поля: обязательны и не пустые.
* Числовые поля: допустимые диапазоны (например, rating 0–10, release_year > 1800).
* Обязательные поля должны присутствовать.
* Булевы поля или даты проверяются на корректность.

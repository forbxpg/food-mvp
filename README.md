# 🍕 Проект Foodgram

Веб-приложение для публикации, поиска и управления кулинарными рецептами с системой социальных взаимодействий.

![Python](https://img.shields.io/badge/Python-3.9.12-blue?logo=python&logoColor=white&style=for-the-badge&logoSize=20)
![Django](https://img.shields.io/badge/Django-4.2.20-darkgreen?logo=django&logoColor=white&style=for-the-badge&logoSize=20)
![Django REST Framework](https://img.shields.io/badge/DRF-3.16.0-darkorange?logo=django&logoColor=white&style=for-the-badge&logoSize=20)
![Yandex Cloud](https://img.shields.io/badge/Yandex_CLoud-darkred?logo=yandexcloud&logoColor=white&style=for-the-badge&logoSize=20)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-blue?logo=postgresql&logoColor=white&style=for-the-badge&logoSize=20)
![Docker](https://img.shields.io/badge/docker-darkblue?logo=docker&logoColor=white&style=for-the-badge&logoSize=20)
![Nginx](https://img.shields.io/badge/nginx-darkgreen?logo=nginx&logoColor=white&style=for-the-badge&logoSize=20)
![Gunicorn](https://img.shields.io/badge/gunicorn-green?logo=gunicorn&logoColor=white&style=for-the-badge&logoSize=20)
![Django Unfold](https://img.shields.io/badge/UNFOLD-darkblue?&logoColor=white&style=for-the-badge&logoSize=20)
![Djoser](https://img.shields.io/badge/djoser-darkblue?logoColor=white&style=for-the-badge&logoSize=20)
![React](https://img.shields.io/badge/React-purple?logo=react&logoColor=white&style=for-the-badge&logoSize=20)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-black?logo=githubactions&logoColor=white&style=for-the-badge&logoSize=20)




## 🌟 Основные возможности

- Регистрация и авторизация пользователей.
- Создание, редактирование и удаление рецептов.
- Поиск рецептов по ингредиентам и названиям.
- Сохранение избранных рецептов и создание списка покупок.
- Возможность скачивания ингредиентов из списка покупок.
- Подписка на других пользователей и просмотр их рецептов.
- Интеграция с API для получения информации о рецептах.

## 🚀 Как запустить проект

1. ***Клонируйте репозиторий:***
```bash
   git clone https://github.com/forbxpg/foodgram.git
```

```tree
backend/
├── api/                            # API
│   ├── v1/                    
│   │   ├── serializers/            # Сериализаторы для API
│   │   │   ├── __init__.py
│   │   │   ...
│   │   ├── views/                  # Представления API
│   │   │   ├── __init__.py   
│   │   │    ... 
│   │   ├── __init__.py
│   │   ├── filters.py              # Фильтры
│   │   ├── routers.py              # Маршрутизаторы
│   │   ├── permissions.py          # Пользовательские права доступа
│   │   └── urls.py                 # URL-маршруты для API v1
│   ├── __init__.py
│   ├── apps.py                     # Конфигурация приложения API
│   └── urls.py                     # Основные URL-маршруты API
│
├── cart/                           # Приложение для списка покупок
│   ├── __init__.py                 
│   ├── models.py                   # Модели списка покупок
│   ...               
│
├── foodgram_backend/               # Основной проект
│   ├── __init__.py
│   ├── asgi.py                     # Конфигурация ASGI
│   ├── settings.py                 # Настройки проекта
│   ├── urls.py                     # Основные URL-маршруты проекта
│   └── wsgi.py                     # Конфигурация WSGI
│
├── recipes/                        # Приложение для ингредиентов
│   ├── __init__.py
│   ├── models.py                   # Модели ингредиентов
│   ├── admin.py                    # Настройки админки
│   └── management/                 # Команды управления
│       └── commands/               # Пользовательские команды
│           └── fill_db.py          # Команда для заполнения БД
│
├── favorite/                       # Приложение для рецептов
│   ├── __init__.py
│   ├── admin.py                    # Настройки админки
│   ├── models.py                   # Модели рецептов
│   ...
│
├── users/                          # Приложение для пользователей
│   ├── __init__.py
│   ├── admin.py                    # Настройки админки
│   └── models.py                   # Модели пользователей
│   ...
│
├── Dockerfile                      # Файл для сборки Docker образа
├── manage.py                       # Скрипт управления Django
└── requirements.txt                # Зависимости проекта

./frontend                           # Frontend часть проекта
./infra/
├── docker-compose.yml              # Файл для запуска Docker контейнеров
├── docker-compose.production.yml   # Файл для запуска Docker контейнеров в продакшене
├── nginx.conf                      # Конфигурация Nginx
./docs/
├── openapi-schema.yml              # Документация API
├── redoc.html                      # Документация API в формате JSON
.env.example                        # Шаблон .env файла
postman_collection.json             # Коллекция Postman для тестирования API
```


2. ***Создайте `.env`- файл по шаблону `.env.example`.***

3. ***Перейдите в директорию с docker-compose файлом:***

```bash
   cd foodgram/infra
```

4. ***Запустите контейнеры:***
```bash
   docker compose up -d
```

5. ***Выполните следующие команды:***
```bash
   docker compose exec backend python manage.py migrate                    # Применение миграций
   docker compose exec backend python manage.py collectstatic --noinput    # Сборка статических файлов
   docker compose exec backend python manage.py fill_db                    # Заполнение базы данных тестовыми данными
```
6. ***Создайте суперпользователя:***
```bash
   docker compose exec backend python manage.py createsuperuser
```
7. ***Откройте браузер и перейдите по адресу:***
```
   http://127.0.0.1:8000/
```
8. ***Изучите админку:***
```
   http://127.0.0.1:8000/admin/
```
9. ***Изучите документацию API:***
```
   http://127.0.0.1:8000/api/docs/
```

## 🔷 Примеры запросов

```bash
# Регистрация пользователей
curl -X POST "http://localhost:8000/api/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "new_user",
    "password": "securepassword123",
    "email": "user@example.com",
    "first_name": "Иван",
    "last_name": "Иванов"
  }'
```
```bash
# Получение токена
curl -X POST "http://localhost:8000/api/auth/token/login/" \
-H "Content-Type: application/json" \
  -d '{
    "password": "securepassword123",
    "email": "user@example.com",
  }'
```
```bash
# Подписка на пользователя
curl -X POST "http://localhost:8000/api/users/2/subscribe/" \
  -H "Authorization: Token your_access_token"
```

Другие примеры можно найти в ***документации*** по адресам: 

- http://127.0.0.1:8000/api/docs - если проект развернут локально
- https://food-mvp.myvnc.com/api/docs/ - готовый развернутый проект


## 🍓 Оригинальный проект

Проект был развернут с помощью Docker Compose и доступен по адресу: https://food-mvp.myvnc.com/

Использует следующие сервисы:

- **nginx** - веб-сервер для обработки запросов и статических файлов.
- **postgres** - база данных для хранения информации о пользователях и рецептах.
- **backend** - API-сервис, предоставляющий интерфейс для взаимодействия с бизнес-логикой.
- **frontend** - сервис для сборки статических файлов для backend-приложения.


## 🛠️ Примененные технологии


 - **Python**
 - **Django**
 - **Django REST Framework**
 - **PostgreSQL**
 - **Docker**
 - **Nginx**
 - **Gunicorn**
 - **Django**
 - **Djoser**
 - **React**
 - **GitHub Actions**

## 📈 Планы апгрейда проекта в будущем

- Добавление возможности указания калорийности блюд.
- Добавление `YouTube`-видеоплеера, если пользователь захотел указать ссылку на туториал.
- Добавление возможности лайкать блюда и оставлять комментарии под рецептами и под самими комментариями.
- Добавление возможности лайкать комментарии других пользователей.
- Добавление более защищенной аутентификации с помощью `JWT`-токенов.
- Подключение `Twilio` для регистрации и аутентификации с помощью телефона.
- Подключение `Celery`, `Redis` для рассылки `email` и фоновых тасок.
- Добавление кеширования запросов на страницах.
- Добавление телеграм бота с уведомлениями об акциях. (Optional)
- Подключение `Stripe`, `YouKassa` и системы подписок для получения доступа к Premium рецептам или что-то типа того)))

`Pull Request`'ы по внедрению новых фич приветствуются! 
Если у вас есть идеи по улучшению проекта, 
не стесняйтесь открывать `issue` или создавать `pull request`'ы. 
Я всегда рад новым идеям и предложениям!
   

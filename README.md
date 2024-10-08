# Cats DRF

## Описание проекта

Это RESTful API для управления информацией о кошках и их породах. API позволяет выполнять следующие операции:
- Регистрацию пользователей
- Авторизацию пользователей
- Выход из системы
- Получение списка пород
- Фильтрацию кошек по породе
- Получение списка кошек
- Добавление новых кошек
- Получение детальной информации о кошке
- Обновление информации о кошке
- Удаление кошки

## Технологии

- Python
- Django
- Django Rest Framework
- Docker
- Docker Compose
- Swagger/OpenAPI

## Установка

### Локальная установка

1. Установите Python и необходимые зависимости: `pip install -r requirements.txt`

2. Клонируйте репозиторий: `git clone https://github.com/your_username/cats_drf.git`

3. Настройте базу данных в settings.py.

4. Запустите сервер: `python manage.py runserver`

### Использование Docker Compose

1. Убедитесь, что у вас установлен Docker и Docker Compose.

2. Клонируйте репозиторий: `git clone https://github.com/your_username/cats_drf.git`

3. Перейдите в директорию проекта: `cd cats_drf`

4. Запустите контейнер: `docker-compose up --build`

5. Для остановки контейнеров: `docker-compose down`

## API Endpoints

### Регистрация пользователя
POST /register/


### Авторизация
POST /login/


### Выход из системы
POST /logout/


### Получение списка пород кошек
GET /kinds/


### Фильтрация кошек по породе
GET /cats/?kind=<имя_породы>


### Получение списка всех кошек
GET /cats/


### Добавление новой кошки
POST /cats/post/


### Получение информации о конкретной кошке
GET /cats/<pk>/


### Изменение информации о конкретной кошке
PUT /cats/put/<pk>/


### Удаление конкретной кошки
DELETE /cats/delete/<pk>/


## Пользовательские роли и разрешения

- GET запросы к любому endpoint'у доступны всем пользователям
- POST запросы к /register/, /login/ доступны всем пользователям
- POST запросы к кошкам доступны только авторизированным пользователям
- PUT и DELETE запросы к кошкам доступны только владельцам кошек

## Swagger/OpenAPI документация

API имеет интегрированную Swagger/OpenAPI документацию. Она доступна по адресу `/swagger/` после запуска сервера.
# Foodgram
![example workflow](https://github.com/tikhonov1994/foodgram-project-react/actions/workflows/main.yml/badge.svg)
### Описание
Проект **Foodgram** позволяет постить рецепты, делиться и скачивать списки продуктов
### Алгоритм регистрации пользователей:
Регистрация проходит на сайте, по форме регистрации
### Установка
Проект собран в Docker 20.10.06 и содержит четыре образа:
- backend - образ бэка проекта
- frontend - образ фронта проекта
- postgres - образ базы данных PostgreSQL v 12.04
- nginx - образ web сервера nginx
#### Команда клонирования репозитория:
```bash
git clone https://github.com/tikhonov1994/foodgram-project-react
```
#### Запуск проекта:
- [Установите Докер](https://docs.docker.com/engine/install/)
- Выполнить команду: 
```bash
docker pull tikhonov1994/foodgramm:latest
```
#### Первоначальная настройка Django:
```bash
- docker-compose exec backend python manage.py makemigrations users --noinput
- docker-compose exec backend python manage.py makemigrations recipes --noinput
- docker-compose exec backend python manage.py migrate --noinput
- docker-compose exec backend python manage.py collectstatic --no-input
```
#### Загрузка тестовой фикстуры ингредиентов и тегов в базу: 
```bash
- docker-compose exec backend python manage.py loaddata ingredients1.json 
```
#### Создание суперпользователя:
```bash
- docker-compose exec backend python manage.py createsuperuser
```
#### Заполнение .env:
Чтобы добавить переменную в .env необходимо открыть файл .env в корневой директории проекта и поместить туда переменную в формате имя_переменной=значение.
Пример .env файла:

```bash
DB_ENGINE=my_db
DB_NAME=db_name
POSTGRES_USER=my_user
POSTGRES_PASSWORD=my_pass
DB_HOST=db_host
DB_PORT=db_port
SECRET_KEY=my_secret_key
```
#### Документация:
Документацию к проекту можно посмотреть на странице api/docs. Администрирование доступно на странице /admin.
#### Автор:
Тихонов Илья. Задание было выполнено в рамках курса от Yandex Praktikum бэкенд разработчик.
#### Server address:
178.154.255.194
#### Superuser pass&email:

```bash
email: admin@admin.ru
pass: 123
```

# Inside
## Описание проекта
Тестовый проект
## Документация к API
API документация доступна по ссылке (создана с помощью redoc):
[http://127.0.0.1/redoc/](http://127.0.0.1/redoc/)
## Запуск проекта в Docker контейнере
* Установите Docker
* Параметры запуска описаны в файлах `docker-compose.yml`
* Запустите docker compose:
```bash
docker-compose up -d --build
```  

  > После сборки появятся 2 контейнера:
  > 1. контейнер базы данных **db**
  > 2. контейнер приложения **test_inside**

* Примените миграции:
```bash
docker-compose exec test_inside python manage.py migrate
```
* Создайте администратора:
```bash
docker-compose exec backend python manage.py createsuperuser
```
* Соберите статику:
```bash
docker-compose exec backend python manage.py collectstatic --noinput
```
* Дополнительные команды очистки докера:
```bash
docker stop $(docker ps -aq) && docker rm $(docker ps -aq)
docker rmi $(docker images -a -q)
docker volume prune
```
## Установка проекта локально
* Склонировать репозиторий и перейти в него в командной строке:
```bash
git clone https://github.com/edw125/TestInside.git
cd TestInside
```
* Cоздать и активировать виртуальное окружение:
```bash
python -m venv env
```
```bash
source env/bin/activate
```
* Cоздайте файл `.env` в корневой директории с содержанием:
```
SECRET_KEY = ${django-secret-key}
ALLOWED_HOSTS = ${localhost 127.0.0.1}
DB_ENGINE = django.db.backends.postgresql
DB_NAME = postgres
POSTGRES_USER = postgres
POSTGRES_PASSWORD = postgres
DB_HOST = db
DB_PORT = 5432
```
* Установить зависимости из файла requirements.txt:
```bash
pip install -r requirements.txt
```
* Выполните миграции:
```bash
python manage.py makemigrations
python manage.py migrate
```
* Соберите статику:
```bash
python manage.py collectstatic --noinput
```
* Запустите сервер:
```bash
python manage.py runserver
```
Готово!
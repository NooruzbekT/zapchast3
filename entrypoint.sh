#!/bin/bash

# Собираем статику без подтверждения
python3 manage.py collectstatic --noinput

# Выполняем миграции базы данных
python3 manage.py migrate

# Запускаем сервер Django
python3 manage.py runserver 0.0.0.0:8000
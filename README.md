# Команда номер: 11
Полноценный сервис уведомлений с админкой.

# Для того, чтобы запустить проект нужно:
1. В каталоге rabbitmq/example.env изменить переменные окружения на свои.
2. Переименовать файл rabbitmq/example.env в .env
3. В каталоге postgresql/example.env изменить переменные окружения на свои.
4. Переименовать файл postgresql/example.env в .env
5. В каталоге notifications/admin_panel/src/config/example.env изменить переменные окружения на свои.
6. Переименовать файл notifications/admin_panel/src/config/example.env в .env
7. В каталоге notifications/notifications_api/src/core/example.env изменить переменные окружения на свои.
8. Переименовать файл notifications/notifications_api/src/core/example.env в .env
9. Собрать статику командой: python manage.py collectstatic
10. В каталоге notifications/worker/src/core/example.env изменить переменные окружения на свои.
11. Переименовать файл notifications/worker/src/core/example.env в .env
10. В каталоге notifications/scheduler/src/core/example.env изменить переменные окружения на свои.
11. Переименовать файл notifications/scheduler/src/core/example.env в .env
13. Запустить контейнер notifications командой docker-compose -f docker-compose.yml up --build
14. При необходимости в контейнере админ панели сделать миграцию: python manage.py migrate
15. При необходимости в контейнере админ панели сделать супер пользователя: python manage.py createsuperuser

# Проектная работа 10 спринта

Проектные работы в этом модуле в команде. Задания на спринт вы найдёте внутри тем.

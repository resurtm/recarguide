.PHONY: default
default:
	@echo "no default action"

.PHONY: celery
celery:
	sleep 5
	celery worker --app recarguide --loglevel INFO

.PHONY: web
web:
	sleep 5
	# python manage.py makemigrations
	# python manage.py migrate
	python manage.py runserver 0.0.0.0:8080

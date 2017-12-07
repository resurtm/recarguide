.PHONY: default
default:
	@echo "no default action"

.PHONY: web
web:
	# wait for other services to start
	sleep 5

	python manage.py makemigrations
	python manage.py migrate
	python manage.py runserver 0.0.0.0:8080

.PHONY: celery
celery:
	# wait for other services to start
	sleep 5

	celery worker --app recarguide --loglevel INFO

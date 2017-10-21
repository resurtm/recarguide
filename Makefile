.PHONY: default celery flower webpack serve

default: serve

celery:
	celery -A recarguide worker -l info

flower:
	flower -A recarguide --port=5555

webpack:
	./node_modules/.bin/webpack --watch

serve:
	./manage.py runserver

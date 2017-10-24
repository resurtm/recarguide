.PHONY: default celery flower webpack serve tests

default: serve

celery:
	celery -A recarguide worker -l info

flower:
	flower -A recarguide --port=5555

webpack:
	./node_modules/.bin/webpack --watch

serve:
	python -Wall ./manage.py runserver

tests:
	python -Wall -m coverage run --source=recarguide ./manage.py test --keepdb
	coverage report > coverage.txt
	coverage html --directory=coverage

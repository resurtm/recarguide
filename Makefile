.PHONY: default celery flower webpack serve tests build

default: serve

celery:
	celery -A recarguide worker -l info

flower:
	flower -A recarguide --port=5555

webpack:
	node_modules/.bin/webpack --watch

serve:
	python -Wall ./manage.py runserver

tests:
	python -Wall -m coverage run --source=recarguide manage.py test --keepdb
	coverage report > coverage.txt
	coverage html --directory=coverage

build:
	# python setup.py sdist bdist_wheel
	# using workaround for this issue:
	# https://bitbucket.org/pypa/wheel/issues/99/cannot-exclude-directory
	python setup.py sdist
	pip wheel --verbose --no-index --no-deps --wheel-dir dist dist/*.tar.gz

.PHONY: all install coverage html travis test clean run serve-html static migrate fixtures

clean:
	find . -name "*.pyc" -type f -delete
	find . -name "__pycache__" -type d -exec rm -rf {} \;
	find . -name "*.egg-info" -type d -exec rm -rf {} \; || true
	rm -rf coverage_html_report .coverage

install:
	pip install -U setuptools
	pip install -q psycopg2
	pip install -r requirements.txt
	pip install anglerfish
	pip install css-html-js-minify
	pip install -U 'html5lib<0.99999999'
	pip install -U bleach
	pip install factory-boy
	pip install fake-factory

run:
	python manage.py runserver 0.0.0.0:8000

static:
	python manage.py collectstatic
	python manage.py generate_favicon --prefix \
	    'assets/img/favicon/' agcs/static/img/agcs.png
	cp -r ~/data/static_root/assets/img/favicon agcs/static/img

coverage:
	coverage run --source=landing,contact,metadata,agcs runtests.py

html: coverage
	coverage html

serve-html: html
	cd coverage_html_report && python2 -m SimpleHTTPServer 8002

travis: coverage

test:
	python runtests.py

migrate:
	python manage.py makemigrations
	python manage.py migrate

fixtures: migrate
	python manage.py loaddata \
	    landing/fixtures/* metadata/fixtures/* agcs/fixtures/*

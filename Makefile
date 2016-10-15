.PHONY: all install coverage html travis test clean run serve-html static migrate fixtures

clean:
	find . -name "*.pyc" -type f -delete
	find . -name "*,cover" -type f -delete
	find . -depth -name "__pycache__" -type d -exec rm -rf {} \;
	find . -depth -name "*.egg-info" -type d -exec rm -rf {} \; || true
	rm -rf coverage_html_report .coverage

install:
	pip install -U setuptools
	pip install -r requirements/dev.txt

run:
	python manage.py runserver 0.0.0.0:8000

static:
	python manage.py collectstatic
	python manage.py generate_favicon --prefix \
	    'assets/img/favicon/' agcs/static/img/agcs.png
	cp -r ~/data/static_root/assets/img/favicon agcs/static/img

coverage:
	coverage run runtests.py

html: coverage
	coverage html

serve-html: html
	cd coverage_html_report && python -m http.server 8002

travis: coverage

test:
	python runtests.py

migrate:
	python manage.py makemigrations
	python manage.py migrate

fixtures: migrate
	python manage.py loaddata \
	    landing/fixtures/* metadata/fixtures/* agcs/fixtures/*

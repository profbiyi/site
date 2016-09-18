.PHONY: all install upgrade coverage html travis test clean upload

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

coverage:
	coverage run --source=landing,contact,agcs runtests.py

html: coverage
	coverage html

travis: coverage

test:
	python runtests.py

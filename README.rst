========================
Main site Django_ project
========================

.. image:: https://img.shields.io/travis/alphageek-xyz/site.svg?style=flat-square
	:target: https://travis-ci.org/alphageek-xyz/site
	:alt: Build status

.. image:: https://img.shields.io/codecov/c/github/alphageek-xyz/site.svg?style=flat-square
	:target: https://codecov.io/gh/alphageek-xyz/site
	:alt: Codecov status

.. _Django: https://www.djangoproject.com/

The code provided in this repo will not run flawlessly without local modification and additional configuration; however, some parts may be useful references. Feel free to use it as a starting point for your own website.

To run locally, do the following (on Ubuntu 16.04):

#. Install system dependencies

   .. code-block:: bash

    sudo apt-get install git python3-pip postgresql-9.5
    sudo -H pip3 install -U pip3
    sudo -H pip3 install -U virtualenvwrapper

#. Start services

   .. code-block:: bash

    sudo systemctl start postgresql.service

#. Setup database

   .. code-block:: sql

    cat <<EOF | sudo -u postgres psql
    CREATE DATABASE agcs_db;
    CREATE USER django WITH PASSWORD 'db-secret';
    ALTER ROLE django SET client_encoding TO 'utf8';
    ALTER ROLE django SET default_transaction_isolation TO 'read committed';
    ALTER ROLE django SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE agcs_db TO django;
    ALTER USER django CREATEDB;
    EOF

#. Set environment variables

   .. code-block:: bash

    cat <<EOF>> ~/.bashrc && . ~/.bashrc
    set -a
    VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
    DJANGOPROJECT_DATA_DIR=~/data
    set +a
    . /usr/local/bin/virtualenvwrapper.sh
    EOF

#. Create a Python 3.x virtualenv

   .. code-block:: bash

    mkvirtualenv -p python3 agcs

#. Clone this repository

   .. code-block:: bash

    mkdir ~/site && cd ~/site
    git clone https://github.com/alphageek-xyz/site.git
    cd site && setvirtualenvproject

#. Create a data directory and 'secrets.json'

   .. code-block:: bash

    mkdir -p ~/data/conf ~/data/log/django
    echo '
    { "secret_key": "xyz",
      "db_host": "localhost",
      "db_password": "db-secret",
      "gapi_key": "gapi-secret",
      "recaptcha_pri": "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe",
      "recaptcha_pub": "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI",
      "email_host_user": "foo@example.com",
      "email_host_pass": "email-secret" }
    ' > ~/data/conf/secrets.json

#. Install dependencies and run tests

   .. code-block::

    make install && make test

#. Run the development server

   .. code-block:: bash

    ./manage.py runserver

   - To fix 404 errors for favicons, generate them

     .. code-block:: bash

        ./manage.py generate_favicon --prefix 'assets/img/favicon/' agcs/static/img/agcs.png &&
        cp -r ~/data/static_root/assets/img/favicon agcs/static/img

- Note: If you are modeling your own site after this one:
    + Adjust all brand-related variables and settings
    + Use your own logo
    + Use your own fixtures

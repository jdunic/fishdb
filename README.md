fishdb
======

## setup
	pip install virtualenv virtualenvwrapper

	source /usr/local/bin/virtualenvwrapper.sh

	mkvirtualenv fishdb_env

	workon fishdb_env

	pip install -r requirements.txt

	./manage.py syncdb

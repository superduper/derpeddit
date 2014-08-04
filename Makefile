export DJANGO_SETTINGS_MODULE=project.settings
export PYTHONPATH=$PYTHONPATH:.

spec:
	find . -name "*.pyc" -exec rm -f {} \;
	@konira --debug -x -t

lint: 
	pep8 . && pylint

clean-db:
	rm test.sqlite
	python manage.py syncdb --noinput

run:
	python manage.py runserver

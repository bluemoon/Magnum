SHELL := /bin/bash

init:
	python setup.py develop
	pip install -r requirements.pip --use-mirrors
test:
	nosetests ./tests/*
ci: init
	nosetests tests/test_magnum.py --with-xunit --xunit-file=junit-report.xml
simpleci:
	nosetests tests/test_magnum.py --with-xunit --xunit-file=junit-report.xml
site:
	cd docs; make dirhtml
docs: site

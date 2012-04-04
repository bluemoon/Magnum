SHELL := /bin/bash

init:
	python setup.py develop
	pip install -r requirements.txt
test:
	nosetests ./tests/*

simple:
	nosetests tests/test_requests.py

ci: init
	nosetests tests/test_requests.py --with-xunit --xunit-file=junit-report.xml

simpleci:
	nosetests tests/test_requests.py --with-xunit --xunit-file=junit-report.xml
site:
	cd docs; make dirhtml
docs: site

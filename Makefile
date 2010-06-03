
install:
	python setup.py install
test:
	nosetests --with-coverage --cover-package=py

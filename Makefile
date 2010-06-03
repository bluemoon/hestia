PYTHON=python2.6

.PHONY: all install clean

all:
	$(PYTHON) setup.py build
	nosetests -s

install:
	$(PYTHON) setup.py install --skip-build

test:
	nosetests --with-coverage --cover-package=py -v

clean:
	$(PYTHON) setup.py clean
	rm -rf build

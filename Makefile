PYTHON=python2.6

.PHONY: all install clean

all:
	$(PYTHON) setup.py build -f
	nosetests -sv py

install:
	$(PYTHON) setup.py install 

test:
	nosetests --with-coverage --cover-package=py -v

clean:
	$(PYTHON) setup.py clean
	rm -rf build

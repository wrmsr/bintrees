# Author:  mozman
# License: MIT-License

FLAGS = --inplace --force
CMD = setup.py build_ext
RUNTESTS = -m unittest discover

PYTHON27 = py -2.7
PYTHON32 = py -3.2
PYTHON33 = py -3.3
PYPY = C:/pypy-2.0-beta1/pypy.exe

build27:
	$(PYTHON27)  $(CMD) $(FLAGS)

build32:
	$(PYTHON32) $(CMD) $(FLAGS)

build33:
	$(PYTHON33) $(CMD) $(FLAGS)

test27:
	$(PYTHON27) $(RUNTESTS)

test32:
	$(PYTHON32) $(RUNTESTS)

test33:
	$(PYTHON33) $(RUNTESTS)
	
testpypy:
	$(PYPY) $(RUNTESTS)

testall: build27 test27 build32 test32 build33 test33 testpypy

packages:
	$(PYTHON27) setup.py sdist --formats=zip,gztar
	$(PYTHON27) setup.py bdist --formats=msi,wininst
	$(PYTHON32) setup.py bdist --formats=msi,wininst
	$(PYTHON33) setup.py bdist --formats=msi,wininst

release:
	$(PYTHON27) setup.py sdist --formats=zip,gztar upload
	$(PYTHON27) setup.py bdist --formats=msi,wininst upload
	$(PYTHON32) setup.py bdist --formats=msi,wininst upload
	$(PYTHON33) setup.py bdist --formats=msi,wininst upload

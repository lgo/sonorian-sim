
default: devrun

devrun: venv
	./run.sh sonorian/main.py

devbuild: venv
	venv/bin/python setup.py install

test: devbuild
	venv/bin/python test/runtests.py

venv: venv/bin/activate
venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate

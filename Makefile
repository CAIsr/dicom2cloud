
default:
	# No default rule

build-client-docker:
	# This is only for local testing, docker auto-builds on commit
	docker build container -t clinic2cloud:dev

build-pip:
	# Building source distribution for pip
	python setup.py sdist

upload-pip:
	# Upload to pypi, requires login
	twine upload dist/*


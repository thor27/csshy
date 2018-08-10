setup:
	@pip install -Ue .[tests]

publish:
	@python setup.py sdist upload

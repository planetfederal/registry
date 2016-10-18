install:
	pip install -r requirements.txt
	pip install -r testing.txt

smoke:
	pycsw-admin.py -c get_sysprof

flake:
	flake8 registry.py

test:
	coverage run --source=registry test_registry.py

.PHONY: install smoke flake test

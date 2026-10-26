.PHONY: validate test snapshots

validate: test snapshots

test:
	python3 -m unittest discover -s tests

snapshots:
	python3 -m promptsnap check

all: isort yapf flake8 mypy test

isort:
	isort -y -rc ./app

yapf:
	yapf -i -r app

flake8:
	flake8 app

mypy:
	mypy app

test:
	PIPELINE_DATABASE_URL=mysql://root:password@dbserver/pipeline pytest

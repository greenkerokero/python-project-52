install:
	uv sync

lint:
	uv run ruff check

format:
	uv run ruff format --diff

format-import:
	uv run ruff check --select I

format-apply:
	uv run ruff format && uv run ruff check --select I --fix

start:
	uv run manage.py runserver 0.0.0.0:8000

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

makemigrations:
	uv run python manage.py makemigrations

migrate:
	uv run manage.py migrate

collectstatic:
	uv run manage.py collectstatic --no-input

translate:
	uv run manage.py makemessages -l ru && uv run manage.py compilemessages

tests:
	uv run manage.py test

tests-coverage:
	uv run coverage run manage.py test

tests-report:
	uv run coverage report -m --skip-covered

demo-data:
	uv run manage.py add_demo_data

clear-db:
	uv run manage.py clear_db
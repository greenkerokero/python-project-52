install:
	uv sync

lint:
	uv run ruff check

format:
	uv run ruff format --diff

format-apply:
	uv run ruff format

start:
	uv run manage.py runserver 0.0.0.0:8000

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

migrate:
	uv run manage.py migrate

collectstatic:
	uv run manage.py collectstatic --no-input

translate:
	uv run manage.py makemessages -l ru && uv run manage.py compilemessages

install:
	uv sync

start:
	uv run manage.py runserver 0.0.0.0:8000

build:
    ./build.sh

render-start:
    gunicorn task_manager.wsgi

migrate:
	uv run manage.py migrate

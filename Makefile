install:
	uv sync

start:
	uv run manage.py runserver 0.0.0.0:8000

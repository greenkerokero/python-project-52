## Task Manager

[![Actions Status](https://github.com/greenkerokero/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/greenkerokero/python-project-52/actions)
[![Python CI](https://github.com/greenkerokero/python-project-52/actions/workflows/python-ci.yml/badge.svg)](https://github.com/greenkerokero/python-project-52/actions/workflows/python-ci.yml)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=greenkerokero_python-project-52&metric=coverage)](https://sonarcloud.io/summary/new_code?id=greenkerokero_python-project-52)

A task management web application built with Python and Django framework. It allows users to set tasks, assign
performers, manage task statuses, and group tasks by labels. Authentication and authorization mechanisms are integrated.

## Demonstration

You can view the application at the [provided link](https://python-project-52-g6kq.onrender.com/).

## Technologies used

- Python
- Django
- HTML/CSS
- Bootstrap 5
- PostgreSQL
- Rollbar (Error Tracking)

## Installation

For installation [UV package manager](https://docs.astral.sh/uv/getting-started/installation/) is required. After
installing UV, clone the repository:

```bash
git clone https://github.com/greenkerokero/python-project-52.git
```

Go to the project folder:

```bash
cd python-project-52
```

Install dependencies using UV:

```bash
make install
```

In the root of the project, create a _.env_ file with your key values and database access:

```bash
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgresql://[db_user]:[db_password]@localhost:5432/[db_name]
```

Initialize the database schema by running migrations:

```bash
make migrate
```

(Optional) You can populate the database with fake users, tasks, statuses, and labels for testing purposes:

```bash
make demo-data
```

## Usage

Start the app using Gunicorn. The server is available at[0.0.0.0:8000](http://0.0.0.0:8000/).

```bash
make render-start
```

Start in debug mode. The development server is available at[127.0.0.1:8000](http://127.0.0.1:8000/).

```bash
make dev
```

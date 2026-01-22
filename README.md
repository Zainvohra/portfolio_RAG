# AI Developer Bootcamp

A starter project using Python, FastAPI and uv.

## Description

A project starter for personal usage containing the following:

- [Python 3.13.\*](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/) web framework
- Structured logging using [`structlog`](https://www.structlog.org/)
- Dependency management using [`uv`](https://docs.astral.sh/uv/)
- Testing with [`pytest`](https://docs.pytest.org/) and optionally with coverage
  with [`pytest-cov`](https://pytest-cov.readthedocs.io/)
- Linting/formatting using [`ruff`](https://beta.ruff.rs/docs/)
- [`.gitignore`](https://github.com/github/gitignore/blob/main/Python.gitignore)

## Prerequisites

- [Python 3.13.\*](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/)

### 1. Install Python 3 and uv

**MacOS (using `brew`)**

```bash
brew install python@3.13 uv
```

**Ubuntu/Debian**

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.13
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Create a virtual environment with all necessary dependencies

From the root of the project execute:

```bash
uv sync
```

Activate the virtual environment with this command:

```bash
source .venv/bin/activate
```

## Run application

### Development mode

```bash
uv run fastapi dev
```

### Production mode

```bash
uv run fastapi run
```

## Testing

```bash
uv run pytest
```

### With coverage

```bash
uv run pytest --cov=app
```

### With coverage and HTML output

```bash
uv run pytest --cov-report html --cov=app
```

## Linting

```bash
uv run ruff check app/* tests/*
```

## Formatting

```bash
uv run ruff format app/* tests/*
```

## Setting up database and Mailhog

```
docker-compose up -d
```

This will create a database on port 5434 and mailhog.
(You can customize the port numbers in the docker-compose.yaml)

### Setting up alembic

Create a file `alembic.ini` and paste the contents of `alembic.ini.example` in it.

Find `sqlalchemy.url` and replace the values in curly brackets with actual values.

```
postgresql+psycopg2://{{username}}:{{password}}@localhost:{{db_port}}/{{db_name}}
```

### Creating Migrations

```
alembic revision --autogenerate -m "initial migration"
```

### Running Migrations

```
alembic upgrade head
```

### Environment Variables

Add the following env variables to your .env

```
OPENAI_API_KEY=OPENAI_API_KEY
DB_HOST_BOOTCAMP=<DB_HOST>
DB_PORT_BOOTCAMP=<DB_PORT>
DB_NAME_BOOTCAMP=<DB_NAME>
DB_USER_BOOTCAMP=<DB_USER>
DB_PASSWORD_BOOTCAMP=<DB_PASSWORD>
SMTP_HOST=<MAILHOG_HOST>
SMTP_PORT=<MAILHOG_PORT>
```

(Values for these variables can be found in docker-compose)

### Creating dummy data

From the tests directory in this project, run the following command:

```
python tests/test_generate_mock_attendance.py
```

## Portfolio RAG Setup

The system includes a RAG (Retrieval Augmented Generation) feature for portfolio data that allows users to ask questions about projects, experience, and skills.

### Setting up Portfolio Data

1. **Create your portfolio PDF**: Create a PDF file containing your portfolio information (projects, experience, skills, etc.) and place it in `rag/docs/portfolio_data.pdf`

2. **Generate embeddings**: Run the portfolio embedding creator script:

```bash
python rag/portfolio_embedding_creator.py --file rag/docs/portfolio_data.pdf
```

Or use the default path:

```bash
python rag/portfolio_embedding_creator.py
```

This will create a FAISS vector store at `rag/vectorstore/portfolio_data.faiss`.

3. **Start the backend**: The portfolio RAG tool is automatically available when you start the FastAPI server:

```bash
uv run fastapi dev
```

4. **Test the API**: You can test the portfolio chat endpoint:

```bash
curl -X POST http://localhost:8000/pulse/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What projects have you worked on?"}'
```

For more detailed instructions, see [rag/docs/PORTFOLIO_SETUP.md](rag/docs/PORTFOLIO_SETUP.md).
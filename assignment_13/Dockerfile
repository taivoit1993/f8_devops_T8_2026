FROM python:3.14-slim

WORKDIR /app

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.0.0 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="/opt/poetry/bin:$PATH"

# Install system dependencies, PostgreSQL client libs, build tools and CA certificates for AWS RDS SSL
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy dependency definition files first for Docker caching
COPY backend/pyproject.toml backend/poetry.lock* /app/

# Update lockfile if dependencies changed and install Python packages globally inside the container
RUN (poetry lock --no-update || poetry lock) && poetry install --no-root --no-interaction --no-ansi

# Copy the backend application source code into the image (for production / AWS deployment)
COPY backend/ /app/

# Expose API port
EXPOSE 8000

# Default command for production container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
FROM python:3.14.7-slim-bookworm

WORKDIR /app

RUN pip install poetry

RUN echo "print('hello world')" > "/app/main.py"

CMD ["python", "/app/main.py"]


# syntax=docker/dockerfile:1
FROM python:3.9.12-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE %{PORT:-5000}
COPY . .
CMD ["python3", "-m", "flask", "run"]

# syntax=docker/dockerfile:1
FROM python:3.11.0a7-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --no-cache-dir
EXPOSE 5000
COPY . .
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
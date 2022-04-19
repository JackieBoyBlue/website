# syntax=docker/dockerfile:1
FROM python:3.9.12-slim-buster
WORKDIR /app
ENV PORT=$PORT
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE $PORT
CMD ["python3", "app.py"]
# CMD ["python3", "-m", "flask", "run", "-p", "$PORT"]

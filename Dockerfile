FROM python:3.9

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

RUN apt-get update && apt-get install -y netcat-openbsd

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# syntax=docker/dockerfile:1

FROM python:3.11

WORKDIR /.

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 3101

CMD ["gunicorn", "app:app"]
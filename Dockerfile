FROM tiangolo/uvicorn-gunicorn-fastapi:latest

COPY ./requirements.txt /app/requirements.txt
COPY ./alembic /app/alembic
COPY ./alembic.ini /app/alembic.ini
COPY ./prestart.sh /app/prestart.sh
COPY ./app /app/app
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

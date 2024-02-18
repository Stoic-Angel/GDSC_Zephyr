FROM python:3.10-bullseye

WORKDIR  /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "-c", "gunicorn_conf.py", "-k", "uvicorn.workers.UvicornWorker", "app:app"]
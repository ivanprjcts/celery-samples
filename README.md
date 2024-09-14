# Celery samples

## Django celery app

* Install dependencies (tested on python `3.10`):
```shell
pip install -r requirements.txt
```

* To run the `celery-django-sample` app use docker:
```shell
docker compose up django-celery-worker
```

* Then, send tasks using `send_task.py` script from your local machine:
````shell
python send_task.py
````

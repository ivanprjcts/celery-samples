from celery import Celery

print("sending message")
app = Celery(
    'sample',
    broker="sqs://key:secret@localhost:4566",
)
app.send_task(
    name='celery_django_sample.tasks.long_task',
    queue='celery'
)

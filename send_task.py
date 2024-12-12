from celery import Celery

print("sending chain message")
app = Celery(
    'sample',
    broker="amqp://guest:guest@localhost:5672",
)
first_step = app.signature(
    'celery_django_sample.tasks.task',
    options={
        'queue': 'celery'
    }
)
next_step = app.signature(
    'other.tasks.task',
    options={
        'queue': 'next'
    }
)
chain = (first_step|next_step)
chain.apply_async()

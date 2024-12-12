# Celery samples

## Django celery app (for raising error)

Our celery application starts consuming unexpected queue after `RecoverableConnectionError`.

### How to reproduce it?

We have created a sample celery app with the following features:
* It uses rabbitMQ as broker.
* It has the heartbeat mechanism enabled, and we force it to fail adding a `time.sleep` in `heartbeat_sent` signal.
* The worker is run using `--pool=threads` mode.
* We send a "chain" task to the default queue. Note that the enchained `task other.tasks.task` task is sent to a new queue.

Then, we need to run the following steps:
* Install dependencies (tested on python `3.11`):
```shell
pip install -r requirements.txt
```
* To run the `celery-django-sample` app use docker:
```shell
docker compose up django-celery-worker
```
* Finally, send tasks using `send_task.py` script from your local machine:
````shell
python send_task.py
````

The stacktrace we are observing looks like this:

```
django-celery-worker-1  | [2024-12-12 13:24:27,073: INFO/MainProcess] celery@e090cc8e0181 ready.
django-celery-worker-1  | [2024-12-12 13:24:27,075: INFO/MainProcess] Task celery_django_sample.tasks.long_task[a14306d5-ba04-42fa-acfe-9509ed9b4ac3] received
django-celery-worker-1  | [2024-12-12 13:24:27,079: INFO/MainProcess] celery_django_sample.tasks.long_task[a14306d5-ba04-42fa-acfe-9509ed9b4ac3]: Running long task ...
django-celery-worker-1  | [2024-12-12 13:24:28,014: INFO/MainProcess] sleeping...
django-celery-worker-1  | [2024-12-12 13:24:37,116: INFO/MainProcess] Task celery_django_sample.tasks.long_task[a14306d5-ba04-42fa-acfe-9509ed9b4ac3] succeeded in 10.037396678999812s: 'Task completed!'
django-celery-worker-1  | [2024-12-12 13:24:40,020: INFO/MainProcess] sleeping...
rabbitmq-1              | 2024-12-12 13:24:47.983429+00:00 [error] <0.837.0> closing AMQP connection <0.837.0> (172.18.0.3:60818 -> 172.18.0.2:5672):
rabbitmq-1              | 2024-12-12 13:24:47.983429+00:00 [error] <0.837.0> missed heartbeats from client, timeout: 8s
django-celery-worker-1  | [2024-12-12 13:24:50,001: WARNING/MainProcess] consumer: Connection to broker lost. Trying to re-establish the connection...
django-celery-worker-1  | Traceback (most recent call last):
django-celery-worker-1  |   File "/usr/local/lib/python3.11/site-packages/celery/worker/consumer/consumer.py", line 340, in start
django-celery-worker-1  |     blueprint.start(self)
django-celery-worker-1  |   File "/usr/local/lib/python3.11/site-packages/celery/bootsteps.py", line 116, in start
django-celery-worker-1  |     step.start(parent)
django-celery-worker-1  |   File "/usr/local/lib/python3.11/site-packages/celery/worker/consumer/consumer.py", line 746, in start
django-celery-worker-1  |     c.loop(*c.loop_args())
django-celery-worker-1  |   File "/usr/local/lib/python3.11/site-packages/celery/worker/loops.py", line 97, in asynloop
django-celery-worker-1  |     next(loop)
django-celery-worker-1  |   File "/usr/local/lib/python3.11/site-packages/kombu/asynchronous/hub.py", line 373, in create_loop
django-celery-worker-1  |     cb(*cbargs)
django-celery-worker-1  |   File "/usr/local/lib/python3.11/site-packages/kombu/transport/base.py", line 248, in on_readable
django-celery-worker-1  |     reader(loop)
django-celery-worker-1  |   File "/usr/local/lib/python3.11/site-packages/kombu/transport/base.py", line 228, in _read
django-celery-worker-1  |     raise RecoverableConnectionError('Socket was disconnected')
django-celery-worker-1  | amqp.exceptions.RecoverableConnectionError: Socket was disconnected
django-celery-worker-1  | [2024-12-12 13:24:50,003: WARNING/MainProcess] /usr/local/lib/python3.11/site-packages/celery/worker/consumer/consumer.py:391: CPendingDeprecationWarning: 
django-celery-worker-1  | In Celery 5.1 we introduced an optional breaking change which
django-celery-worker-1  | on connection loss cancels all currently executed tasks with late acknowledgement enabled.
django-celery-worker-1  | These tasks cannot be acknowledged as the connection is gone, and the tasks are automatically redelivered
django-celery-worker-1  | back to the queue. You can enable this behavior using the worker_cancel_long_running_tasks_on_connection_loss
django-celery-worker-1  | setting. In Celery 5.1 it is set to False by default. The setting will be set to True by default in Celery 6.0.
django-celery-worker-1  | 
django-celery-worker-1  |   warnings.warn(CANCEL_TASKS_BY_DEFAULT, CPendingDeprecationWarning)
django-celery-worker-1  | 
django-celery-worker-1  | [2024-12-12 13:24:50,004: INFO/MainProcess] sleeping...
django-celery-worker-1  | [2024-12-12 13:25:00,011: WARNING/MainProcess] /usr/local/lib/python3.11/site-packages/celery/worker/consumer/consumer.py:508: CPendingDeprecationWarning: The broker_connection_retry configuration setting will no longer determine
django-celery-worker-1  | whether broker connection retries are made during startup in Celery 6.0 and above.
django-celery-worker-1  | If you wish to retain the existing behavior for retrying connections on startup,
django-celery-worker-1  | you should set broker_connection_retry_on_startup to True.
django-celery-worker-1  |   warnings.warn(
django-celery-worker-1  | 
rabbitmq-1              | 2024-12-12 13:25:00.016160+00:00 [info] <0.955.0> accepting AMQP connection <0.955.0> (172.18.0.3:50890 -> 172.18.0.2:5672)
django-celery-worker-1  | [2024-12-12 13:25:00,020: INFO/MainProcess] Connected to amqp://guest:**@rabbitmq:5672//
rabbitmq-1              | 2024-12-12 13:25:00.020373+00:00 [info] <0.955.0> connection <0.955.0> (172.18.0.3:50890 -> 172.18.0.2:5672): user 'guest' authenticated and granted access to vhost '/'
django-celery-worker-1  | [2024-12-12 13:25:00,024: WARNING/MainProcess] /usr/local/lib/python3.11/site-packages/celery/worker/consumer/consumer.py:508: CPendingDeprecationWarning: The broker_connection_retry configuration setting will no longer determine
django-celery-worker-1  | whether broker connection retries are made during startup in Celery 6.0 and above.
django-celery-worker-1  | If you wish to retain the existing behavior for retrying connections on startup,
rabbitmq-1              | 2024-12-12 13:25:00.025102+00:00 [info] <0.846.0> closing AMQP connection <0.846.0> (172.18.0.3:60828 -> 172.18.0.2:5672, vhost: '/', user: 'guest')
django-celery-worker-1  | you should set broker_connection_retry_on_startup to True.
rabbitmq-1              | 2024-12-12 13:25:00.028481+00:00 [info] <0.967.0> accepting AMQP connection <0.967.0> (172.18.0.3:50906 -> 172.18.0.2:5672)
django-celery-worker-1  |   warnings.warn(
django-celery-worker-1  | 
rabbitmq-1              | 2024-12-12 13:25:00.031988+00:00 [info] <0.967.0> connection <0.967.0> (172.18.0.3:50906 -> 172.18.0.2:5672): user 'guest' authenticated and granted access to vhost '/'
django-celery-worker-1  | [2024-12-12 13:25:00,033: INFO/MainProcess] sleeping...
django-celery-worker-1  | [2024-12-12 13:25:10,039: INFO/MainProcess] mingle: searching for neighbors
django-celery-worker-1  | [2024-12-12 13:25:11,059: INFO/MainProcess] mingle: all alone
django-celery-worker-1  | [2024-12-12 13:25:11,083: ERROR/MainProcess] Received unregistered task of type 'other.tasks.task'.
django-celery-worker-1  | The message has been ignored and discarded.
django-celery-worker-1  | 
django-celery-worker-1  | Did you remember to import the module containing this task?
django-celery-worker-1  | Or maybe you're using relative imports?
django-celery-worker-1  | 
django-celery-worker-1  | Please see
django-celery-worker-1  | https://docs.celeryq.dev/en/latest/internals/protocol.html
django-celery-worker-1  | for more information.
django-celery-worker-1  | 
django-celery-worker-1  | The full contents of the message body was:
django-celery-worker-1  | '[["Task completed!"], {}, {"callbacks": null, "errbacks": null, "chain": [], "chord": null}]' (92b)
django-celery-worker-1  | 
django-celery-worker-1  | The full contents of the message headers:
django-celery-worker-1  | {'argsrepr': "('Task completed!',)", 'eta': None, 'expires': None, 'group': None, 'group_index': None, 'id': 'e41091dc-3904-4afc-baf7-19ddea93c86f', 'ignore_result': False, 'kwargsrepr': '{}', 'lang': 'py', 'origin': 'gen1@e090cc8e0181', 'parent_id': 'a14306d5-ba04-42fa-acfe-9509ed9b4ac3', 'replaced_task_nesting': 0, 'retries': 0, 'root_id': 'a14306d5-ba04-42fa-acfe-9509ed9b4ac3', 'shadow': None, 'stamped_headers': None, 'stamps': {}, 'task': 'other.tasks.task', 'timelimit': [None, None]}
django-celery-worker-1  | 
django-celery-worker-1  | The delivery info for this task is:
django-celery-worker-1  | {'consumer_tag': 'None9', 'delivery_tag': 1, 'redelivered': False, 'exchange': '', 'routing_key': 'next'}
django-celery-worker-1  | Traceback (most recent call last):
django-celery-worker-1  |   File "/usr/local/lib/python3.11/site-packages/celery/worker/consumer/consumer.py", line 659, in on_task_received
django-celery-worker-1  |     strategy = strategies[type_]
django-celery-worker-1  |                ~~~~~~~~~~^^^^^^^
django-celery-worker-1  | KeyError: 'other.tasks.task'
```

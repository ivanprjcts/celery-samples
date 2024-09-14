from time import sleep

from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def add(x, y):
    return x + y


@shared_task
def long_task():
    logger.info("Running long task ...")
    sleep(10)  # Simulate a long-running task
    return 'Task completed!'

from __future__ import absolute_import
from celery import Celery
from footman.settings import CELERY_BROKER_URL

MAX_TASKS_OUTSTANDING = 10000

app = Celery('footman',
             broker=CELERY_BROKER_URL,
             backend=CELERY_BROKER_URL,
             include=['footman.footman'])

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=300,
    CELERY_ACKS_LATE=True,
)
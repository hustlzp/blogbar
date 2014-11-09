from __future__ import absolute_import
from celery import Celery

app = Celery('celery_proj',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/1',
             include=['celery_proj.tasks'])
app.config_from_object('celery_proj.config')

if __name__ == '__main__':
    app.start()

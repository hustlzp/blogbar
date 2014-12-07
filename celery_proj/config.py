from celery.schedules import crontab

CELERY_TIMEZONE = 'Asia/Shanghai'
CELERYBEAT_SCHEDULE = {
    'grab': {
        'task': 'celery_proj.tasks.grab',
        'schedule': crontab(hour='0, 6, 11, 18', minute=0)
    }
}

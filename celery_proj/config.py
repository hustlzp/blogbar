from celery.schedules import crontab

CELERY_TIMEZONE = 'Asia/Shanghai'
CELERYBEAT_SCHEDULE = {
    'grab': {
        'task': 'celery_proj.tasks.grab',
        'schedule': crontab(hour='0, 6, 12, 18', minute=30)
    },
    'analyse': {
        'task': 'celery_proj.tasks.analyse',
        'schedule': crontab(hour='1, 7, 13, 17', minute=30)
    }
}

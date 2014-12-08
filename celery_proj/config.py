from celery.schedules import crontab

CELERY_DISABLE_RATE_LIMITS = True
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERYBEAT_SCHEDULE = {
    'grab': {
        'task': 'celery_proj.tasks.grab',
        'schedule': crontab(hour='6, 12, 18, 23', minute=0)
    }
}

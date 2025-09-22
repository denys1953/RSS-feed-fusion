from celery import Celery
from app.core.config import settings

redis_url = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"

celery_app = Celery(
    "feed_fusion_worker",
    broker=redis_url,   
    backend=redis_url,
    include=["app.tasks.feed_tasks"] 
)


celery_app.conf.beat_schedule = {
    'fetch-all-feeds-every-30-minutes': {
        'task': 'app.tasks.feed_tasks.schedule_all_feeds_task',
        'schedule': 1800.0,  
    },
}


celery_app.conf.timezone = 'UTC'

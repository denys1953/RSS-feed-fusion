from sqlalchemy.future import select

from app.apis.feeds.models import Feed
from app.celery_worker import celery_app
from app.core.feed_parser import parse_rss_feed
from app.apis.articles import models as article_models
from app.db.session import SyncSessionLocal


@celery_app.task
def fetch_single_feed_task(feed_id: int):
    db = SyncSessionLocal()

    try:
        # Resolve feed_id by URL and limit duplicate check by this feed
        feed_query = select(Feed).where(Feed.id == feed_id)
        feed_result = db.execute(feed_query)
        feed = feed_result.scalar_one_or_none()

        parsed_articles = parse_rss_feed(feed.url)


        query = select(article_models.Article.url).where(article_models.Article.feed_id == feed_id)
        result = db.execute(query)
        existing_links = set(result.scalars().all())
        new_articles_to_add = []

        for article in parsed_articles:
            if str(article.url) not in existing_links:
                new_article = article_models.Article(
                    title = article.title,
                    url = str(article.url),
                    source = feed.title,
                    description = article.description,
                    publication_date = article.publication_date,
                    feed_id = feed_id
                )
                new_articles_to_add.append(new_article)

        if new_articles_to_add:
            db.add_all(new_articles_to_add)
            try:
                db.commit()
            except Exception:
                db.rollback()

    finally:
        db.close()
        

@celery_app.task
def schedule_all_feeds_task():
    db = SyncSessionLocal()

    try:
        query = select(Feed.id)
        result = db.execute(query)
        all_feed_ids = result.scalars().all()

        for feed_id in all_feed_ids:
            fetch_single_feed_task.delay(feed_id)

    finally:
        db.close()

    return f"Refreshing for {len(all_feed_ids)} feeds has started"
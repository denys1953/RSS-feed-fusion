from datetime import datetime, timezone
import time

import httpx
import feedparser
from app.apis.articles.schemas import ParsedArticle


def format_publication_date(time_struct: str):
    timestamp = time.mktime(time_struct)
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)


def parse_rss_feed(url: str) -> list[ParsedArticle]:
    articles = feedparser.parse(url)
    parsed_articles = []

    for article in articles["entries"]:
        art = {
            "title": article["title"],
            "description": article["summary"],
            "url": article["links"][0]["href"],
            "publication_date": format_publication_date(article["published_parsed"])
        }
        parsed_article = ParsedArticle.model_validate(art)
        parsed_articles.append(parsed_article)


    return parsed_articles
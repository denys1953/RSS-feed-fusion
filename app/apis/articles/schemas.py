from datetime import datetime
from pydantic import BaseModel, HttpUrl

class ParsedArticle(BaseModel):
    title: str
    url: HttpUrl
    source: str
    description: str
    publication_date: datetime



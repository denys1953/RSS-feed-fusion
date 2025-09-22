from sqlalchemy import Table, Column, Integer, ForeignKey
from .base import Base

subscription_table = Table(
    "subscription_users_to_feeds",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("feed_id", Integer, ForeignKey("feeds.id"), primary_key=True),
)
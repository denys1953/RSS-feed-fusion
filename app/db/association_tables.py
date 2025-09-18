from sqlalchemy import Table, Column, Integer, ForeignKey
from .base import Base

subscription_table = Table(
    "subscriptions",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("feed_id", Integer, ForeignKey("feeds.id"), primary_key=True),
)
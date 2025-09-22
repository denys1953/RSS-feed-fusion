from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass


import app.apis
import app.db.association_tables
from database import Base
from sqlalchemy import Column, Integer, VARCHAR, DATE
class Book(Base):
    __tablename__ = "Books"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(VARCHAR(255))
    author = Column(VARCHAR(255))
    publish_date = Column(DATE)

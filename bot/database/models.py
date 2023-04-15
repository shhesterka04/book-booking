from sqlalchemy import Base, Table, Column, Integer, String, DateTime, ForeignKey

from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Books(Base):
    __tablename__ = 'books'
    boock_id = Column(Integer, primary_key=True)
    title = Column(String())
    author = Column(String())
    published = Column(DateTime())
    date_added = Column(DateTime())
    date_deleted = Column(DateTime())

class Borrows(Base):
    __tablename__ = 'borrows'
    borrow_id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.boock_id'))
    date_start = Column(DateTime())
    date_end = Column(DateTime())
    user_id = Column(Integer)

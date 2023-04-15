from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship, Mapped
from datetime import date
from sqlalchemy.sql import func

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'

    book_id: Mapped[int] = Column(Integer, primary_key=True)
    title: Mapped[str] = Column(String)
    author: Mapped[str] = Column(String)
    published: Mapped[int] = Column(Integer)
    date_added: Mapped[date] = Column(Date, server_default=func.now())
    date_deleted: Mapped[date] = Column(Date)

    borrow: Mapped['Borrow'] = relationship('Borrow', back_populates='book')

class Borrow(Base):
    __tablename__ = 'borrows'

    borrow_id: Mapped[int] = Column(Integer, primary_key=True)
    book_id: Mapped[int] = Column(Integer, ForeignKey('books.book_id'))
    date_start: Mapped[date] = Column(Date, server_default=func.now())
    date_end: Mapped[date] = Column(Date)
    user_id: Mapped[int] = Column(Integer)

    book: Mapped['Book'] = relationship('Book', back_populates='borrow')


from sqlalchemy import create_engine

USER = 'Arzym'
PASSWORD = '201200374art'
PORT = '5432'
DBNAME = 'books'

engine = create_engine(f'postgresql://{USER}:{PASSWORD}@localhost:{PORT}/{DBNAME}')
Base.metadata.create_all(engine)
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Mapped
from datetime import datetime


Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'

    boock_id: Mapped[int] = Column(Integer, primary_key=True)
    title: Mapped[str] = Column(String())
    author: Mapped[str] = Column(String())
    published: Mapped[datetime] = Column(DateTime())
    date_added: Mapped[datetime] = Column(DateTime())
    date_deleted: Mapped[datetime] = Column(DateTime())

    borrow: Mapped['Borrow'] = relationship('Borrow', back_populates='book')

class Borrow(Base):
    __tablename__ = 'borrows'

    borrow_id: Mapped[int] = Column(Integer, primary_key=True)
    book_id: Mapped[int] = Column(Integer, ForeignKey('books.boock_id'))
    date_start: Mapped[datetime] = Column(DateTime())
    date_end: Mapped[datetime] = Column(DateTime())
    user_id: Mapped[datetime] = Column(Integer)

    book: Mapped['Book'] = relationship('Book', back_populates='borrow')


from sqlalchemy import create_engine

USER = 'Arzym'
PASSWORD = '201200374art'
PORT = '5432'
DBNAME = 'books'

engine = create_engine(f'postgresql://{USER}:{PASSWORD}@localhost:{PORT}/{DBNAME}')
Base.metadata.create_all(engine)
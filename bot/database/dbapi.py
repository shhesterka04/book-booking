from typing import Tuple, List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import *

class DatabaseConnector:

    def __init__(self):
        USER = 'Arzym'
        PASSWORD = '201200374art'
        PORT = '5432'
        DBNAME = 'books'

        self.engine = create_engine(f'postgresql://{USER}:{PASSWORD}@localhost:{PORT}/{DBNAME}')
        self.Session = sessionmaker(bind=engine)

    def add(self, title: str, author: str, published: int) -> tuple[bool, int]:
        session = self.Session()
        try:
            book = Book(title=title, author=author, published=published)
            session.add(book)
            session.commit()
        except:
            session.rollback() 
            return False
        else:
            return book.boock_id
        finally:
            session.close()

    def delete(self, book_id: int) -> bool:
        session = self.Session()
        session.close()

    def list_books(self) -> List[int]:
        session = self.Session()
        session.close()

    def get_book(self, title: str, author: str, published: int) -> tuple[bool, int]:
        session = self.Session()
        session.close()

    def borrow(self, book_id: int) -> tuple[bool, int]:
        session = self.Session()
        session.close()

    def get_borrow(self, title: str, author: str, published: int) -> int:
        session = self.Session()
        session.close()

    def retrieve(self) -> None:
        session = self.Session()
        session.close()
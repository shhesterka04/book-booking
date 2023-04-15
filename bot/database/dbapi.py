from typing import Tuple, List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import *

class DatabaseConnector:

    def __init__(self):
        self.engine = create_engine('sqlite:///books.db')
        self.Session = sessionmaker(bind=self.engine)

    def add(self, name: str, author: str, pub_year: int) -> tuple[bool, int]:
        session = self.Session()
        session.close() 

    def delete(self, book_id: int) -> bool:
        session = self.Session()
        session.close()

    def list_books(self) -> List[int]:
        session = self.Session()
        session.close()

    def get_book(self, name: str, author: str, pub_year: int) -> tuple[bool, int]:
        session = self.Session()
        session.close()

    def borrow(self, book_id: int) -> tuple[bool, int]:
        session = self.Session()
        session.close()

    def get_borrow(self, name: str, author: str, pub_year: int) -> int:
        session = self.Session()
        session.close()

    def retrieve(self) -> None:
        session = self.Session()
        session.close()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DatabaseConnector:

    def __init__(self):
        self.engine = create_engine('sqlite:///books.db')
        self.Session = sessionmaker(bind=self.engine)

    def add(self):
        session = self.Session()
        session.close() 

    def delete(self):
        session = self.Session()
        session.close()

    def list_books(self):
        session = self.Session()
        session.close()

    def get_book(self):
        session = self.Session()
        session.close()

    def borrow(self):
        session = self.Session()
        session.close()

    def get_borrow(self):
        session = self.Session()
        session.close()

    def retrieve(self):
        session = self.Session()
        session.close()
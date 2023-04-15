from typing import Tuple, List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

from .models import *

class DatabaseConnector:

    def __init__(self, user_id: int):
        USER = 'Arzym'
        PASSWORD = '201200374art'
        PORT = '5432'
        DBNAME = 'books'

        self.user_id = user_id
        self.engine = create_engine(f'postgresql://{USER}:{PASSWORD}@localhost:{PORT}/{DBNAME}')
        self.Session = sessionmaker(bind=engine)

    '''
        `add` - добавляет книгу в таблицу Books. 
        Возвращает book_id новой книги или False, если не получилось добавить
    '''
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
            if not book:
                return False
            else: 
                return book.book_id
        finally:
            session.close()


    '''
        `delete` - помечает книгу более непригодной к использованию 
        Возвращает true/false: успешно или неуспешно прошла операция. 
        Книгу нельзя удалить, если она у кого-то на руках.
    '''
    def delete(self, book_id: int) -> bool:
        session = self.Session()
        book = session.query(Book).filter(Book.book_id == book_id).first()
        is_deleted = False
        if book: # Book was found
            if len(book.borrow) == 0 and book.date_deleted == None: # Book is not borrowed and is not deleted
                book.date_deleted = date.today()
                session.commit()
                session.close()
                is_deleted = True
        session.close()
        return is_deleted


    '''
        `list_books` - возвращает список всех добавленных в БД книг
    '''
    def list_books(self) -> List[Book]:
        session = self.Session()
        books = list(session.query(Book).all())
        session.close()
        return books


    '''
        `get_book` - поиск книги по названию и автору. 
        Возвращает book_id или None, если такой книги нет. 
        Помните, что пользователь может вводить информацию в разных регистрах.
    '''
    def get_book(self, title: str, author: str) -> tuple[None, int]:
        session = self.Session()
        book = (session
            .query(Book)
            .where(and_(Book.title == title, Book.author == author))
            .first())
        session.close()
        if book:
            return book.book_id
        else:
            return None


    '''
        `borrow` - добавляет новую запись в таблицу Borrows со временем начала аренды книги. 
        Если книга уже в аренде, то ее не должно быть можно арендовать. 
        Если у человека уже есть книга в аренде, вторую он взять не может. 
        Возвращает borrow_id или False, если не получилось арендовать книгу.
    '''
    def borrow(self, book_id: int) -> tuple[bool, int]:
        session = self.Session()
        # Try to find book  
        book = (session
                .query(Book)
                .filter(Book.book_id == book_id)
                .first())
        # Look up for user borrows
        user_borrow = (session
            .query(Borrow)
            .filter(and_(Borrow.user_id == self.user_id, Borrow.date_end == None))
            .first())
        book_borrow = (session
            .query(Borrow)
            .filter(and_(Borrow.book_id == book_id, Borrow.date_end == None))
            .first())
        created_borrow = False
        book_id = None
        print(book)
        print(book_borrow)
        print(user_borrow)
        if book and not user_borrow and not book_borrow:
                book.borrow.append(Borrow(
                    book_id=book.book_id,
                    user_id=self.user_id
                ))
                session.commit()
                book_id = book.book_id
                created_borrow = True
        session.close()
        if created_borrow:
            return book_id
        else:
            return False
        

    def get_borrow(self) -> tuple[bool, int]:
        session = self.Session()
        borrow = (session
            .query(Borrow)
            .filter(and_(Borrow.user_id == self.user_id, Borrow.date_end == None))
            .first())
        session.close()
        if borrow:
            return borrow.book_id
        else:
            return None
        

    def retrieve(self) -> None:
        session = self.Session()
        borrow = (session
            .query(Borrow)
            .filter(and_(Borrow.user_id == self.user_id, Borrow.date_end == None))
            .first())
        if borrow:
            borrow.date_end = date.today()
            session.commit()
        session.close()
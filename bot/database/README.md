# 1. Структура базы данных и моделей ORM

### `(файл database/dbapi.py)`

Для того, чтобы реализовать весь заявленный функционал, нам понадобятся 2 таблицы в Postgres: справочник всех добавленных книг и таблица, содержащая информацию о датах использования книг.

## Спецификация БД

### Таблица Books

- `book_id` - идентификатор записи в таблице
- `title` - название книги
- `author` - автор книги
- `published` - год издания книги
- `date_added` - дата, когда книга была зарегистрирована в нашей библиотеке
- `date_deleted` - дата, когда было зарегистрировано, что эту книгу больше нельзя использовать (nullable)

### Таблица Borrows

- `borrow_id` - идентификатор записи в таблице
- `book_id` - foreign key на идентификатор книги в таблице Books
- `date_start` - дата и время начала аренды книги
- `date_end` - дата и время конца аренды книги (nullable)
- `user_id` - идентификатор чата пользователя, который взял книгу

Классы моделей данных назовите соответственно `Book` и `Borrow`.


----------------------------------------------------------------


# 2. Структура кода

## 2.1. `database/dbapi.py`

В этом файле опишем класс DatabaseConnector. Он должен содержать методы, которые позволят проводить операции с книгами:

- `add` - добавляет книгу в таблицу Books. Возвращает book_id новой книги или False, если не получилось добавить.
- `delete` - помечает книгу более непригодной к использованию возвращает true/false: успешно или неуспешно прошла операция. Книгу нельзя удалить, если она у кого-то на руках.
- `list_books` - возвращает список всех добавленных в БД книг
- `get_book` - поиск книги по названию и автору. Возвращает book_id или None, если такой книги нет. Помните, что пользователь может вводить информацию в разных регистрах.
- `borrow` - добавляет новую запись в таблицу Borrows со временем начала аренды книги. Если книга уже в аренде, то ее не должно быть можно арендовать. Если у человека уже есть книга в аренде, вторую он взять не может. Возвращает borrow_id или False, если не получилось арендовать книгу.
- `get_borrow` - возвращает borrow_id брони, однозначно связанной с пользователем
- `retrieve` - изменяет запись в таблице Borrows, добавляя к ней дату возврата книги

В атрибутах класса должны содержаться параметры подключения к БД. Соединение с БД должно устанавливаться отдельно для каждой операции.
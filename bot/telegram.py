import telebot
import database as db

token = "5958465756:AAE8FNZ2_sNZ5tJHKhs-QnV6afQHA6kBptM" 
#db_connector = DatabaseConnector()
#интересно а в VS можно делать переменные среды?
bot = telebot.TeleBot(token)
temp_books = {}

class Book():
    def __init__(self, title:str=None, author:str=None, year:int=None, command=None):
        self.title = title
        self.author = author
        self.year = year
        self.command = command

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """\
Привет! Это бот для обмена книгами. Он умеет следующее:
- добавлять книги в общую библиотеку
- брать книги из библиотеки для чтения
- возвращать книги в библиотеку после чтения
- удалять книги из библиотеки (например, из-за износа)
- формировать файл со статистикой использования книги и отправление ссылки на скачивание этого файла
\
""")

@bot.message_handler(commands=['add', 'delete', 'find', 'borrow', 'stats'])
def add_book(message):
    chat_id = message.chat.id
    cmd = message.text
    temp_books[chat_id] = Book(command=cmd)
    msg = bot.send_message(chat_id, "Введите название книги:")
    bot.register_next_step_handler(msg, book_title)

def book_title(message):
    chat_id = message.chat.id
    title = message.text
    temp_books[chat_id].title = title
    msg = bot.send_message(chat_id, "Введите автора книги:")
    bot.register_next_step_handler(msg, book_author)

def book_author(message):
    chat_id = message.chat.id
    author = message.text
    temp_books[chat_id].author = author
    msg = bot.send_message(chat_id, "Введите год издания:")
    bot.register_next_step_handler(msg, book_year)

def book_year(message):
    chat_id = message.chat.id
    try:
        year = int(message.text)
    except ValueError:
        bot.send_message(chat_id, "Невалидный год публикации. Введите целое число")
        return
    temp_books[chat_id].year = year
    book = temp_books[chat_id]

    if book.command == '/add':
        bot.message_handler(f"Книга {book.title}, {book.author} {book.year} года добавлена!") #debug
        # book_id = db_connector.add(book.title, book.author, book.year)
        # if book_id:
        #     bot.send_message(chat_id, f"Книга добавлена (id: {book_id})")
        # else:
        #     bot.send_message(chat_id, "Ошибка создания записи")
    elif book.command == '/delete':
        pass

    elif book.command == '/borrow':
        pass

    elif book.command == '/find':
        pass

    elif book.command == '/stats':
        pass

@bot.message_handler(commands=['list'])
def show_list(message):
    pass


@bot.message_handler(commands=['retrieve'])
def retrieve_book(message):
    pass


bot.infinity_polling()






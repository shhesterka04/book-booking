import telebot
import database as db

token = "5958465756:AAE8FNZ2_sNZ5tJHKhs-QnV6afQHA6kBptM" 
db_connector = DatabaseConnector()
#интересно а в VS можно делать переменные среды?
bot = telebot.TeleBot(token)
temp_books = {}

class Book():
    def __init__(self, title:str=None, author:str=None, year:int=None):
        self.title = title
        self.author = author
        self.year = year

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

@bot.message_handler(commands=['add'])
def add_book(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Введите название книги:")
    temp_books[chat_id] = Book()
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
    except:
        bot.send_message(chat_id, "Невалидный год публикации. Введите целое число")
        return
        #мб цикл сюда?
    temp_books[chat_id].year = year
    current_book = temp_books[chat_id]
    book_id = db_connector.add(current_book.title, current_book.author, current_book.year)
    if book_id:
        bot.send_message(chat_id, f"Книга добавлена (id: {book_id})")
    else:
        bot.send_message(chat_id, "Ошибка создания записи")


@bot.message_handler(commands=['delete'])
def delete_book(message):
    pass

@bot.message_handler(commands=['list'])
def show_list(message):
    pass

@bot.message_handler(commands=['find'])
def find_book(message):
    pass

@bot.message_handler(commands=['borrow'])
def borrow_book(message):
    pass

@bot.message_handler(commands=['retrieve'])
def retrieve_book(message):
    pass

@bot.message_handler(commands=['stats'])
def get_stats(message):
    pass



bot.infinity_polling()


class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year



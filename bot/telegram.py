import telebot
import database as db
import app

token = "5958465756:AAE8FNZ2_sNZ5tJHKhs-QnV6afQHA6kBptM" 
db_connector = db.DatabaseConnector()
bot = telebot.TeleBot(token)
temp_books = {}

class Book():
    def __init__(self, title:str=None, author:str=None, published:int=None, command=None):
        self.title = title
        self.author = author
        self.published = published
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
    bot.register_next_step_handler(msg, book_published)

def book_published(message):
    chat_id = message.chat.id
    try:
        published = int(message.text)
    except ValueError:
        bot.send_message(chat_id, "Невалидный год публикации. Введите целое число")
        return
    temp_books[chat_id].published = published
    book = temp_books[chat_id]

    if book.command == '/add':
        bot.message_handler(f"Книга {book.title}, {book.author} {book.published} года добавлена!") #debug
        book_id = db_connector.add(book.title, book.author, book.published)
        if book_id:
            bot.send_message(chat_id, f"Книга добавлена (id: {book_id})")
        else:
            bot.send_message(chat_id, "Ошибка создания записи")
    elif book.command == '/delete':
        book_id = db_connector.get_book(book.title, book.author, book.published)
        if book_id:
            msg = bot.send_message(chat_id, f"Найдена книга: {book.title} {book.author} {book.published}. Удаляем?")
            bot.register_next_step_handler(msg, delete_book)
        else:
            bot.send_message("Невозможно удалить книгу")

    elif book.command == '/borrow':
        book_id = db_connector.get_book(book.title, book.author, book.published)
        if book_id:
            msg = bot.send_message(chat_id, f"Найдена книга: {book.title} {book.author} {book.published}. Берем?")
            bot.register_next_step_handler(msg, borrow_book)
        else:
            bot.send_message("Книгу сейчас невозможно взять")


    elif book.command == '/find':
        book_id = db_connector.get_book(book.title, book.author, book.published)
        if book_id:
            bot.send_message(chat_id, f"Найдена книга: {book.title} {book.author} {book.published}")
        else:
            bot.send_message(chat_id, "Такой книги у нас нет")

    elif book.command == '/stats':
        book_id = db_connector.get_book(book.title, book.author, book.published)
        if book_id:
            app.download_book_stats(book_id)
            bot.send_message(chat_id, f"Статистика доступна по адресу http://localhost/download/{book_id}")
        else:
            bot.send_message(chat_id, "Нет такой книги")

def delete_book(message):
    chat_id = message.chat.id
    book = temp_books[chat_id]
    if message.text == "Да":
        status = db_connector.delete(book.title, book.author, book.published)
        if status:
            bot.send_message(chat_id, "Книга удалена")
        else:
            bot.send_message(chat_id, "Невозможно удалить книгу")
    elif message.text == "Нет":
        bot.send_message(chat_id, "Удаление книги отменено")

def borrow_book(message):
    chat_id = message.chat.id
    book = temp_books[chat_id]
    if message.text == "Да":
        status = db_connector.borrow(book.title, book.author, book.published)
        if status:
            bot.send_message(chat_id, "Вы взяли книгу")
        else:
            bot.send_message(chat_id, "Книгу сейчас невозможно взять")
    elif message.text == "Нет":
        bot.send_message(chat_id, "Аренда книги отменена")

@bot.message_handler(commands=['list'])
def show_list(message):
    chat_id = message.chat.id
    books_list = db_connector.list_books()
    ans = ""
    for book in books_list:
        line = ""
        ans.append(line)
    bot.send_message(chat_id, ans)
    #дописать логику после того, как узнаю принцип работы АПИ

@bot.message_handler(commands=['retrieve'])
def retrieve_book(message):
    book_id = db_connector.get_borrow()
    book = temp_books[book_id]
    db_connector.retrieve()
    bot.send_message(f"Вы вернули книгу {book.title} {book.author} {book.published}")





bot.infinity_polling()






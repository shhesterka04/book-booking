import telebot

token = "5958465756:AAE8FNZ2_sNZ5tJHKhs-QnV6afQHA6kBptM" 
#интересно а в VS можно делать переменные среды?
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")

bot.infinity_polling()
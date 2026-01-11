from email import message
import os
import telebot
from logic import process_image
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, """Добро пожаловать,в бот тех подержки онлайн магазина 'предлагаем все на свете'.
                        /standart - базовые вопросы и ответы на них
                        /zadat - вы можете сами задать вопрос специалисту
                     
                     """)

@bot.message_handler(commands=["standart","стандарт"])
def standart(message):
    pass

@bot.message_handler(commands=["zadat","задать"])
def standart(message):
        bot.send_message(
        message.chat.id,
        "Опишите вашу проблему.\n"
        "Если сайт или оплата — *программисты*\n"
        "Если товар, доставка, возврат — *отдел продаж*",
        parse_mode="Markdown"
    )
        bot.register_next_step_handler(message,)

if __name__ == "__main__":
    bot.polling(none_stop=True)


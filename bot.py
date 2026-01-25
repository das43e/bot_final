from email import message
import os
import telebot
#from logic import DatabaseManeger
import logic
from config import TOKEN,DATABASE
from telebot import types

bot = telebot.TeleBot(TOKEN)
manager =logic. DatabaseManeger(DATABASE)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, """Добро пожаловать,в бот тех подержки онлайн магазина 'предлагаем все на свете'.
                        /standart - базовые вопросы и ответы на них
                        /zadat - вы можете сами задать вопрос специалисту
                     
                     """)

@bot.message_handler(commands=["standart"])        
def send_questions_menu(message):
    questions = manager.get_all_questions() # Вызов метода вашего класса БД
    markup = types.InlineKeyboardMarkup()
    print(questions)
    for row in questions:
        q_id = row[0]   # ID вопроса
        q_text = row[1] # Текст вопроса
        
        # Если текст вопроса — это тоже кортеж (из-за ошибки zip, которую обсуждали ранее),
        # берем первый элемент кортежа:
        if isinstance(q_text, tuple):
            q_text = q_text[0]

        button = types.InlineKeyboardButton(
            text=str(q_text)[:30], # Telegram ограничивает длину текста на кнопках
            callback_data=f"q_{q_id}"
        )
        markup.add(button)

    bot.send_message(message.chat.id, "Выберите интересующий вас вопрос:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('q_'))
def handle_question_click(call):
    # Извлекаем ID из callback_data (удаляем 'q_')
    question_id = call.data.replace('q_', '')
    
    # Получаем ответ из базы
    answer = manager.get_answer_by_id(question_id)
    
    # Редактируем сообщение или отправляем новое с ответом
    bot.send_message(call.message.chat.id, f"<b>Ответ:</b>\n{answer}", parse_mode='HTML')
    
    # Обязательно уведомляем Telegram, что callback обработан
    bot.answer_callback_query(call.id)

@bot.message_handler(commands=["zadat","задать"])
def standart(message):
        user_id = message.from_user.id
        bot.send_message(
        message.chat.id,
        "Опишите вашу проблему.\n"
        "Если сайт или оплата — *программисты*\n"
        "Если товар, доставка, возврат — *отдел продаж*",
    )
        bot.register_next_step_handler(message,save_request)



def save_request(message):
        text = message.text.lower()
        user_name = message.from_user.first_name
        
        if "оплат" in text or "сайт" in text:
            department = "программисты"
        else:
            department = "отдел продаж"

        data = {"request":text,
                "user_name":user_name,
                "status":"получен",
                "specialist":department, 
                  
        }
        manager.save_request(data)


        bot.send_message(
            message.chat.id,
            f"Ваш запрос передан в {department}"
        )


@bot.message_handler(func=lambda message: True)
def echo_all(message):
        bot.reply_to(message, message.text)
    
    #bot.polling()


if __name__ == "__main__":
    bot.polling(none_stop=True)


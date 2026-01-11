import sqlite3
import bot
from config import DATABASE
request = [(_,) for _ in (["Как оформить заказ?","Как оформить заказ?"," Как отменить заказ?",
                           " Как отменить заказ?","Как связаться с вашей технической поддержкой?"," Как узнать информацию о доставке?"])]
otvet = [(_,) for _ in (['Для оформления заказа, пожалуйста, выберите интересующий вас товар и нажмите кнопку "Добавить в корзину", затем перейдите в корзину и следуйте инструкциям для завершения покупки.',
                         'Вы можете узнать статус вашего заказа, войдя в свой аккаунт на нашем сайте и перейдя в раздел "Мои заказы". Там будет указан текущий статус вашего заказа.',
                         'Если вы хотите отменить заказ, пожалуйста, свяжитесь с нашей службой поддержки как можно скорее. Мы постараемся помочь вам с отменой заказа до его отправки.',
                         'При получении поврежденного товара, пожалуйста, сразу свяжитесь с нашей службой поддержки и предоставьте фотографии повреждений. Мы поможем вам с обменом или возвратом товара.',
                         ' Вы можете связаться с нашей технической поддержкой через телефон на нашем сайте или написать нам в чат-бота.',
                         'Информацию о доставке вы можете найти на странице оформления заказа на нашем сайте. Там указаны доступные способы доставки и сроки.'])]


class DatabaseManeger:
    def __init__(self,database):
        self.database = database

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''
                        CREATE TABLE IF NOT EXISTS users (
                            user_id INTEGER PRIMARY KEY,
                            user_name TEXT,
                         
                        ) 
                        
                        ''' )
            

            conn.execute('''
                        CREATE TABLE IF NOT EXISTS statuses (
                            status_id INTEGER PRIMARY KEY,
                            status_name TEXT,
                         
                        ) 
                        
                        ''' )
            
            conn.execute('''
                        CREATE TABLE IF NOT EXISTS specials (
                            special_id INTEGER PRIMARY KEY,
                            special_name TEXT,
                            info TEXT
                        ) 
                        
                        ''' )
            
            conn.execute('''
                        CREATE TABLE IF NOT EXISTS  standart_request(
                            request_id INTEGER PRIMARY KEY,
                            request TEXT,
                            otvet TEXT
                         
                        ) 
                        
                        ''' )
            
            conn.execute('''
                        CREATE TABLE IF NOT EXISTS requests (
                            request_id INTEGER PRIMARY KEY,
                            request TEXT,
                            user_id INTEGER,
                            status_id INTEGER,
                            special_id INTEGER,
                            FOREIGN KEY (user_id) REFERENCES users(user_id),
                            FOREIGN KEY (status_id) REFERENCES statuses(status_id),
                            FOREIGN  KEY (special_id) REFERENCES specials(special_id)
                        )
                        ''')
            conn.commit()
            
    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()

    def __select_data(self, sql, data = tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()


    def save_request(message):
        text = message.text.lower()

        if "оплат" in text or "сайт" in text:
            department = "программисты"
        else:
            department = "отдел продаж"

        bot.send_message(
            message.chat.id,
            f"Ваш запрос передан в {department}"
        )


    def default_insert(self):
        sql = 'INSERT OR IGNORE INTO standart_request (request) values(?)'
        data = request
        self.__executemany(sql, data)
        sql = 'INSERT OR IGNORE INTO standart_request (otvet) values(?)'
        data = otvet
        self.__executemany(sql, data)

    def add_user(self, user_id, user_name):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('INSERT OR IGNORE INTO users (user_id, user_name) VALUES (?, ?)', 
                         (user_id, user_name))
            conn.commit()

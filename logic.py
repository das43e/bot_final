import sqlite3
from config import DATABASE
request = [(_,) for _ in (["Как оформить заказ?",
                           "Как оформить заказ?",
                           "Как отменить заказ?",
                           "Как отменить заказ?",
                           "Как связаться с вашей технической поддержкой?",
                           "Как узнать информацию о доставке?"])]
otvet = [(_,) for _ in (['Для оформления заказа, пожалуйста, выберите интересующий вас товар и нажмите кнопку "Добавить в корзину", затем перейдите в корзину и следуйте инструкциям для завершения покупки.',
                         'Вы можете узнать статус вашего заказа, войдя в свой аккаунт на нашем сайте и перейдя в раздел "Мои заказы". Там будет указан текущий статус вашего заказа.',
                         'Если вы хотите отменить заказ, пожалуйста, свяжитесь с нашей службой поддержки как можно скорее. Мы постараемся помочь вам с отменой заказа до его отправки.',
                         'При получении поврежденного товара, пожалуйста, сразу свяжитесь с нашей службой поддержки и предоставьте фотографии повреждений. Мы поможем вам с обменом или возвратом товара.',
                         'Вы можете связаться с нашей технической поддержкой через телефон на нашем сайте или написать нам в чат-бота.',
                         'Информацию о доставке вы можете найти на странице оформления заказа на нашем сайте. Там указаны доступные способы доставки и сроки.'])]


class DatabaseManeger:
    def __init__(self,database):
        self.database = database

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            
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
                            user_name TEXT,
                            status TEXT,
                            special_name TEXT
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





    def default_insert(self):
# Объединяем два списка в список кортежей: [(req1, otv1), (req2, otv2), ...]
        data = [(r[0], o[0]) for r, o in zip(request, otvet)]
        
    # Один запрос для вставки в обе колонки сразу
        sql = 'INSERT OR IGNORE INTO standart_request (request, otvet) VALUES (?, ?)'
    
    # Выполняем вставку всех пар данных
        self.__executemany(sql, data)
    def add_user(self, user_id, user_name):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('INSERT OR IGNORE INTO users (user_id, user_name) VALUES (?, ?)', 
                         (user_id, user_name))
            conn.commit()

    def save_request(self, data):
        sql = "INSERT INTO requests (request,user_name,status,special_name) VALUES (?,?,?,?)"
        self.__executemany(sql, [(data["request"],data["user_name"],data["status"],data["specialist"])])

    def get_all_questions(self):
        # Получаем ID и текст вопроса
        sql = 'SELECT request_id, request FROM standart_request'
        return self.__select_data(sql)

    def get_answer_by_id(self, q_id):
        # Получаем ответ по ID
        sql = 'SELECT otvet FROM standart_request WHERE request_id = ?'
        result = self.__select_data(sql, (q_id,))
        
        # result — это список кортежей, например [('Текст ответа',)]
        if result:
            return result[0][0] # Берем первый элемент первого кортежа
        return "Ответ не найден."





if __name__ == '__main__':
    manager = DatabaseManeger(DATABASE)
    manager.create_tables()
    manager.default_insert()
  

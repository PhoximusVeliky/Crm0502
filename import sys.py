import pymysql

def create_connection():
    """
    Создаёт соединение с одной статичной базой данных.
    """
    connection = None
    try:
        connection = pymysql.connect(
            host='5.183.188.132',      # Хост базы данных
            user='host',           # Пользователь базы данных
            password='thasrCt3pKYWAYcK', # Пароль пользователя
            db='db_vgu_test2'  # Название базы данных
        )
        print("Соединение с базой данных успешно установлено.")
    except pymysql.MySQLError as e:
        print(f"Ошибка подключения к базе данных: {e}")
    return connection

def main():
    create_connection()
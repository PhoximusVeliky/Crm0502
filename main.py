import pymysql

def create_connection():
    """
    Создаёт соединение с одной статичной базой данных.
    """
    connection = None
    try:
        connection = pymysql.connect(
            host='127.0.0.1',      # Хост базы данных
            user='root',           # Пользователь базы данных
            password='1234', # Пароль пользователя
            db='crm'  # Название базы данных
        )
        print("Соединение с базой данных успешно установлено.")
    except pymysql.MySQLError as e:
        print(f"Ошибка подключения к базе данных: {e}")
    return connection

# Пример использования
connection = create_connection()
if connection:
    # Действия с базой данных
    print("Работа с базой данных...")
    connection.close()
    print("Соединение закрыто.")
    
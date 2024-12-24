import pymysql

def create_connection():
    """
    Создаёт соединение с одной статичной базой данных.
    """
    connection = None
    try:
        connection = pymysql.connect(
            host='5.183.188.132',      # Хост базы данных
            user='db_vgu_student',           # Пользователь базы данных
            password='thasrCt3pKYWAYcK', # Пароль пользователя
            db='db_vgu_test2'  # Название базы данных
        )
        print("Соединение с базой данных успешно установлено.")
    except pymysql.MySQLError as e:
        print(f"Ошибка подключения к базе данных: {e}")
    return connection

def fetch_banners(connection):
    """
    Выполняет запрос для получения всех данных из таблицы banner.
    """
    try:
        with connection.cursor() as cursor:
            sql_query = "SELECT * FROM `banner`;"
            cursor.execute(sql_query)
            results = cursor.fetchall()
            for row in results:
                print(row)  # Выводим каждую строку
    except pymysql.MySQLError as e:
        print(f"Ошибка выполнения SQL-запроса: {e}")

# Пример использования
connection = create_connection()
if connection:
    fetch_banners(connection)  # Выполняем запрос
    connection.close()
    print("Соединение закрыто.")
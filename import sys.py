import pymysql

def create_connection():
    """
    Создаёт соединение с базой данных MySQL.
    """
    connection = None
    try:
        connection = pymysql.connect(
            host='127.0.0.1',  # Локальный хост
            user='root',       # Пользователь базы данных
            password='1234',   # Пароль пользователя
            db='CRM',          # Название базы данных
            cursorclass=pymysql.cursors.DictCursor  # Получение результатов в виде словаря
        )
        print("Соединение с базой данных успешно установлено.")
    except pymysql.MySQLError as e:
        print(f"Ошибка подключения к базе данных: {e}")
    return connection

def fetch_sales():
    """
    Выполняет запрос к таблице Sales и выводит результаты.
    """
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql_query = "SELECT * FROM Sales;"
                cursor.execute(sql_query)
                results = cursor.fetchall()  # Получаем все строки результата

                for row in results:
                    print(row)  # Выводим каждую строку

        except pymysql.MySQLError as e:
            print(f"Ошибка выполнения SQL-запроса: {e}")
        finally:
            connection.close()
            print("Соединение закрыто.")

# Вызов функции для получения данных из таблицы Sales
fetch_sales()

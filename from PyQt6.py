from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QWidget, QGridLayout, QScrollArea, QDialog, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QFont
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QGridLayout,
    QFrame,
    QHBoxLayout,
    QTableWidgetItem, QSpinBox, QLineEdit, QPushButton,

)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, QPoint
import pymysql
import pymysql
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

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

def create_side_menu(button_callbacks):
    panel_widget = QWidget()
    panel_widget.setStyleSheet("background-color: #2A5266; border-radius: 0px;")
    panel_widget.setFixedWidth(600)

    panel_layout = QVBoxLayout(panel_widget)
    panel_layout.setContentsMargins(10, 20, 10, 20)
    panel_layout.setSpacing(50)

    panel_layout.addStretch()

    buttons = ["главная", "каталог", "проданные товары", "оформить карту", "продажа"]
    for button_text, callback in zip(buttons, button_callbacks):
        button = QPushButton(button_text)

        if button_text == "продажа":
            button.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    border: none;
                    border-radius: 100px;
                    padding: 20px;
                    font-size: 20px;
                    font-family: "Inter";
                }
                QPushButton:hover {
                    background-color: #3C7993;
                }
            """)
            button.setFixedSize(400, 200)
        else:
            button.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    border: none;
                    border-radius: 75px;
                    padding: 10px;
                    font-size: 20px;
                    font-family: "Inter";
                }
                QPushButton:hover {
                    background-color: #3C7993;
                }
            """)
            button.setFixedSize(300, 150)

        button.clicked.connect(callback)
        panel_layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

    panel_layout.addStretch()
    return panel_widget

def create_top_bar():
    top_bar = QWidget()
    top_bar.setStyleSheet("background-color: #3C7993;")
    top_bar.setFixedHeight(50)

    logo = QLabel("Игровая полка", top_bar)
    logo.setFont(QFont("Inter", 20))
    logo.setStyleSheet("color: #FFFFFF;")
    logo.setGeometry(200, 10, 200, 30)

    search_box = QLineEdit(top_bar)
    search_box.setPlaceholderText("поиск по продажам")
    search_box.setStyleSheet("""
        QLineEdit {
            background-color: white;
            border: 1px solid #d9d9d9;
            border-radius: 10px;
            padding: 8px 15px;
            font-size: 14px;
        }
    """)
    search_box.setGeometry(600, 10, 800, 30)

    return top_bar, search_box


class MainPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        # Добавляем отступы для основного макета
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Заголовок
        title = QLabel("Жанры")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #2A5266;")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # Создаем виджет для прокрутки
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Для автоматической подгонки размера
        layout.addWidget(scroll_area)

        # Создаем виджет, который будет внутри QScrollArea
        scroll_widget = QWidget()
        scroll_area.setWidget(scroll_widget)

        # Сетка жанров внутри прокручиваемого виджета
        genres_layout = QGridLayout(scroll_widget)
        genres_layout.setHorizontalSpacing(30)
        genres_layout.setVerticalSpacing(20)

        # Получаем жанры из базы данных
        genres = self.get_genres()

        # Добавляем жанры в сетку
        for row in range(4):  # 4 строки
            for col in range(3):  # 3 колонки
                index = row * 3 + col
                if index < len(genres):
                    genre_name = genres[index]['name']
                    
                    # Создаем контейнер для изображения и текста
                    genre_widget = QWidget()
                    genre_widget.setStyleSheet("""
                        QWidget {
                            background-color: white;
                            border: 1px solid #2A5266;
                            border-radius: 10px;
                            padding: 10px;
                            text-align: center;
                        }
                    """)
                    genre_layout = QVBoxLayout(genre_widget)

                    # Создаем и добавляем изображение
                    genre_label_image = QLabel()
                    pixmap = QPixmap("00.jpg")  # Замените на путь к изображению
                    scaled_pixmap = pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    genre_label_image.setPixmap(scaled_pixmap)
                    genre_layout.addWidget(genre_label_image, alignment=Qt.AlignmentFlag.AlignCenter)

                    # Создаем и добавляем текст
                    genre_label_text = QLabel(genre_name)
                    genre_label_text.setFont(QFont("Arial", 14))
                    genre_label_text.setStyleSheet("color: #2A5266; font-weight: bold;")
                    genre_label_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    genre_layout.addWidget(genre_label_text)

                    genres_layout.addWidget(genre_widget, row, col, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)

    # Функция для получения всех жанров из базы данных
    def get_genres(self):
        connection = create_connection()
        genres = []
        if connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM Genres")
                    genres = cursor.fetchall()
            except pymysql.MySQLError as e:
                print(f"Ошибка выполнения запроса: {e}")
            finally:
                connection.close()
        return genres

class ProductDetailsWindow(QWidget):
    def __init__(self, parent, product_info, image_path):
        super().__init__()
        self.parent = parent  # Сохраняем ссылку на родителя для возврата

        self.setWindowTitle("Подробности о товаре")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout(self)

        # Добавляем изображение товара
        image_label = QLabel(self)
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            image_label.setText("Изображение не загружено")
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            image_label.setStyleSheet("color: red; font-size: 14px;")
        else:
            image_label.setPixmap(pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(image_label)

        # Добавляем описание товара
        info_label = QLabel(product_info)
        info_label.setWordWrap(True)
        info_label.setStyleSheet("""
            font-size: 14px;
            color: #333333;
            margin-top: 10px;
        """)
        layout.addWidget(info_label)

        # Кнопка возврата
        back_button = QPushButton("Назад", self)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #3C7993;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2A5266;
            }
        """)
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button)

    def go_back(self):
        self.close()  # Закрываем текущее окно
        self.parent.show()  # Показываем родительское окно

# class CatalogPage(QWidget):
#     def __init__(self):
#         super().__init__()

#         # Основной layout
#         self.main_layout = QHBoxLayout(self)
#         self.main_layout.setContentsMargins(20, 20, 20, 20)
#         self.main_layout.setSpacing(20)

#         # Создаем QScrollArea для добавления скролла (слева от панели с деталями)
#         self.scroll_area = QScrollArea(self)
#         self.scroll_area.setWidgetResizable(True)

#         # Вложенный виджет, который будет содержать все товары
#         self.scroll_widget = QWidget()
#         self.scroll_layout = QVBoxLayout(self.scroll_widget)
#         self.scroll_layout.setContentsMargins(0, 0, 0, 0)
#         self.scroll_layout.setSpacing(10)

#         # Сетка товаров
#         self.grid_layout = QGridLayout()
#         self.grid_layout.setHorizontalSpacing(30)
#         self.grid_layout.setVerticalSpacing(30)
#         self.scroll_layout.addLayout(self.grid_layout)

#         # Путь к изображениям
#         images = ["00.jpg"] * 6  # Используйте свои изображения для реального приложения

#         # Добавление карточек в сетку
#         for row in range(2):  # Количество строк
#             for col in range(3):  # Количество столбцов
#                 card_widget = QWidget()
#                 card_widget.setStyleSheet(""" 
#                     QWidget { 
#                         background-color: white; 
#                         border: 1px solid #d9d9d9; 
#                         border-radius: 10px; 
#                     } 
#                 """)
#                 card_layout = QVBoxLayout(card_widget)
#                 card_layout.setContentsMargins(10, 10, 10, 10)
#                 card_layout.setSpacing(10)

#                 # Информация о товаре
#                 product_info = f"Название: Товар {row * 3 + col + 1}\nЖанр: Жанр {row * 3 + col + 1}\nЦена: {100 * (row * 3 + col + 1)} руб."
#                 image_path = images[row * 3 + col]

#                 # Изображение товара
#                 image_label = QLabel(self)
#                 pixmap = QPixmap(image_path)
#                 image_label.setPixmap(pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))
#                 image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

#                 # Добавляем обработчик события
#                 image_label.mousePressEvent = lambda event, p=image_path, i=product_info: self.show_product_details(p, i)

#                 card_layout.addWidget(image_label)

#                 # Кнопка "добавить"
#                 add_button = QPushButton("добавить")
#                 add_button.setStyleSheet(""" 
#                     QPushButton { 
#                         background-color: #3C7993; 
#                         color: white; 
#                         border: none; 
#                         border-radius: 5px; 
#                         font-size: 14px; 
#                         padding: 10px; 
#                     } 
#                     QPushButton:hover { 
#                         background-color: #2A5266; 
#                     } 
#                 """)
#                 add_button.setFixedHeight(40)
#                 card_layout.addWidget(add_button)

#                 # Добавление карточки в сетку
#                 self.grid_layout.addWidget(card_widget, row, col)

#         # Добавляем ScrollArea в основной layout
#         self.scroll_area.setWidget(self.scroll_widget)
#         self.main_layout.addWidget(self.scroll_area)

#         # Панель для деталей товара
#         self.details_panel = QFrame(self)
#         self.details_panel.setFixedWidth(300)
#         self.details_panel.setStyleSheet(""" 
#             QFrame { 
#                 background-color: #f9f9f9; 
#                 border: 1px solid #d9d9d9; 
#                 border-radius: 10px; 
#             } 
#         """)
#         self.details_layout = QVBoxLayout(self.details_panel)
#         self.details_layout.setContentsMargins(20, 20, 20, 20)
#         self.details_layout.setSpacing(10)

#         self.details_panel.hide()  # Скрываем по умолчанию
#         self.main_layout.addWidget(self.details_panel)  # Добавляем справа

#     def show_product_details(self, image_path, product_info):
#         # Удаляем старое содержимое панели
#         for i in reversed(range(self.details_layout.count())):
#             widget_item = self.details_layout.itemAt(i).widget()
#             if widget_item:
#                 widget_item.deleteLater()

#         # Добавляем изображение товара
#         image_label = QLabel(self)
#         pixmap = QPixmap(image_path)
#         if pixmap.isNull():
#             image_label.setText("Изображение не загружено")
#             image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#             image_label.setStyleSheet("color: red; font-size: 14px;")
#         else:
#             image_label.setPixmap(pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))
#             image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.details_layout.addWidget(image_label)

#         # Добавляем информацию о товаре
#         info_label = QLabel(product_info)
#         info_label.setWordWrap(True)
#         info_label.setStyleSheet("""
#             font-size: 14px;
#             color: #333333;
#             margin-top: 10px;
#         """)
#         self.details_layout.addWidget(info_label)

#         # Кнопка "Показать больше"
#         show_more_button = QPushButton("Показать больше", self)
#         show_more_button.setStyleSheet("""
#             QPushButton {
#                 background-color: #3C7993;
#                 color: white;
#                 border: none;
#                 border-radius: 5px; 
#                 font-size: 14px;
#                 padding: 10px;
#             }
#             QPushButton:hover {
#                 background-color: #2A5266;
#             }
#         """)
#         show_more_button.setFixedHeight(40)
#         show_more_button.clicked.connect(self.show_more_details)
#         self.details_layout.addWidget(show_more_button)

#         # Делаем панель видимой
#         self.details_panel.show()

#     def show_more_details(self):
#         # Скрываем каталог и панель с деталями товара
#         self.scroll_area.hide()
#         self.details_panel.hide()

#         # Создаем новый виджет с подробной информацией
#         self.more_details_widget = QWidget(self)
#         more_details_layout = QVBoxLayout(self.more_details_widget)
#         more_details_layout.setContentsMargins(20, 20, 20, 20)
#         more_details_layout.setSpacing(10)

#         # Пример подробной информации
#         more_details_layout.addWidget(QLabel("Дополнительная информация о товаре"))

#         # Кнопка для возврата
#         back_button = QPushButton("Назад", self)
#         back_button.clicked.connect(self.back_to_details)
#         more_details_layout.addWidget(back_button)

#         # Добавляем новый виджет в основной layout
#         self.main_layout.addWidget(self.more_details_widget)

#     def back_to_details(self):
#         # Убираем подробную информацию и показываем каталог и панель с деталями товара
#         self.more_details_widget.deleteLater()
#         self.scroll_area.show()
#         self.details_panel.show()

class CatalogPage(QWidget):
    def __init__(self):
        super().__init__()

        # Основной layout
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        # Создаем QScrollArea для добавления скролла (слева от панели с деталями)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        # Вложенный виджет, который будет содержать все товары
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(10)

        # Сетка товаров
        self.grid_layout = QGridLayout()
        self.grid_layout.setHorizontalSpacing(30)
        self.grid_layout.setVerticalSpacing(30)
        self.scroll_layout.addLayout(self.grid_layout)

        # Загрузка данных из базы
        self.load_products()

        # Добавляем ScrollArea в основной layout
        self.scroll_area.setWidget(self.scroll_widget)
        self.main_layout.addWidget(self.scroll_area)

        # Панель для деталей товара
        self.details_panel = QFrame(self)
        self.details_panel.setFixedWidth(300)
        self.details_panel.setStyleSheet(""" 
            QFrame { 
                background-color: #f9f9f9; 
                border: 1px solid #d9d9d9; 
                border-radius: 10px; 
            } 
        """)
        self.details_layout = QVBoxLayout(self.details_panel)
        self.details_layout.setContentsMargins(20, 20, 20, 20)
        self.details_layout.setSpacing(10)

        self.details_panel.hide()  # Скрываем по умолчанию
        self.main_layout.addWidget(self.details_panel)  # Добавляем справа

    def load_products(self):
        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT 
                            p.id_product,
                            p.name, 
                            GROUP_CONCAT(g.name SEPARATOR ', ') AS genres, 
                            p.price, 
                            p.age_category, 
                            p.difficulty, 
                            i.image_path
                        FROM Products p
                        LEFT JOIN Product_Genres pg ON p.id_product = pg.id_product
                        LEFT JOIN Genres g ON pg.id_genre = g.id_genre
                        LEFT JOIN Images i ON p.id_product = i.id_product
                        GROUP BY p.id_product, p.name, p.price, p.age_category, p.difficulty, i.image_path
                    """)

                    products = cursor.fetchall()
                    row, col = 0, 0
                    for product in products:
                        self.add_product_card(product, row, col)
                        col += 1
                        if col == 3:
                            col = 0
                            row += 1
            finally:
                connection.close()

    def add_product_card(self, product, row, col):
        card_widget = QWidget()
        card_widget.setStyleSheet(""" 
            QWidget { 
                background-color: white; 
                border: 1px solid #d9d9d9; 
                border-radius: 10px; 
            } 
        """)
        card_layout = QVBoxLayout(card_widget)
        card_layout.setContentsMargins(10, 10, 10, 10)
        card_layout.setSpacing(10)

        product_info = f"Название: {product['name']}\nЖанры: {product['genres']}\nЦена: {product['price']} руб.\nВозраст: {product['age_category']}\nСложность: {product['difficulty']}"
        image_path = product['image_path'] if product['image_path'] else 'placeholder.jpg'

        image_label = QLabel(self)
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            image_label.setText("Изображение не загружено")
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            image_label.setStyleSheet("color: red; font-size: 14px;")
        else:
            image_label.setPixmap(pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.mousePressEvent = lambda event, p=image_path, i=product_info: self.show_product_details(p, i)

        card_layout.addWidget(image_label)
        add_button = QPushButton("добавить")
        add_button.setStyleSheet(""" 
            QPushButton { 
                background-color: #3C7993; 
                color: white; 
                border: none; 
                border-radius: 5px; 
                font-size: 14px; 
                padding: 10px; 
            } 
            QPushButton:hover { 
                background-color: #2A5266; 
            } 
        """)
        add_button.setFixedHeight(40)
        card_layout.addWidget(add_button)
        self.grid_layout.addWidget(card_widget, row, col)

    def show_product_details(self, image_path, product_info):
        for i in reversed(range(self.details_layout.count())):
            widget_item = self.details_layout.itemAt(i).widget()
            if widget_item:
                widget_item.deleteLater()

        image_label = QLabel(self)
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            image_label.setText("Изображение не загружено")
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            image_label.setStyleSheet("color: red; font-size: 14px;")
        else:
            image_label.setPixmap(pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.details_layout.addWidget(image_label)

        info_label = QLabel(product_info)
        info_label.setWordWrap(True)
        info_label.setStyleSheet("""
            font-size: 14px;
            color: #333333;
            margin-top: 10px;
        """)
        self.details_layout.addWidget(info_label)
        self.details_panel.show()


class SoldItemsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        title = QLabel("Проданные товары")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title.setStyleSheet("color: #2A5266; margin-bottom: 20px;")
        layout.addWidget(title)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background-color: white; border: none;")
        layout.addWidget(scroll_area)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(10, 10, 10, 10)
        scroll_layout.setSpacing(10)

        connection = create_connection()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT Sales.id_sale, Sales.sale_date, Sales_Details.quantity
                    FROM Sales
                    JOIN Sales_Details ON Sales.id_sale = Sales_Details.id_sale;
                """)
                results = cursor.fetchall()
                for row in results:
                    sale_widget = QWidget()
                    sale_widget.setStyleSheet("""
                        QWidget {
                            background-color: #f9f9f9;
                            border: 1px solid #d9d9d9;
                            border-radius: 5px;
                        }
                    """)
                    sale_layout = QVBoxLayout(sale_widget)
                    sale_layout.setContentsMargins(10, 10, 10, 10)
                    sale_layout.setSpacing(5)

                    sale_info = QLabel(f"Дата продажи: {row['sale_date']} Количество наименований: {row['quantity']}")
                    sale_info.setStyleSheet("font-size: 14px; color: #333333;")
                    sale_layout.addWidget(sale_info)

                    more_button = QPushButton("показать больше")
                    more_button.setStyleSheet("""
                        QPushButton {
                            background-color: #3C7993;
                            color: white;
                            border: none;
                            border-radius: 5px;
                            font-size: 14px;
                            padding: 5px;
                        }
                        QPushButton:hover {
                            background-color: #2A5266;
                        }
                    """)
                    more_button.clicked.connect(lambda _, sale_id=row['id_sale']: self.show_more_info(sale_id))
                    sale_layout.addWidget(more_button, alignment=Qt.AlignmentFlag.AlignRight)

                    scroll_layout.addWidget(sale_widget)
            connection.close()

        scroll_area.setWidget(scroll_content)

    def show_more_info(self, sale_id):
        details_window = QDialog()
        details_window.setWindowTitle("Подробности продажи")
        details_window.setStyleSheet("background-color: white;")

        details_layout = QVBoxLayout(details_window)

        title = QLabel(f"Детали продажи №{sale_id}")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #2A5266;")
        details_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        table = QTableWidget(0, 3)
        table.setHorizontalHeaderLabels(["Наименование", "Кол-во", "Цена за шт"])

        total_price = 0  # Для подсчета итоговой суммы

        connection = create_connection()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT Products.name, Sales_Details.quantity, Products.price
                    FROM Sales_Details
                    JOIN Products ON Sales_Details.id_product = Products.id_product
                    WHERE Sales_Details.id_sale = %s
                """, (sale_id,))
                results = cursor.fetchall()
                for row_index, row in enumerate(results):
                    table.insertRow(row_index)
                    table.setItem(row_index, 0, QTableWidgetItem(row['name']))
                    table.setItem(row_index, 1, QTableWidgetItem(str(row['quantity'])))
                    table.setItem(row_index, 2, QTableWidgetItem(str(row['price'])))
                    
                    # Рассчитываем общую стоимость для каждого товара
                    total_price += row['quantity'] * row['price']
            connection.close()

        details_layout.addWidget(table)

        # Добавляем метку с итоговой суммой
        total_label = QLabel(f"Итого: {total_price:.2f}")
        total_label.setFont(QFont("Arial", 14))
        total_label.setStyleSheet("color: #2A5266;")
        details_layout.addWidget(total_label, alignment=Qt.AlignmentFlag.AlignRight)

        details_window.setLayout(details_layout)
        details_window.exec()

class ApplyCardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        # Заголовок
        title = QLabel("Оформление карты")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title.setStyleSheet("color: #2A5266; margin-bottom: 20px;")
        self.layout.addWidget(title)

        # Поля ввода
        self.inputs = {}
        fields = ["ФИО клиента", "номер телефона", "e-mail", "номер карты"]
        for field in fields:
            label = QLabel(field)
            label.setFont(QFont("Arial", 14))
            label.setStyleSheet("color: #2A5266;")
            self.layout.addWidget(label)

            input_field = QLineEdit()
            input_field.setStyleSheet("""
                QLineEdit {
                    background-color: white;
                    border: 1px solid #d9d9d9;
                    border-radius: 5px;
                    padding: 10px;
                    font-size: 14px;
                }
            """)
            self.layout.addWidget(input_field)
            self.inputs[field] = input_field

        # Кнопка подтверждения
        confirm_button = QPushButton("Подтвердить")
        confirm_button.setStyleSheet("""
            QPushButton {
                background-color: #3C7993;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2A5266;
            }
        """)
        confirm_button.setFixedHeight(50)
        confirm_button.clicked.connect(self.save_to_db)
        self.layout.addWidget(confirm_button, alignment=Qt.AlignmentFlag.AlignRight)

    def save_to_db(self):
        """Сохраняет данные из формы в базу данных."""
        try:
            # Считываем данные из полей ввода
            client_name = self.inputs["ФИО клиента"].text()
            phone_number = self.inputs["номер телефона"].text()
            email = self.inputs["e-mail"].text()
            card_number = self.inputs["номер карты"].text()

            # Проверяем, что поля не пустые
            if not all([client_name, phone_number, email, card_number]):
                QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
                return

            # Подключение к базе данных
            connection = create_connection()
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Clients (client_name, phone_number, email, card_number)
                    VALUES (%s, %s, %s, %s)
                """, (client_name, phone_number, email, card_number))
                connection.commit()

            QMessageBox.information(self, "Успех", "Данные успешно сохранены!")
            # Очищаем поля
            for field in self.inputs.values():
                field.clear()

        except pymysql.MySQLError as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось сохранить данные: {e}")
        finally:
            if 'connection' in locals() and connection.open:
                connection.close()

class SalePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Заголовок страницы
        title = QLabel("Продажа")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title.setStyleSheet("color: #2A5266; margin-bottom: 20px;")
        layout.addWidget(title)

        # Прокручиваемая область для товаров
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Включаем возможность прокрутки
        scroll_area.setStyleSheet("background-color: white; border: none;")
        layout.addWidget(scroll_area)

        # Контейнер для списка товаров
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(10, 10, 10, 10)
        scroll_layout.setSpacing(10)

        # Пример списка товаров с кнопками увеличения/уменьшения
        self.cart = {}
        button_style = """
            QPushButton {
                background-color: #3C7993;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #2A5266;
            }
        """
        for i in range(5):
            item_widget = QWidget()
            item_widget.setStyleSheet("""
                QWidget {
                    background-color: #f9f9f9;
                    border: 1px solid #d9d9d9;
                    border-radius: 5px;
                }
            """)
            item_layout = QHBoxLayout(item_widget)
            item_layout.setContentsMargins(10, 10, 10, 10)
            item_layout.setSpacing(10)  # Добавляем отступ между элементами

            # Изображение товара (квадратное)
            item_image = QLabel()
            item_image.setFixedSize(200, 200)  # Картинка квадратная
            item_image.setPixmap(QPixmap("00.jpg").scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
            item_layout.addWidget(item_image)

            # Название товара
            item_label = QLabel(f"Товар {i + 1}")
            item_label.setStyleSheet("font-size: 14px; color: #333333;")
            item_layout.addWidget(item_label)

            # Кнопки изменения количества
            decrease_button = QPushButton("-")
            decrease_button.setFixedSize(50, 50)  # Размер кнопки "минус"
            decrease_button.setStyleSheet(button_style)
            decrease_button.clicked.connect(lambda _, item_id=i: self.update_cart(item_id, -1))
            item_layout.addWidget(decrease_button)

            # Метка для отображения количества, фиксированная ширина
            quantity_label = QLabel("0")
            quantity_label.setFixedSize(30, 50)  # Устанавливаем фиксированную ширину и высоту
            quantity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            item_layout.addWidget(quantity_label)

            # Кнопка увеличения количества
            increase_button = QPushButton("+")
            increase_button.setFixedSize(50, 50)  # Размер кнопки "плюс"
            increase_button.setStyleSheet(button_style)
            increase_button.clicked.connect(lambda _, item_id=i: self.update_cart(item_id, 1))
            item_layout.addWidget(increase_button)

            scroll_layout.addWidget(item_widget)

            # Сохраняем связь товара с виджетами
            self.cart[i] = {"label": item_label, "quantity_label": quantity_label, "quantity": 0}

        scroll_area.setWidget(scroll_content)

        # Общая сумма
        self.total_label = QLabel("Итого: 0")
        self.total_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.total_label.setStyleSheet("color: #2A5266; margin-top: 20px;")
        layout.addWidget(self.total_label, alignment=Qt.AlignmentFlag.AlignRight)

        # Кнопка завершения покупки
        confirm_button = QPushButton("Завершить покупку")
        confirm_button.setStyleSheet("""
            QPushButton {
                background-color: #3C7993;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2A5266;
            }
        """)
        confirm_button.clicked.connect(self.complete_purchase)
        layout.addWidget(confirm_button, alignment=Qt.AlignmentFlag.AlignRight)

        # Настроим растягивание: прокручиваемая область будет растягиваться
        layout.setStretch(0, 0)  # Заголовок не растягивается
        layout.setStretch(1, 1)  # Прокручиваемая область будет растягиваться
        layout.setStretch(2, 0)  # Общая сумма не растягивается
        layout.setStretch(3, 0)  # Кнопка завершения покупки не растягивается

    def update_cart(self, item_id, change):
        item = self.cart[item_id]
        item["quantity"] += change
        if item["quantity"] < 0:
            item["quantity"] = 0
        item["quantity_label"].setText(str(item["quantity"]))

        self.update_total()

    def update_total(self):
        total = sum(item["quantity"] * 100 for item in self.cart.values())  # Пример: цена каждого товара = 100
        self.total_label.setText(f"Итого: {total}")

    def complete_purchase(self):
        print("Покупка завершена")
        self.sale_dialog = SaleDialog()  # Сохраняем ссылку на объект
        self.sale_dialog.show()

class SaleDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Продажа")
        self.setStyleSheet("background-color: white;")
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout(self)

        title = QLabel("Оформление продажи")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #2A5266;")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Название", "Количество", "Цена за шт"])
        layout.addWidget(self.table)

        controls_layout = QHBoxLayout()

        total_label = QLabel("Итого: ")
        total_label.setFont(QFont("Arial", 14))
        total_label.setStyleSheet("color: #2A5266;")
        controls_layout.addWidget(total_label)

        self.total_field = QLineEdit()
        self.total_field.setReadOnly(True)
        self.total_field.setText("0")
        controls_layout.addWidget(self.total_field)

        confirm_button = QPushButton("Подтвердить")
        confirm_button.setStyleSheet("background-color: #3C7993; color: white;")
        confirm_button.clicked.connect(self.finalize_sale)
        controls_layout.addWidget(confirm_button)

        layout.addLayout(controls_layout)

        self.add_test_data()

    def add_test_data(self):
        items = [("Товар 1", 2, 500), ("Товар 2", 1, 300), ("Товар 3", 4, 200)]
        for name, quantity, price in items:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(name))

            quantity_spinbox = QSpinBox()
            quantity_spinbox.setValue(quantity)
            quantity_spinbox.setMinimum(1)
            quantity_spinbox.valueChanged.connect(self.update_total)
            self.table.setCellWidget(row_position, 1, quantity_spinbox)

            self.table.setItem(row_position, 2, QTableWidgetItem(str(price)))
        self.update_total()

    def update_total(self):
        total = 0
        for row in range(self.table.rowCount()):
            price_item = self.table.item(row, 2)
            quantity_widget = self.table.cellWidget(row, 1)
            if price_item and quantity_widget:
                total += int(price_item.text()) * quantity_widget.value()
        self.total_field.setText(str(total))

    def confirm_sale(self):
        total = self.total_field.text()
        confirmation_dialog = QDialog(self)
        confirmation_dialog.setWindowTitle("Подтверждение продажи")
        confirmation_dialog.setMinimumSize(300, 150)
        dialog_layout = QVBoxLayout(confirmation_dialog)

        confirm_message = QLabel(f"Вы подтверждаете продажу на сумму {total}?")
        dialog_layout.addWidget(confirm_message, alignment=Qt.AlignmentFlag.AlignCenter)

        button_layout = QHBoxLayout()

        yes_button = QPushButton("Да")
        yes_button.clicked.connect(lambda: self.finalize_sale(confirmation_dialog))
        button_layout.addWidget(yes_button)

        no_button = QPushButton("Нет")
        no_button.clicked.connect(confirmation_dialog.reject)
        button_layout.addWidget(no_button)

        dialog_layout.addLayout(button_layout)
        confirmation_dialog.exec()

    def finalize_sale(self, confirmation_dialog):
        print("Продажа подтверждена на сумму:", self.total_field.text())
        self.close()  # Закрываем окно после подтверждения

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Игровая полка")

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        main_widget.setStyleSheet("background-color: #e6e6e6;")

        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Верхняя полоска
        self.top_bar, self.search_box = create_top_bar()
        main_layout.addWidget(self.top_bar)

        # Основное содержимое
        main_content = QHBoxLayout()
        main_content.setContentsMargins(0, 0, 0, 0)
        main_content.setSpacing(0)
        main_layout.addLayout(main_content)

        # Функции для кнопок бокового меню
        button_callbacks = [
            lambda: self.switch_page("main"),
            lambda: self.switch_page("catalog"),
            lambda: self.switch_page("sold_items"),
            lambda: self.switch_page("apply_card"),
            lambda: self.switch_page("sale")
        ]

        # Боковое меню
        side_menu = create_side_menu(button_callbacks)
        main_content.addWidget(side_menu)

        # Динамическое содержимое
        self.content_area = QVBoxLayout()
        self.content_area.setContentsMargins(10, 10, 10, 10)
        main_content.addLayout(self.content_area)

        # Страницы
        self.pages = {
            "main": MainPage(),
            "catalog": CatalogPage(),
            "sold_items": SoldItemsPage(),
            "apply_card": ApplyCardPage(),
            "sale": SalePage()
        }

        self.current_page = None
        self.switch_page("main")

    def switch_page(self, page_name):
        if self.current_page is not None:
            # Убираем текущую страницу из центрального макета
            self.content_area.itemAt(0).widget().setParent(None)

            # Если текущая страница — CatalogPage, скрываем панель деталей
            if isinstance(self.current_page, CatalogPage):
                self.current_page.details_panel.hide()

        # Настраиваем плейсхолдер поиска
        if page_name == "sold_items":
            self.search_box.setPlaceholderText("поиск по продажам")
        else:
            self.search_box.setPlaceholderText("поиск")

        # Добавляем новую страницу
        self.content_area.addWidget(self.pages[page_name])
        self.current_page = self.pages[page_name]


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()
    sys.exit(app.exec())

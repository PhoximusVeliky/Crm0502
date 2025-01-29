from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QWidget, QGridLayout, QScrollArea, QDialog, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import QTimer
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

cart = {} 
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
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Заголовок
        title = QLabel("Жанры")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #2A5266;")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # Виджет прокрутки
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        # Контейнер для жанров
        scroll_widget = QWidget()
        scroll_area.setWidget(scroll_widget)

        # Сетка жанров
        genres_layout = QGridLayout(scroll_widget)
        genres_layout.setHorizontalSpacing(30)
        genres_layout.setVerticalSpacing(20)

        # Получаем жанры с изображениями
        genres = self.get_genres_with_images()

        row, col = 0, 0
        for genre in genres:
            genre_name = genre['name']
            image_path = genre['image_path']

            if not image_path:
                continue  # Пропускаем жанры без изображения

            # Виджет жанра
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

            # Загружаем и растягиваем изображение
            genre_label_image = QLabel()
            genre_label_image.setFixedSize(300, 300)  # Фиксированный размер
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(300, 300, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
            genre_label_image.setPixmap(scaled_pixmap)
            genre_label_image.setScaledContents(True)  # Включаем масштабирование внутри QLabel
            genre_layout.addWidget(genre_label_image, alignment=Qt.AlignmentFlag.AlignCenter)

            # Название жанра
            genre_label_text = QLabel(genre_name)
            genre_label_text.setFont(QFont("Arial", 14))
            genre_label_text.setStyleSheet("color: #2A5266; font-weight: bold;")
            genre_label_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
            genre_layout.addWidget(genre_label_text)

            genres_layout.addWidget(genre_widget, row, col, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)

            # Перемещаемся по сетке
            col += 1
            if col >= 3:
                col = 0
                row += 1

    # Получение жанров с изображениями
    def get_genres_with_images(self):
        connection = create_connection()
        genres = []
        if connection:
            try:
                with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                    query = """
                        SELECT g.name, MIN(i.image_path) AS image_path
                        FROM Genres g
                        LEFT JOIN Product_Genres pg ON g.id_genre = pg.id_genre
                        LEFT JOIN Images i ON pg.id_product = i.id_product
                        WHERE i.image_path IS NOT NULL  -- Фильтруем только те, у которых есть изображения
                        GROUP BY g.id_genre, g.name;
                    """
                    cursor.execute(query)
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

class CatalogPage(QWidget):
    def __init__(self):
        super().__init__()

        # Основной layout
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        # Левая часть - товары с прокруткой
        left_layout = QVBoxLayout()
        left_layout.setSpacing(10)

        # Заголовок "Каталог"
        title = QLabel("Каталог")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #2A5266;")
        left_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # QScrollArea для товаров
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        left_layout.addWidget(self.scroll_area)

        # Контейнер для товаров
        self.scroll_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_widget)

        # Сетка товаров
        self.grid_layout = QGridLayout(self.scroll_widget)
        self.grid_layout.setHorizontalSpacing(30)
        self.grid_layout.setVerticalSpacing(30)

        # Загрузка товаров
        self.load_products()

        # Добавляем левую часть в основной layout
        self.main_layout.addLayout(left_layout)

        # Правая панель - Детали товара
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

        # Виджеты для деталей товара (по умолчанию скрыты)
        self.product_image = QLabel()
        self.product_image.setFixedSize(250, 250)
        self.product_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.product_info = QLabel()
        self.product_info.setWordWrap(True)
        self.product_info.setStyleSheet("font-size: 14px; color: #333;")

        self.details_layout.addWidget(self.product_image)
        self.details_layout.addWidget(self.product_info)

        self.details_panel.hide()  # По умолчанию скрываем
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
                            i.image_path,
                            p.quantity
                        FROM Products p
                        LEFT JOIN Product_Genres pg ON p.id_product = pg.id_product
                        LEFT JOIN Genres g ON pg.id_genre = g.id_genre
                        LEFT JOIN Images i ON p.id_product = i.id_product
                        GROUP BY p.id_product, p.name, p.price, p.age_category, p.difficulty, i.image_path, p.quantity
                    """)
                    
                    products = cursor.fetchall()
                    row, col = 0, 0
                    for product in products:
                        if product["quantity"] > 0:  # Показываем только товары в наличии
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
                border: 1px solid #2A5266; 
                border-radius: 10px; 
                padding: 10px; 
                text-align: center;
            } 
        """)
        card_layout = QVBoxLayout(card_widget)

        # Загружаем изображение товара
        image_label = QLabel()
        image_label.setFixedSize(300, 300)
        image_path = product['image_path'] if product['image_path'] else 'placeholder.jpg'
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            image_label.setText("Изображение не найдено")
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            image_label.setStyleSheet("color: red; font-size: 14px;")
        else:
            scaled_pixmap = pixmap.scaled(300, 300, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
            image_label.setPixmap(scaled_pixmap)
            image_label.setScaledContents(True)
        
        # Привязываем событие клика на изображение
        image_label.mousePressEvent = lambda event, p=product: self.show_product_details(p)

        card_layout.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Название товара
        product_label = QLabel(product["name"])
        product_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        product_label.setStyleSheet("color: #2A5266;")
        product_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(product_label)

        # Кнопка "Добавить"
        add_button = QPushButton("Добавить")
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
        add_button.clicked.connect(lambda: self.add_to_cart(product['id_product']))
        card_layout.addWidget(add_button)

        self.grid_layout.addWidget(card_widget, row, col, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)

    def show_product_details(self, product):
        """ Отображает информацию о товаре в правой панели """
        image_path = product['image_path'] if product['image_path'] else 'placeholder.jpg'
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            self.product_image.setText("Изображение не найдено")
            self.product_image.setStyleSheet("color: red; font-size: 14px;")
        else:
            scaled_pixmap = pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.product_image.setPixmap(scaled_pixmap)

        product_info_text = f"""
        <b>Название:</b> {product['name']}<br>
        <b>Жанры:</b> {product['genres']}<br>
        <b>Цена:</b> {product['price']} руб.<br>
        <b>Возраст:</b> {product['age_category']}<br>
        <b>Сложность:</b> {product['difficulty']}<br>
        <b>В наличии:</b> {product['quantity']} шт.
        """
        self.product_info.setText(product_info_text)

        self.details_panel.show()  # Показываем панель

    def add_to_cart(self, product_id):
        connection = create_connection()
        if not connection:
            return

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT quantity FROM Products WHERE id_product = %s", (product_id,))
                result = cursor.fetchone()

                if not result:
                    print(f"Товар с ID {product_id} не найден.")
                    return
                
                available_quantity = result['quantity']
                
                if product_id in cart:
                    if cart[product_id] < available_quantity:
                        cart[product_id] += 1
                    else:
                        print(f"Недостаточно товара {product_id} на складе!")
                else:
                    if available_quantity > 0:
                        cart[product_id] = 1
                    else:
                        print(f"Товар {product_id} закончился на складе.")

        finally:
            connection.close()

    def filter_products(self, search_text):
        """Фильтрует товары в каталоге по названию или жанру."""
        for i in range(self.grid_layout.count()):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                name_label = widget.findChild(QLabel)  # Название товара
                if name_label and search_text.lower() in name_label.text().lower():
                    widget.show()
                else:
                    widget.hide()

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
        self.scroll_layout = QVBoxLayout(scroll_content)  # Сохраняем `scroll_layout`
        self.scroll_layout.setContentsMargins(10, 10, 10, 10)
        self.scroll_layout.setSpacing(10)

        scroll_area.setWidget(scroll_content)

        self.sales_widgets = []  # Храним виджеты продаж для фильтрации
        self.load_sales()

    def load_sales(self):
        """Загружает список продаж из базы данных."""
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

                    # Информация о продаже
                    sale_info = QLabel(f"Дата продажи: {row['sale_date']} | Количество: {row['quantity']}")
                    sale_info.setStyleSheet("font-size: 14px; color: #333333;")
                    sale_layout.addWidget(sale_info)

                    # Кнопка "показать больше"
                    more_button = QPushButton("Показать больше")
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

                    self.scroll_layout.addWidget(sale_widget)
                    self.sales_widgets.append((sale_widget, sale_info))  # Сохраняем для поиска
            connection.close()

    def filter_sales(self, search_text):
        """Фильтрует список продаж по дате."""
        for widget, sale_info in self.sales_widgets:
            if search_text.lower() in sale_info.text().lower():
                widget.show()
            else:
                widget.hide()

    def show_more_info(self, sale_id):
        """Открывает окно с деталями продажи."""
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

        total_price = 0

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
                    total_price += row['quantity'] * row['price']
            connection.close()

        details_layout.addWidget(table)

        total_label = QLabel(f"Итого: {total_price:.2f} руб.")
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

cart = {}

class PaymentDialog(QDialog):
    def __init__(self, cart_items):
        super().__init__()
        self.setWindowTitle("Выбор способа оплаты")
        self.setFixedSize(300, 250)

        self.cart_items = cart_items  # Список товаров в корзине
        self.payment_method = None
        self.bonus_card_number = None

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        self.card_input = QLineEdit(self)
        self.card_input.setPlaceholderText("Введите номер бонусной карты (необязательно)")
        self.card_input.setStyleSheet("padding: 5px; font-size: 14px; border-radius: 5px;")
        layout.addWidget(QLabel("Бонусная карта:"))
        layout.addWidget(self.card_input)

        for method in ["cash", "card"]:
            button = QPushButton(method)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #3C7993;
                    color: white;
                    border-radius: 10px;
                    padding: 10px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #2A5266;
                }
            """)
            button.clicked.connect(lambda _, m=method: self.select_payment(m))
            layout.addWidget(button)

    def select_payment(self, method):
        self.payment_method = method    
        self.bonus_card_number = self.card_input.text().strip()
        self.process_payment()  # Записываем в БД
        self.accept()

    def process_payment(self):
        connection = create_connection()  # Используем твою функцию подключения
        if not connection:
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных.")
            return

        try:
            with connection.cursor() as cursor:
                # Получаем id клиента, если указана бонусная карта
                id_client = None
                if self.bonus_card_number:
                    cursor.execute(
                        """SELECT id_client FROM Clients 
                        WHERE id_card = (SELECT id_card FROM Bonus_Cards WHERE card_code = %s)""",
                        (self.bonus_card_number,)
                    )
                    result = cursor.fetchone()
                    if result:
                        id_client = result["id_client"]

                print("Отправляемый метод оплаты:", self.payment_method)
                print("DEBUG cart_items:", self.cart_items)     

                # Записываем продажу
                cursor.execute(
                    "INSERT INTO Sales (sale_date, id_client, payment_method) VALUES (NOW(), %s, %s)",
                    (id_client, self.payment_method)
                )
                sale_id = cursor.lastrowid  # Получаем ID новой продажи

                # Записываем детали продажи и обновляем склад
                for id_product, quantity in self.cart_items.items():
                    cursor.execute(
                        "INSERT INTO Sales_Details (id_sale, id_product, quantity) VALUES (%s, %s, %s)",
                        (sale_id, id_product, quantity)
                    )

                    cursor.execute(
                        "UPDATE Products SET quantity = quantity - %s WHERE id_product = %s",
                        (quantity, id_product)
                    )

                connection.commit()
                QMessageBox.information(self, "Успех", "Оплата успешно завершена!")

        except pymysql.MySQLError as err:
            QMessageBox.critical(self, "Ошибка", f"Ошибка базы данных: {err}")
        finally:
            connection.close()

class SalePage(QWidget):
    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_and_reload_cart)
        self.timer.start(1000)
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
        self.scroll_layout = QVBoxLayout(scroll_content)
        self.scroll_layout.setContentsMargins(10, 10, 10, 10)
        self.scroll_layout.setSpacing(10)

        scroll_area.setWidget(scroll_content)

        # Общая сумма
        self.total_label = QLabel("Итого: 0")
        self.total_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.total_label.setStyleSheet("color: #2A5266; margin-top: 20px;")
        layout.addWidget(self.total_label, alignment=Qt.AlignmentFlag.AlignRight)

        # Кнопка завершения покупки
        # Кнопка завершения покупки
        self.confirm_button = QPushButton("Завершить покупку")  # <-- теперь self.confirm_button
        self.confirm_button.setStyleSheet("""
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
        self.confirm_button.clicked.connect(self.complete_purchase)
        layout.addWidget(self.confirm_button, alignment=Qt.AlignmentFlag.AlignRight)

        # И сразу отключаем кнопку, если сумма 0
        self.confirm_button.setEnabled(False)


        # Настроим растягивание
        layout.setStretch(0, 0)  # Заголовок не растягивается
        layout.setStretch(1, 1)  # Прокручиваемая область будет растягиваться
        layout.setStretch(2, 0)  # Общая сумма не растягивается
        layout.setStretch(3, 0)  # Кнопка завершения покупки не растягивается

        # Загружаем товары из корзины
        self.load_cart_items()

    def create_connection(self):
        """
        Создаёт соединение с базой данных MySQL.
        """
        connection = None
        try:
            connection = pymysql.connect(
                host='127.0.0.1',
                user='root',
                password='1234',
                db='CRM',
                cursorclass=pymysql.cursors.DictCursor
            )
        except pymysql.MySQLError as e:
            print(f"Ошибка подключения к базе данных: {e}")
        return connection

    def load_cart_items(self):
        """
        Загружает данные о товарах из корзины и создаёт соответствующие виджеты.
        """
        connection = self.create_connection()
        if not connection:
            return

        try:
            with connection.cursor() as cursor:
                # Запрос для получения данных о товарах
                query = """
                    SELECT Products.id_product, Products.name AS product_name, Products.price, Images.image_path
                    FROM Products
                    LEFT JOIN Images ON Products.id_product = Images.id_product;
                """
                cursor.execute(query)
                items = cursor.fetchall()

                for item in items:
                    product_id = item['id_product']
                    quantity = cart.get(product_id, 0)  # Получаем количество товара из корзины
                    if quantity > 0:  # Добавляем только товары с количеством больше 0
                        self.add_item_to_layout(item, quantity)

        except pymysql.MySQLError as e:
            print(f"Ошибка выполнения запроса: {e}")
        finally:
            connection.close()


    def add_item_to_layout(self, item, quantity=0):
        """
        Создаёт виджет товара и добавляет его в макет.

        :param item: Словарь с данными о товаре (id, название, цена, путь к изображению).
        :param quantity: Количество товара в корзине (по умолчанию 0).
        """
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
        item_layout.setSpacing(10)

        # Изображение товара
        item_image = QLabel()
        item_image.setFixedSize(200, 200)
        image_path = item['image_path'] or 'default.jpg'
        item_image.setPixmap(QPixmap(image_path).scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
        item_layout.addWidget(item_image)

        # Название товара
        item_label = QLabel(item['product_name'])
        item_label.setStyleSheet("font-size: 14px; color: #333333;")
        item_layout.addWidget(item_label)

        # Цена товара
        price_label = QLabel(f"Цена: {item['price']} руб.")
        price_label.setObjectName(f"product_{item['id_product']}_price")  # Уникальный ID для цены
        price_label.setStyleSheet("font-size: 14px; color: #333333;")
        item_layout.addWidget(price_label)

        # Кнопки изменения количества
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
        decrease_button = QPushButton("-")
        decrease_button.setFixedSize(50, 50)
        decrease_button.setStyleSheet(button_style)
        decrease_button.clicked.connect(lambda _, item_id=item['id_product']: self.update_quantity(item_id, -1))
        item_layout.addWidget(decrease_button)

        # Метка для отображения количества
        quantity_label = QLabel(str(quantity))  # Используем переданное количество
        quantity_label.setObjectName(f"product_{item['id_product']}_quantity")  # Уникальный ID для количества
        quantity_label.setFixedSize(30, 50)
        quantity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        item_layout.addWidget(quantity_label)

        # Кнопка увеличения количества
        increase_button = QPushButton("+")
        increase_button.setFixedSize(50, 50)
        increase_button.setStyleSheet(button_style)
        increase_button.clicked.connect(lambda _, item_id=item['id_product']: self.update_quantity(item_id, 1))
        item_layout.addWidget(increase_button)

        # Добавляем виджет в прокручиваемый макет
        self.scroll_layout.addWidget(item_widget)


    def update_quantity(self, item_id, change):
        """
        Обновляет количество товара в корзине и в пользовательском интерфейсе,
        проверяя его наличие в базе данных.

        :param item_id: ID товара.
        :param change: Изменение количества (+1 или -1).
        """
        connection = self.create_connection()
        if not connection:
            return

        try:
            with connection.cursor() as cursor:
                # Запрашиваем текущее количество товара в БД
                query = "SELECT quantity FROM Products WHERE id_product = %s"
                cursor.execute(query, (item_id,))
                result = cursor.fetchone()

                if result:
                    available_quantity = result['quantity']
                    new_quantity = cart.get(item_id, 0) + change

                    # Проверяем, достаточно ли товара в БД
                    if new_quantity > available_quantity:
                        QMessageBox.warning(self, "Ошибка", "Недостаточно товара в наличии!")
                        return  # Не обновляем корзину, если товара недостаточно

                    # Обновляем корзину
                    if new_quantity > 0:
                        cart[item_id] = new_quantity
                    else:
                        cart.pop(item_id, None)  # Удаляем товар из корзины, если он обнулился

        except pymysql.MySQLError as e:
            print(f"Ошибка запроса к БД: {e}")

        finally:
            connection.close()

        # Обновляем интерфейс
        self.refresh_and_reload_cart()


    def refresh_cart(self):
        """
        Обновляет отображение корзины.
        """
        # Очищаем текущий макет
        while self.scroll_layout.count():
            widget = self.scroll_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()

    def update_total(self):
        """
        Пересчитывает общую стоимость корзины и включает/отключает кнопку "Завершить покупку".
        """
        total = 0
        for product_id, quantity in cart.items():
            if quantity > 0:
                for i in range(self.scroll_layout.count()):
                    widget = self.scroll_layout.itemAt(i).widget()
                    if widget:
                        price_label = widget.findChild(QLabel, f"product_{product_id}_price")
                        if price_label:
                            price = float(price_label.text().replace("Цена: ", "").replace(" руб.", ""))
                            total += price * quantity

        self.total_label.setText(f"Итого: {total:.2f} руб.")

        # Делаем кнопку "Завершить покупку" неактивной, если сумма 0
        self.confirm_button.setEnabled(total > 0)


    def refresh_and_reload_cart(self):
        """
        Очищает и перезагружает список товаров в корзине.
        """
        self.refresh_cart()
        self.load_cart_items()
        self.update_total()

    def complete_purchase(self):
        dialog = PaymentDialog(cart)
        if dialog.exec():  # Если выбор сделан
            selected_method = dialog.payment_method
            bonus_card = dialog.bonus_card_number if dialog.bonus_card_number else "Не использовалась"
            
            # Очистка корзины после покупки
            cart.clear()
            
            # Обновляем интерфейс
            self.refresh_and_reload_cart()

            QMessageBox.information(self, "Покупка завершена", f"Вы выбрали оплату: {selected_method}\nБонусная карта: {bonus_card}")

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
        self.search_box.textChanged.connect(self.search_items)
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
    def search_items(self, text):
        """Фильтрует элементы на активной странице по введённому запросу."""
        if isinstance(self.current_page, CatalogPage):
            self.current_page.filter_products(text)
        elif isinstance(self.current_page, SoldItemsPage):
            self.current_page.filter_sales(text)



if __name__ == "__main__":
    import sys
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()
    sys.exit(app.exec())

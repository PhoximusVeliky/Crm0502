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
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, QPoint

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

        for row in range(5):
            for col in range(3):
                genre_label = QLabel()
                genre_label.setStyleSheet("""
                    QLabel {
                        background-color: white;
                        border: 1px solid #2A5266;
                        border-radius: 10px;
                        padding: 10px;
                    }
                """)
                genre_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                genre_label.setFixedSize(300, 300)  # Размер для изображений 300x300

                # Устанавливаем изображение в QLabel
                pixmap = QPixmap("path_to_image.jpg")  # Замените на путь к изображению
                scaled_pixmap = pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                genre_label.setPixmap(scaled_pixmap)

                genres_layout.addWidget(genre_label, row, col, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)



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

        # Путь к изображениям
        images = ["00.jpg"] * 6  # Используйте свои изображения для реального приложения

        # Добавление карточек в сетку
        for row in range(2):  # Количество строк
            for col in range(3):  # Количество столбцов
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

                # Информация о товаре
                product_info = f"Название: Товар {row * 3 + col + 1}\nЖанр: Жанр {row * 3 + col + 1}\nЦена: {100 * (row * 3 + col + 1)} руб."
                image_path = images[row * 3 + col]

                # Изображение товара
                image_label = QLabel(self)
                pixmap = QPixmap(image_path)
                image_label.setPixmap(pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))
                image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

                # Добавляем обработчик события
                image_label.mousePressEvent = lambda event, p=image_path, i=product_info: self.show_product_details(p, i)

                card_layout.addWidget(image_label)

                # Кнопка "добавить"
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

                # Добавление карточки в сетку
                self.grid_layout.addWidget(card_widget, row, col)

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

    def show_product_details(self, image_path, product_info):
        # Удаляем старое содержимое панели
        for i in reversed(range(self.details_layout.count())):
            widget_item = self.details_layout.itemAt(i).widget()
            if widget_item:
                widget_item.deleteLater()

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
        self.details_layout.addWidget(image_label)

        # Добавляем информацию о товаре
        info_label = QLabel(product_info)
        info_label.setWordWrap(True)
        info_label.setStyleSheet("""
            font-size: 14px;
            color: #333333;
            margin-top: 10px;
        """)
        self.details_layout.addWidget(info_label)

        # Кнопка "Показать больше"
        show_more_button = QPushButton("Показать больше", self)
        show_more_button.setStyleSheet("""
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
        show_more_button.setFixedHeight(40)
        show_more_button.clicked.connect(self.show_more_details)
        self.details_layout.addWidget(show_more_button)

        # Делаем панель видимой
        self.details_panel.show()

    def show_more_details(self):
        # Скрываем каталог и панель с деталями товара
        self.scroll_area.hide()
        self.details_panel.hide()

        # Создаем новый виджет с подробной информацией
        self.more_details_widget = QWidget(self)
        more_details_layout = QVBoxLayout(self.more_details_widget)
        more_details_layout.setContentsMargins(20, 20, 20, 20)
        more_details_layout.setSpacing(10)

        # Пример подробной информации
        more_details_layout.addWidget(QLabel("Дополнительная информация о товаре"))

        # Кнопка для возврата
        back_button = QPushButton("Назад", self)
        back_button.clicked.connect(self.back_to_details)
        more_details_layout.addWidget(back_button)

        # Добавляем новый виджет в основной layout
        self.main_layout.addWidget(self.more_details_widget)

    def back_to_details(self):
        # Убираем подробную информацию и показываем каталог и панель с деталями товара
        self.more_details_widget.deleteLater()
        self.scroll_area.show()
        self.details_panel.show()






class SoldItemsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Заголовок страницы
        title = QLabel("Проданные товары")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title.setStyleSheet("color: #2A5266; margin-bottom: 20px;")
        layout.addWidget(title)

        # Прокручиваемая область для списка продаж
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background-color: white; border: none;")
        layout.addWidget(scroll_area)

        # Контейнер внутри прокручиваемой области
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(10, 10, 10, 10)
        scroll_layout.setSpacing(10)

        for i in range(10):
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

            sale_info = QLabel(f"Дата продажи: 2023-12-25  Количество: {i + 1}")
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
            more_button.clicked.connect(lambda _, i=i: self.show_more_info(i))
            sale_layout.addWidget(more_button, alignment=Qt.AlignmentFlag.AlignRight)

            scroll_layout.addWidget(sale_widget)

        scroll_area.setWidget(scroll_content)

    def show_more_info(self, index):
        details_window = QDialog()
        details_window.setWindowTitle("Подробности продажи")
        details_window.setStyleSheet("background-color: white;")

        details_layout = QVBoxLayout(details_window)

        title = QLabel(f"Детали продажи №{index + 1}")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #2A5266;")
        details_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        table = QTableWidget(3, 3)
        table.setHorizontalHeaderLabels(["Наименование", "Кол-во", "Цена за шт"])
        table.setItem(0, 0, QTableWidgetItem("Товар 1"))
        table.setItem(0, 1, QTableWidgetItem("2"))
        table.setItem(0, 2, QTableWidgetItem("500"))

        table.setItem(1, 0, QTableWidgetItem("Товар 2"))
        table.setItem(1, 1, QTableWidgetItem("1"))
        table.setItem(1, 2, QTableWidgetItem("300"))

        table.setItem(2, 0, QTableWidgetItem("Товар 3"))
        table.setItem(2, 1, QTableWidgetItem("4"))
        table.setItem(2, 2, QTableWidgetItem("200"))
        details_layout.addWidget(table)

        total_label = QLabel("Итого: 2300")
        total_label.setFont(QFont("Arial", 14))
        total_label.setStyleSheet("color: #2A5266;")
        details_layout.addWidget(total_label, alignment=Qt.AlignmentFlag.AlignRight)

        details_window.setLayout(details_layout)
        details_window.exec()

class ApplyCardPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Заголовок
        title = QLabel("Оформление карты")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title.setStyleSheet("color: #2A5266; margin-bottom: 20px;")
        layout.addWidget(title)

        # Поля ввода
        fields = ["ФИО клиента", "номер телефона", "e-mail", "номер карты"]
        for field in fields:
            label = QLabel(field)
            label.setFont(QFont("Arial", 14))
            label.setStyleSheet("color: #2A5266;")
            layout.addWidget(label)

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
            layout.addWidget(input_field)

        # Кнопка подтверждения
        confirm_button = QPushButton()
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
        confirm_button.setFixedSize(50, 50)
        layout.addWidget(confirm_button, alignment=Qt.AlignmentFlag.AlignRight)

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
        # Здесь можно добавить функциональность для обработки покупки

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

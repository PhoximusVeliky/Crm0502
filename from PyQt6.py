from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QWidget, QGridLayout, QScrollArea, QDialog, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

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
        title = QLabel("Жанры")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #2A5266; margin: 10px 0;")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignLeft)

        genres_layout = QGridLayout()
        genres_layout.setHorizontalSpacing(30)
        genres_layout.setVerticalSpacing(20)
        layout.addLayout(genres_layout)

        for row in range(2):
            for col in range(3):
                genre_label = QLabel("изображение для жанра")
                genre_label.setStyleSheet("""
                    QLabel {
                        background-color: white;
                        border: 1px solid #2A5266;
                        border-radius: 10px;
                        font-size: 12px;
                        padding: 10px;
                    }
                """)
                genre_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                genre_label.setFixedSize(200, 120)
                genres_layout.addWidget(genre_label, row, col, alignment=Qt.AlignmentFlag.AlignCenter)

class CatalogPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Заголовок страницы
        title = QLabel("Каталог товаров")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title.setStyleSheet("color: #2A5266; margin-bottom: 20px;")
        layout.addWidget(title)

        # Сетка товаров
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(30)
        grid_layout.setVerticalSpacing(30)
        layout.addLayout(grid_layout)

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

                # Изображение товара
                image_label = QLabel("изображение товара")
                image_label.setStyleSheet("""
                    QLabel {
                        background-color: #e6e6e6;
                        border-radius: 5px;
                        font-size: 14px;
                        color: #999999;
                        padding: 40px;
                    }
                """)
                image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
                grid_layout.addWidget(card_widget, row, col)

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
        label = QLabel("Начать продажу")
        label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

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
            self.content_area.itemAt(0).widget().setParent(None)

        if page_name == "sold_items":
            self.search_box.setPlaceholderText("поиск по продажам")
        else:
            self.search_box.setPlaceholderText("поиск")

        self.content_area.addWidget(self.pages[page_name])
        self.current_page = self.pages[page_name]

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()
    sys.exit(app.exec())

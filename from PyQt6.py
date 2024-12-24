from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QWidget, QGridLayout
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
    search_box.setPlaceholderText("поиск по жанру")
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

    return top_bar


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
        label = QLabel("Каталог товаров")
        label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)


class SoldItemsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Проданные товары")
        label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)


class ApplyCardPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Оформить карту")
        label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)


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
        top_bar = create_top_bar()
        main_layout.addWidget(top_bar)

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

        self.content_area.addWidget(self.pages[page_name])
        self.current_page = self.pages[page_name]


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()
    sys.exit(app.exec())

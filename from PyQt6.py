from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton,
    QLineEdit, QLabel, QWidget, QSizePolicy, QSpacerItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


def create_side_menu(button_callbacks):
    panel_widget = QWidget()
    panel_widget.setStyleSheet("background-color: #2A5266; border-radius: 0px;")
    panel_widget.setFixedWidth(600)  # размеры панели

    panel_layout = QVBoxLayout(panel_widget)
    panel_layout.setContentsMargins(10, 20, 10, 20)  # Внутренние отступы
    panel_layout.setSpacing(50)# Расстояние между кнопками

    # Добавляем растяжку сверху
    panel_layout.addStretch()

    buttons = ["главная", "каталог", "проданные товары", "оформить карту", "продажа"]
    for button_text, callback in zip(buttons, button_callbacks):
        button = QPushButton(button_text)

        # Уникальный стиль для кнопки "продажа"
        if button_text == "продажа":
            button.setStyleSheet("""
                QPushButton {
                    background-color: white;  /* цвет */
                    border: none;             /* рамка */
                    border-radius: 100px;     /* скругления */
                    padding: 20px;
                    font-size: 20px;          /* Размер текста */
                    font-family: "Inter";     /* Шрифт */                    
                }
                QPushButton:hover {       
                    background-color: #3C7993; 
                }
            """)
            button.setFixedSize(400, 200)  # Размеры для кнопки "продажа"
        else:
            # Базовый стиль для остальных кнопок
            button.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    border: none;
                    border-radius: 75px;
                    padding: 10px;
                    font-size: 20px;         /* Размер текста */
                    font-family: "Inter";    /* Шрифт */
                }
                QPushButton:hover {
                    /*border-radius: 50px;*/
                    background-color: #3C7993;
                }
            """)
            button.setFixedSize(300, 150)  # Размеры для остальных кнопок

        button.clicked.connect(callback)
        panel_layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

    # Добавляем растяжку снизу
    panel_layout.addStretch()

    return panel_widget

def create_top_bar():
    """
    Создает верхнюю полоску с фиксированным размещением элементов и возвращает ее как виджет.
    """
    # Создаем верхнюю полоску
    top_bar = QWidget()
    top_bar.setStyleSheet("background-color: #3C7993;")
    top_bar.setFixedHeight(50)  # Фиксированная высота верхней полоски

    # Логотип/текст "Игровая полка"
    logo = QLabel("Игровая полка", top_bar)
    logo.setFont(QFont("Inter", 20))
    logo.setStyleSheet("color: #FFFFFF;")
    logo.setGeometry(200, 10, 200, 30)  # Устанавливаем позицию (x, y) и размер (ширина, высота)

    # Поле для поиска
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
    search_box.setGeometry(600, 10, 800, 30)  # Устанавливаем позицию (x, y) и размер (ширина, высота)

    return top_bar




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Игровая полка")

        # Основной виджет и макет
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        main_widget.setStyleSheet("background-color: #e6e6e6;")  # Светлый фон

        main_layout.setContentsMargins(0, 0, 0, 0)  # Убраны внешние отступы
        main_layout.setSpacing(0)

        # Верхняя полоска
        top_bar = create_top_bar()
        main_layout.addWidget(top_bar)

        # Основное содержимое
        main_content = QHBoxLayout()
        main_content.setContentsMargins(0, 0, 0, 0)  # Убраны внешние отступы
        main_content.setSpacing(0)
        main_layout.addLayout(main_content)

        # Функции для кнопок бокового меню
        button_callbacks = [
            self.go_to_main,
            self.open_catalog,
            self.view_sold_items,
            self.apply_card,
            self.start_sale
        ]

        # Левая панель
        side_menu = create_side_menu(button_callbacks)
        main_content.addWidget(side_menu)

        # Правая часть (содержимое)
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(10, 10, 10, 10)  # Отступы для правой части
        main_content.addLayout(content_layout)

        # Заголовок "Жанры"
        title = QLabel("жанры")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #2A5266; margin: 10px 0;")
        content_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignLeft)

        # Сетка жанров
        genres_layout = QGridLayout()
        genres_layout.setHorizontalSpacing(30)
        genres_layout.setVerticalSpacing(20)
        content_layout.addLayout(genres_layout)

        # Добавление ячеек с жанрами
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

        # Растяжка внизу для выравнивания
        content_layout.addStretch()

    # Обработчики кнопок бокового меню
    def go_to_main(self):
        print("Перейти на главную страницу")

    def open_catalog(self):
        print("Открыть каталог")

    def view_sold_items(self):
        print("Просмотр проданных товаров")

    def apply_card(self):
        print("Оформить карту")

    def start_sale(self):
        print("Начать продажу")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()  # Полноэкранный режим
    sys.exit(app.exec())

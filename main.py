from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QLineEdit, QSpinBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class SaleDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Продажа")
        self.setStyleSheet("background-color: white;")
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout(self)

        # Заголовок
        title = QLabel("Оформление продажи")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #2A5266;")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        # Таблица для отображения добавленных товаров
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Название", "Количество", "Цена за шт"])
        self.table.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.table)

        # Область для ввода итоговой суммы и подтверждения
        controls_layout = QHBoxLayout()

        # Итоговая сумма
        total_label = QLabel("Итого: ")
        total_label.setFont(QFont("Arial", 14))
        total_label.setStyleSheet("color: #2A5266;")
        controls_layout.addWidget(total_label)

        self.total_field = QLineEdit()
        self.total_field.setReadOnly(True)
        self.total_field.setText("0")
        self.total_field.setStyleSheet("font-size: 14px; padding: 5px; border: 1px solid #d9d9d9; border-radius: 5px;")
        controls_layout.addWidget(self.total_field)

        # Кнопка подтверждения
        confirm_button = QPushButton("Подтвердить")
        confirm_button.setStyleSheet("""
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
        confirm_button.clicked.connect(self.confirm_sale)
        controls_layout.addWidget(confirm_button)

        layout.addLayout(controls_layout)

        # Добавление тестовых данных
        self.add_test_data()

    def add_test_data(self):
        # Пример добавления тестовых данных
        items = [
            ("Товар 1", 2, 500),
            ("Товар 2", 1, 300),
            ("Товар 3", 4, 200)
        ]

        for name, quantity, price in items:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(name))

            # Спинбокс для изменения количества
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
                price = int(price_item.text())
                quantity = quantity_widget.value()
                total += price * quantity

        self.total_field.setText(str(total))

    def confirm_sale(self):
        total = self.total_field.text()
        confirmation_dialog = QDialog(self)
        confirmation_dialog.setWindowTitle("Подтверждение продажи")
        confirmation_dialog.setStyleSheet("background-color: white;")
        confirmation_dialog.setMinimumSize(300, 150)

        dialog_layout = QVBoxLayout(confirmation_dialog)

        confirm_message = QLabel(f"Вы подтверждаете продажу на сумму {total}?")
        confirm_message.setFont(QFont("Arial", 12))
        confirm_message.setStyleSheet("color: #2A5266;")
        dialog_layout.addWidget(confirm_message, alignment=Qt.AlignmentFlag.AlignCenter)

        button_layout = QHBoxLayout()

        yes_button = QPushButton("Да")
        yes_button.setStyleSheet("""
            QPushButton {
                background-color: #3C7993;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #2A5266;
            }
        """)
        yes_button.clicked.connect(lambda: self.finalize_sale(confirmation_dialog))
        button_layout.addWidget(yes_button)

        no_button = QPushButton("Нет")
        no_button.setStyleSheet("""
            QPushButton {
                background-color: #B22222;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #8B0000;
            }
        """)
        no_button.clicked.connect(confirmation_dialog.reject)
        button_layout.addWidget(no_button)

        dialog_layout.addLayout(button_layout)
        confirmation_dialog.exec()

    def finalize_sale(self, confirmation_dialog):
        total = self.total_field.text()
        print(f"Продажа подтверждена. Общая сумма: {total}")
        confirmation_dialog.accept()
        self.accept()

# Тестовое использование окна продажи
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    dialog = SaleDialog()
    dialog.exec()

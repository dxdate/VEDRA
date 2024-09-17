import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QComboBox, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon, QPixmap, QColor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Создание QComboBox
        self.combo_box = QComboBox()

        # Создание QPixmap
        pixmap = QPixmap(32, 32)  # Задаём размер изображения
        pixmap.fill(QColor(Qt.blue))  # Заполняем изображение синим цветом

        # Преобразование QPixmap в QIcon
        icon = QIcon(pixmap)

        # Добавление элемента с текстом и иконкой
        self.combo_box.addItem(icon, "Синий")

        # Основной виджет
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.combo_box)
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

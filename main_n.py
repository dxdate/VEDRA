import configparser
import random
import sys
import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal as Signal, QThread, Qt
from PyQt5.QtGui import QIntValidator, QPixmap, QColor, QIcon, QBrush
from PyQt5.QtWidgets import QMainWindow, QWidget
from window_colors import Ui_colors
from window_main import Ui_MainWindow
from  window_liters import  Ui_liters_form

config = configparser.ConfigParser()
config.read("settings.ini")
colors = []
for i in range(1, len(config['colors']) + 1):
    colors.append(list(map(int, config['colors'][f'col{i}'].split(', '))))
aval_colors = colors
buckets_liters = []
for i in range(1, len(config['buckets']) + 1):
    buckets_liters.append([i - 1, int(config['buckets'][f'bucket{i}'])])

current_bucket_liters = buckets_liters.copy()

def quit_app():
    sys.exit(0)


def recolor_image(pixmap, target_color=(0, 0, 255), tolerance=255):
    pixmap = QPixmap("images/bucket.png")
    image = pixmap.toImage()
    width, height = image.width(), image.height()
    for x in range(width):
        for y in range(height):
            pixel_color = QColor(image.pixel(x, y))
            if (abs(pixel_color.red() - 255) < tolerance and
                    abs(pixel_color.green() - 255) < tolerance and
                    abs(pixel_color.blue() - 255) < tolerance):
                new_color = QColor(target_color[0], target_color[1], target_color[2])
                image.setPixel(x, y, new_color.rgb())
    return QPixmap.fromImage(image)


class Buckets:
    def __init__(self):
        self.speed = 0
        self.zero_speed_time = 300_000
        self.max_speed_time = 1
        self.buckets = []
        self.tick_time = 0

    def generate_buckets(self):
        self.buckets = []
        for i in range(10):
            self.buckets.append(buckets_liters[i])
        return self.buckets

    def calculate_tick_time(self):
        return int(self.zero_speed_time / (1 + (self.speed / 10) ** 4))

    def add_water_to_bucket(self, bucket_i):
        self.buckets[bucket_i][1] += 1
        return self.buckets

    def remove_water_from_bucket(self, bucket_i):
        self.buckets[bucket_i][1] -= 1
        return self.buckets

    def check_bucket_full(self, bucket_i):
        if self.buckets[bucket_i][1] >= 10:
            return False
        return True

    def check_bucket_empty(self, bucket_i):
        if self.buckets[bucket_i][1] == 0:
            return True
        return False


class Form_Colors(QWidget, Ui_colors):
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)
        self.main_window = main_window  # Ссылка на главное окно
        self.color_boxes = [self.color_box_1, self.color_box_2, self.color_box_3,
                            self.color_box_4, self.color_box_5, self.color_box_6,
                            self.color_box_7, self.color_box_8, self.color_box_9,
                            self.color_box_10]

        # Хранение предыдущего выбора цветов для каждого ведра
        self.previous_colors = self.main_window.cur_colors.copy()

        self.btn_ok.clicked.connect(self.apply_colors)  # Применить цвета и закрыть окно
        self.btn_otmena.clicked.connect(self.cancel_colors)  # Кнопка отмены
        self.btn_rand_cols.clicked.connect(self.assign_random_colors)  # Случайные цвета

        # Подключаем обработчики изменения каждого комбобокса
        for i, combo_box in enumerate(self.color_boxes):
            combo_box.currentIndexChanged.connect(lambda _, i=i: self.color_changed(i))

        self.update_color_boxes()  # Инициализация доступных цветов

    def create_color_icon(self, color):
        """Создаём иконку квадратика с указанным цветом"""
        pixmap = QPixmap(16, 16)
        pixmap.fill(QColor(color[0], color[1], color[2]))
        return QIcon(pixmap)

    def color_changed(self, index):
        """Обработчик изменения цвета в комбо боксе"""
        current_color = list(map(int, self.color_boxes[index].currentText().split()))  # Новый выбранный цвет
        self.previous_colors[index] = current_color  # Обновляем цвет в списке выбранных
        print(f"ComboBox {index}: Selected color {current_color}")  # Debug output
        self.update_color_boxes()  # Обновляем все комбобоксы

    def apply_colors(self):
        """Применяем новые цвета ведер и закрываем окно"""
        new_colors = []
        for i in range(len(self.color_boxes)):
            color_text = self.color_boxes[i].currentText().split()
            new_colors.append(list(map(int, color_text)))

        print(f"Applying colors: {new_colors}")  # Debug output

        # Устанавливаем новые цвета в главное окно
        self.main_window.cur_colors = new_colors
        self.main_window.paint_buckets()  # Перекрасить ведра

        # Закрываем окно после применения цветов
        self.main_window.show()
        self.close()

    def cancel_colors(self):
        """Отмена и возврат к предыдущим цветам"""
        print("Color selection canceled.")  # Debug output
        self.main_window.cur_colors = self.previous_colors.copy()
        self.main_window.paint_buckets()  # Вернуть предыдущие цвета ведер
        self.main_window.show()  # Показываем главное окно
        self.close()  # Закрываем текущее окно

    def update_color_boxes(self):
        """Обновляем комбо боксы, чтобы отображать только доступные цвета и показывать квадратики перед текстом"""
        used_colors = self.previous_colors[:]  # Используемые цвета

        for i, combo_box in enumerate(self.color_boxes):
            current_color = self.previous_colors[i]  # Текущий выбранный цвет в этом комбо боксе
            combo_box.blockSignals(True)  # Отключаем сигналы, чтобы избежать повторных срабатываний

            # Очищаем текущий комбобокс и добавляем текущий цвет ведра
            combo_box.clear()
            combo_box.addItem(self.create_color_icon(current_color),
                              f'{current_color[0]} {current_color[1]} {current_color[2]}')

            # Добавляем все цвета, кроме уже использованных другими комбо боксами и текущего цвета
            for color in colors:
                if color not in used_colors:
                    combo_box.addItem(self.create_color_icon(color), f'{color[0]} {color[1]} {color[2]}')

            combo_box.blockSignals(False)  # Включаем сигналы обратно

    def assign_random_colors(self):
        """Назначаем случайные цвета всем ведрам"""
        available_colors = colors[:]  # Список доступных цветов
        random.shuffle(available_colors)  # Перемешиваем цвета

        # Присваиваем случайные цвета
        for i in range(len(self.color_boxes)):
            color = available_colors[i]
            self.previous_colors[i] = color  # Обновляем выбранные цвета

        # Обновляем комбо боксы, чтобы учесть изменения
        self.update_color_boxes()
        print(f"Random colors assigned: {self.previous_colors}")  # Debug output
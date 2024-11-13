import configparser
import random
import sys
import time
import copy
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QGraphicsOpacityEffect
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal as Signal, QThread, Qt, QPropertyAnimation, QPoint, QEasingCurve, QTimer
from PyQt5.QtGui import QIntValidator, QPixmap, QColor, QIcon, QBrush
from PyQt5.QtWidgets import QMainWindow, QWidget
from window_colors import Ui_colors
from window_main import Ui_MainWindow
from window_liters import Ui_liters_form

colors_name = {
    (255, 0, 0): "Красный",
    (0, 255, 0): "Зеленый",
    (0, 0, 255): "Синий",
    (255, 255, 0): "Жёлтый",
    (255, 0, 255): "Фуксия",
    (0, 255, 255): "Бирюзовый",
    (128, 0, 0): "Тёмно-красный",
    (0, 128, 0): "Тёмно-зелёный",
    (0, 0, 128): "Тёмно-синий",
    (128, 128, 0): "Оливковый",
    (128, 0, 128): "Пурпурный",
    (0, 128, 128): "Сине-зелёный",
    (192, 192, 192): "Серебряный",
    (128, 128, 128): "Серый",
    (255, 165, 0): "Оранжевый",
    (0, 255, 127): "Весенне-зелёный"
}

colors = list(colors_name.keys())


# Функция для получения названия цвета по RGB-коду
def get_color_name(rgb):
    return colors_name.get(tuple(rgb), f"{rgb[0]} {rgb[1]} {rgb[2]}")


default_colors = [[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0], [255, 0, 255], [0, 255, 255], [128, 0, 0],
                  [0, 128, 0], [0, 0, 128],
                  [128, 128, 0], [128, 0, 128], [0, 128, 128], [192, 192, 192], [128, 128, 128], [255, 165, 0],
                  [0, 255, 127]]
colors = default_colors
default_buckets = []
for i in range(1, 11):
    default_buckets.append([i - 1, 1])


def quit_app():
    sys.exit(0)


import ast  # Импортируем модуль ast для безопасной оценки строк


def read_custom_settings():
    default_colors = []
    default_liters = []
    speed = 0
    bad_chance = 0
    filename, _ = QFileDialog.getOpenFileName(None, "Open File", ".", "Text Files (*.txt);;All Files (*)")
    if filename:
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
            colors_section = False
            buckets_section = False
            color_set = set()  # Множество для проверки уникальности цветов

            for line in lines:
                line = line.strip()  # Удаляем лишние пробелы и переносы строк

                # Проверяем на начало секции [colors]
                if line == '[colors]':
                    colors_section = True
                    buckets_section = False
                    continue
                # Проверяем на начало секции [buckets]
                elif line == '[buckets]':
                    colors_section = False
                    buckets_section = True
                    continue
                if '[speed]' in line:
                    speed_ = line.split(' ')[1]
                    if 0 <= int(speed_) <= 100:
                        speed = int(speed_)
                    else:
                        raise ValueError("Скорость должна быть в диапазоне от 0 до 100.")
                    continue
                if '[bad]' in line:
                    bad_chance_ = line.split(' ')[1]
                    if 0 <= int(bad_chance_) <= 100:
                        bad_chance = int(bad_chance_)
                        break
                    else:
                        raise ValueError("Шанс должен быть в диапазоне от 0 до 100.")
                # Если секция [colors] активна, собираем цвета
                if colors_section:
                    try:
                        color_values = ast.literal_eval(line)  # Преобразуем строку в список чисел
                        if len(color_values) != 3 or not all(
                                isinstance(x, int) and 0 <= x <= 255 for x in color_values):
                            raise ValueError(f"Неверный цвет: {color_values}")  # Проверка корректности цвета
                        if tuple(color_values) in color_set:
                            raise ValueError(f"Цвет {color_values} уже существует.")  # Проверка на уникальность
                        color_set.add(tuple(color_values))  # Добавляем цвет в множество для проверки уникальности
                        default_colors.append(color_values)
                    except (SyntaxError, ValueError) as e:
                        raise ValueError(f"Ошибка при обработке цвета: {line}. {str(e)}")

                # Если секция [buckets] активна, собираем литры
                elif buckets_section:
                    try:
                        bucket_values = ast.literal_eval(line)  # Преобразуем строку в список чисел
                        if len(bucket_values) != 2 or not all(isinstance(x, int) for x in bucket_values):
                            raise ValueError(f"Неверные значения ведер: {bucket_values}")  # Проверка корректности ведер
                        if bucket_values[1] > 10:
                            raise ValueError(
                                f"Общее количество литров в ведрах {bucket_values} не должно превышать 10!")  # Проверка на максимальную заполненность
                        default_liters.append(bucket_values)
                    except (SyntaxError, ValueError) as e:
                        raise ValueError(f"Ошибка при обработке ведер: {line}. {str(e)}")

            # print(default_colors, default_liters, speed, bad_chance)
            return default_colors, default_liters, speed, bad_chance


        except ValueError as e:
            QMessageBox.critical(None, "Ошибка", str(e))
        except Exception as e:
            QMessageBox.critical(None, "Ошибка",
                                 "Произошла ошибка при чтении файла:\n" + "Файл поврежден и не может быть прочитан")
            print(e)


def save_custom_settings(colors, buckets, speed, bad_chance):
    filename, _ = QFileDialog.getSaveFileName(None, "Save File", ".", "Text Files (*.txt);;All Files (*)")
    if filename:
        with open(filename, 'w') as f:
            colors_f = ''
            buckets_f = ''
            for i in colors:
                colors_f += str(i) + '\n'
            for i in buckets:
                buckets_f += str(i) + '\n'
            f.write(f'[colors]\n{colors_f}[buckets]\n{buckets_f}[speed] {speed}\n[bad] {int(bad_chance)}')


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


class Form_Colors(QWidget, Ui_colors):
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)
        self.main_window = main_window
        self.color_boxes = [self.color_box_1, self.color_box_2, self.color_box_3,
                            self.color_box_4, self.color_box_5, self.color_box_6,
                            self.color_box_7, self.color_box_8, self.color_box_9,
                            self.color_box_10]

        # Хранение предыдущего выбора цветов для каждого ведра
        self.previous_colors = self.main_window.cur_colors.copy()
        self.temporary_colors = self.previous_colors.copy()  # Временное хранилище для новых/случайных цветов

        self.btn_ok.clicked.connect(self.apply_colors)  # Применить цвета и закрыть окно
        self.btn_otmena.clicked.connect(self.cancel_colors)  # Кнопка отмены
        self.btn_rand_cols.clicked.connect(self.assign_random_colors)  # Случайные цвета

        # Подключаем обработчики изменения каждого комбобокса
        for i, combo_box in enumerate(self.color_boxes):
            combo_box.currentIndexChanged.connect(lambda _, i=i: self.color_changed(i))

        self.update_color_boxes()

    def create_color_icon(self, color):
        """Создаём иконку квадратика с указанным цветом"""
        pixmap = QPixmap(16, 16)
        pixmap.fill(QColor(color[0], color[1], color[2]))
        return QIcon(pixmap)

    def color_changed(self, index):
        """Обработчик изменения цвета в комбо боксе"""
        current_color = self.color_boxes[index].currentData()  # Получаем RGB-цвет как данные элемента
        if current_color:  # Проверяем, что данные не пустые
            self.temporary_colors[index] = current_color  # Обновляем временные цвета
        self.update_color_boxes()  # Обновляем все комбобоксы # Обновляем все комбобоксы

    def apply_colors(self):
        """Применяем временные цвета в качестве текущих и закрываем окно"""
        self.main_window.cur_colors = self.temporary_colors.copy()
        self.main_window.paint_buckets()
        self.main_window.show()
        self.close()

    def cancel_colors(self):
        """Отмена и возврат к предыдущим цветам"""
        self.temporary_colors = self.previous_colors.copy()  # Отменяем изменения, возвращая пред. выбор
        self.main_window.cur_colors = self.previous_colors.copy()
        self.main_window.paint_buckets()
        self.main_window.show()
        self.close()

    def update_color_boxes(self):
        """Обновляем комбо-боксы с учетом временных цветов и исключаем уже выбранные цвета"""
        selected_colors = {tuple(color) for color in self.temporary_colors}  # Множество уже выбранных цветов

        for i, combo_box in enumerate(self.color_boxes):
            combo_box.blockSignals(True)
            combo_box.clear()

            # Текущий цвет комбобокса - это временный цвет
            current_color = self.temporary_colors[i]
            color_name = colors_name.get(tuple(current_color), "Неизвестный цвет")

            # Добавляем текущий цвет первым элементом, чтобы оставить его в списке
            combo_box.addItem(self.create_color_icon(current_color), color_name)
            combo_box.setItemData(0, current_color)

            # Убираем текущий цвет из множества, чтобы он оставался в текущем комбобоксе
            available_colors = [color for color in colors if
                                tuple(color) not in selected_colors or color == current_color]

            # Добавляем остальные доступные цвета
            for color in available_colors:
                color_name = colors_name.get(tuple(color), "Неизвестный цвет")
                combo_box.addItem(self.create_color_icon(color), color_name)
                combo_box.setItemData(combo_box.count() - 1, color)

            combo_box.blockSignals(False)

    def assign_random_colors(self):
        """Назначаем случайные цвета всем ведрам, сохраняя их во временный список"""
        available_colors = colors[:]
        random.shuffle(available_colors)

        # Присваиваем случайные цвета временно, не изменяя previous_colors
        self.temporary_colors = available_colors[:len(self.color_boxes)]
        self.update_color_boxes()


class Form_liters(QWidget, Ui_liters_form):
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)

        self.main_window = main_window  # Ссылка на главное окно
        self.liter_boxes = [self.liters_bucket_1, self.liters_bucket_2, self.liters_bucket_3, self.liters_bucket_4,
                            self.liters_bucket_5, self.liters_bucket_6, self.liters_bucket_7, self.liters_bucket_8,
                            self.liters_bucket_9, self.liters_bucket_10]
        self.liters = []

        # Заполняем форму с настройками значениями из buckets_liters при первом запуске
        self.fill_liters_form()
        self.btn_rand_liters.clicked.connect(self.set_random_liters)
        self.btn_ok.clicked.connect(self.apply_liters)  # Применить новые литры и закрыть форму
        self.btn_otmena.clicked.connect(self.cancel)

    def set_random_liters(self):
        """Назначаем случайные значения литров для каждого ведра"""
        for i in range(len(self.liter_boxes)):
            random_liters = random.randint(0, 10)  # Генерируем случайное количество литров от 0 до 10
            self.liter_boxes[i].setValue(random_liters)

    def fill_liters_form(self):
        """Заполняет форму с литрами значениями из buckets_liters"""
        for i in range(len(default_buckets)):
            self.liter_boxes[i].setValue(default_buckets[i][1])  # Устанавливаем значения из начальных настроек

    def apply_liters(self):
        """Применить настройки литров для ведер"""
        # Обновляем текущие значения ведер на основе введенных данных
        for i in range(len(self.liter_boxes)):
            new_value = self.liter_boxes[i].value()
            default_buckets[i][1] = new_value  # Обновляем глобальные настройки ведер

        # Обновляем ведра в основном окне
        self.main_window.update_buckets_liters()  # Обновляем отображение ведер

        self.showmain()  # Показываем главное окно
        self.close()  # Закрываем окно с настройками

    def cancel(self):
        """Отмена изменений, возврат в главное окно"""
        # print("Liters adjustment canceled.")  # Debug output
        self.showmain()  # Показываем главное окно
        self.close()  # Закрываем текущее окно

    def showmain(self):
        # for i in range(len(default_buckets)):
        #     if int(default_buckets[i][1]) == 10:
        #         self.main_window.hide_bucket(i)
        self.main_window.show()


class Main_window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.flag_start = False
        self.flag_pause = False
        self.default_buckets = copy.deepcopy(default_buckets)
        self.speed = 0
        self.zero_speed_time = 100_000
        self.buckets = []
        self.tick_time = 0
        # self.rl = [self.rl_1, self.rl_2, self.rl_3, self.rl_4, self.rl_5, self.rl_6, self.rl_7, self.rl_8, self.rl_9, self.rl_10]
        # for i in range(len(self.rl)):
        #     self.rl[i].hide()
        self.shake_duration = 100

        # Инициализация уникальных цветов для ведер
        self.cur_colors = [colors[i] for i in range(10)]  # Здесь `colors` — это список возможных цветов.
        self.Form_liters = Form_liters(self)
        self.Form_colors = Form_Colors(self)  # Теперь можно безопасно инициализировать Form_Colors

        self.thread = QThread()
        self.worker = Worker()
        self.flag_end = False
        self.bad_num_chance = 10  # шанс на генерацию аварийной лампы
        self.label_bad_chance.setValidator(QIntValidator(0, 100, self))
        self.current_speed = self.slider_speed.value()
        self.label_speed.setValidator(QIntValidator(0, 100, self))
        self.label_speed.setText(str(self.current_speed))
        self.color_boxes = self.Form_colors.color_boxes
        self.flag_shadow_pause = False
        self.Form_colors.btn_ok.clicked.connect(self.fc_ok)

        self.slider_speed.valueChanged.connect(self.change_speed)
        self.label_speed.textChanged.connect(self.label_speed_check)
        self.label_bad_chance.textChanged.connect(self.label_bad_chance_check)
        self.action_colors.triggered.connect(self.open_colors)
        self.action_liters.triggered.connect(self.open_liters)
        self.action_quit.triggered.connect(quit_app)
        self.action_save.triggered.connect(self.save_settings)
        self.action_open.triggered.connect(self.open_settings)
        self.slider_bad_chance.valueChanged.connect(self.change_chance)

        self.button_exit.clicked.connect(quit_app)
        self.button_start.clicked.connect(self.start)
        self.button_pause.clicked.connect(self.pause)
        self.worker.generated_number.connect(self.test)
        self.init_app()
        self.speed = self.current_speed
        self.tick_time = self.calculate_tick_time()
        self.change_speed()
        self.change_chance()

    def save_settings(self):
        # print(self.default_buckets, default_buckets)
        save_custom_settings(self.cur_colors, default_buckets, self.speed, self.bad_num_chance)

    def change_chance(self):
        self.bad_num_chance = self.slider_bad_chance.value()
        # print(self.bad_num_chance)
        self.label.setText(f"Шанс на аварийную лампочку")
        self.label_bad_chance.setText(str(self.bad_num_chance))

    def open_settings(self):
        """Открывает файл с настройками и загружает данные."""
        colors, liters, speed, bad_chance = read_custom_settings()
        # print(colors and liters and speed and bad_chance)
        if colors and liters and speed + 1 and bad_chance + 1:
            self.cur_colors = colors
            self.speed = speed
            self.bad_num_chance = bad_chance  # Присваиваем цветам из файла
            default_buckets.clear()  # Очищаем старые значения ведер
            default_buckets.extend(liters)  # Записываем новые значения ведер
            self.update_buckets_liters()
            self.slider_speed.setValue(self.speed)
            self.label_bad_chance.setText(str(bad_chance))  # Обновляем ведра в основном окне

    def update_buckets_liters(self):
        """Обновить отображение ведер на основе их текущих значений"""

        self.buckets = copy.deepcopy(default_buckets)  # Копируем обновленные данные из глобальных настроек
        self.fill_buckets_text()  # Обновляем текстовое отображение
        self.paint_buckets()

    def generate_buckets(self):
        self.buckets = copy.deepcopy(default_buckets)
        return self.buckets

    def calculate_tick_time(self):
        print(int(self.zero_speed_time / (1 + (self.speed / 10) ** 2.7)))
        return int(self.zero_speed_time / (1 + (self.speed / 10) ** 2.7))

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
            del self.not_full_b[bucket_i]
            return True
        return False

    def open_liters(self):
        if self.flag_start: self.start()
        self.Form_liters.show()
        self.Form_liters.fill_liters_form()
        self.hide()

    def fc_ok(self):
        # При нажатии на ОК в окне выбора цветов
        self.Form_colors.apply_colors()

    def init_app(self):
        self.not_full_b = []
        # В этом месте `cur_colors` уже инициализирован и готов к использованию
        self.rl = [self.rl_1, self.rl_2, self.rl_3, self.rl_4, self.rl_5, self.rl_6, self.rl_7, self.rl_8, self.rl_9,
                   self.rl_10]
        for i in range(len(self.rl)):
            self.rl[i].hide()
        self.buckets = self.generate_buckets()
        self.buckets_l = [self.bucket_1, self.bucket_2, self.bucket_3,
                          self.bucket_4, self.bucket_5, self.bucket_6, self.bucket_7,
                          self.bucket_8, self.bucket_9, self.bucket_10]

        self.label_buckets_l = [self.label_bucket_1, self.label_bucket_2, self.label_bucket_3,
                                self.label_bucket_4, self.label_bucket_5, self.label_bucket_6, self.label_bucket_7,
                                self.label_bucket_8, self.label_bucket_9, self.label_bucket_10]
        for i in range(len(self.buckets_l)):
            self.buckets_l[i].show()
            self.label_buckets_l[i].show()
        self.paint_buckets()
        self.fill_buckets_text()

    def open_colors(self):
        if self.flag_start: self.start()
        self.Form_colors.update_color_boxes()  # Обновляем комбо боксы перед открытием окна
        self.Form_colors.show()
        self.hide()

    def fill_buckets_text(self):
        for k in range(len(self.buckets)):
            self.label_buckets_l[k].setText(f"  Ведро: {self.buckets[k][0]}\n  Литры: {self.buckets[k][1]}")

    def paint_buckets(self):
        # print(f"Painting buckets with colors: {self.cur_colors}")  # Debug output
        for k in range(len(self.buckets_l)):
            # print(f"Bucket {k}: Color {self.cur_colors[k]}")  # Debug output
            self.buckets_l[k].setPixmap(recolor_image(self.buckets_l[k].pixmap(), target_color=self.cur_colors[k]))

    def shake_bucket(self, index, al=False):
        bucket = self.buckets_l[index]  # Получаем ведро по индексу

        # Создаем эффект прозрачности
        opacity_effect = QGraphicsOpacityEffect(bucket)
        bucket.setGraphicsEffect(opacity_effect)

        # Устанавливаем начальную прозрачность (100%)
        opacity_effect.setOpacity(1.0)

        # Изменяем прозрачность до 40%
        if not al:
            opacity_effect.setOpacity(0.4)
        if al:
            self.rl[index].show()
            QTimer.singleShot(int(self.shake_duration / 2.3), lambda: self.rl[index].hide())
            # self.rl[index].hide()

            # self.rl[index].hide()

        # Создаем таймер для возврата прозрачности через некоторое время
        QTimer.singleShot(int(self.shake_duration / 2), lambda: opacity_effect.setOpacity(1.0))  # Запуск анимации

    def hide_bucket(self, bucket_i):
        if bucket_i < len(self.buckets_l):
            # Скрываем виджет и метку
            self.buckets_l[bucket_i].hide()
            self.label_buckets_l[bucket_i].hide()

            # Удаляем виджет и метку из их списков
            del self.rl[bucket_i]
            del self.buckets_l[bucket_i]
            del self.label_buckets_l[bucket_i]

            # Удаляем данные ведра
            del self.buckets[bucket_i]
            for i in range(len(self.buckets)):
                self.buckets[i][0] = int(i)
            print('del')
            # Ensure colors list stays in sync
            # print(f"Bucket {bucket_i} removed. Remaining buckets: {len(self.buckets_l)}")  # Debug output

    def test(self, num, bad_num):
        if self.buckets:  # Проверяем, что ведра не пустые
            if self.flag_start:
                if random.randint(0, 100) <= self.bad_num_chance:
                    for i in self.buckets:
                        if i[0] != 0:
                            self.not_full_b.append(i)
                    # генерация АЛ
                    # print(((bad_num % len(self.buckets) == num % len(self.buckets)) or self.check_bucket_empty(bad_num % len(self.buckets))) and len(self.buckets) > 1)
                    if ((bad_num % len(self.buckets) == num % len(self.buckets)) or self.check_bucket_empty(
                            bad_num % len(self.buckets))) and len(self.buckets) > 1 and self.not_full_b:
                        if len(self.buckets) > 2:
                            cnt = 0
                            breakout = False
                            while (bad_num % len(self.buckets) == num % len(self.buckets)) or self.check_bucket_empty(
                                bad_num % len(self.buckets)):
                                cnt += 1
                                if cnt >= 100000:
                                    self.label_bad_num.setText('Ал не сработала')
                                    breakout = True
                                    break
                            if breakout:
                                bad_num = round(random.randint(0, 9))
                                # self.label_bad_num.setText(f'АЛ: {bad_num % len(self.buckets)}')
                                self.add_water_to_bucket(num % len(self.buckets))
                                self.label_generated_number.setText(f'Добавляем литр в ведро: {num % len(self.buckets)}')
                                # self.remove_water_from_bucket(bad_num % len(self.buckets))
                                self.shake_bucket(num % len(self.buckets))
                                # self.shake_bucket(bad_num % len(self.buckets), True)
                            else:
                                bad_num = round(random.randint(0, 9))
                                self.label_bad_num.setText(f'АЛ: {bad_num % len(self.buckets)}')
                                self.add_water_to_bucket(num % len(self.buckets))
                                self.label_generated_number.setText(
                                    f'Добавляем литр в ведро: {num % len(self.buckets)}')
                                self.remove_water_from_bucket(bad_num % len(self.buckets))
                                self.shake_bucket(num % len(self.buckets))
                                self.shake_bucket(bad_num % len(self.buckets), True)
                        else:
                            self.label_bad_num.setText(f'АЛ не сработала')
                            self.add_water_to_bucket(num % len(self.buckets))
                            self.label_generated_number.setText(f'Добавляем литр в ведро: {num % len(self.buckets)}')
                            # self.remove_water_from_bucket(bad_num % len(self.buckets))
                            self.shake_bucket(num % len(self.buckets))
                            # self.shake_bucket(bad_num % len(self.buckets), True)

                    elif len(self.buckets) == 1:
                        self.label_bad_num.setText(f"АЛ не сработает, осталось одно ведро")
                        self.add_water_to_bucket(num % len(self.buckets))
                        self.shake_bucket(num % len(self.buckets))
                        self.label_generated_number.setText(f'Добавляем литр в ведро: {num % len(self.buckets)}')
                    else:
                        self.label_bad_num.setText(f'АЛ: {bad_num % len(self.buckets)}')
                        self.add_water_to_bucket(num % len(self.buckets))
                        self.remove_water_from_bucket(bad_num % len(self.buckets))
                        self.shake_bucket(num % len(self.buckets))
                        self.shake_bucket(bad_num % len(self.buckets), True)
                        self.label_generated_number.setText(f'Добавляем литр в ведро: {num % len(self.buckets)}')
                else:
                    self.label_bad_num.setText("Все работает без ошибок :)")
                    self.label_generated_number.setText(f'Добавляем литр в ведро: {num % len(self.buckets)}')
                    self.add_water_to_bucket(num % len(self.buckets))
                    self.shake_bucket(num % len(self.buckets))
                if not self.check_bucket_full(num % len(self.buckets)):
                    self.hide_bucket(num % len(self.buckets))
                self.fill_buckets_text()

        elif not self.flag_end:
            self.flag_end = True
            self.label_generated_number.setText("Ведра заполнены! Нажмите 'СТОП' для перезапуска!")
            self.label_bad_num.setText("")

    def check_all_full_buckets(self):
        for i in reversed(range(len(default_buckets))):
            if int(default_buckets[i][1]) == 10:
                self.hide_bucket(i)

    def start(self):
        if self.flag_start:
            self.stop()
        else:
            self.check_all_full_buckets()
            if not self.flag_pause:
                self.action_save.setEnabled(False)
                self.action_open.setEnabled(False)
                self.action_liters.setEnabled(False)
                self.action_colors.setEnabled(False)
                self.flag_start = True
                self.button_start.setText('Стоп')
                # self.button_pause.setEnabled(True)
                self.worker.stop_signal(True)
                self.worker.update_params(self.tick_time)
                self.worker.start()
            else:
                self.action_save.setEnabled(False)
                self.action_open.setEnabled(False)
                self.action_liters.setEnabled(False)
                self.action_colors.setEnabled(False)
                self.flag_start = True
                self.button_start.setText('Стоп')
                # self.button_pause.setEnabled(True)
                # self.worker.stop_signal(True)
                self.worker.update_params(self.tick_time)
                # self.worker.start()

    def stop(self):
        self.worker.stop_signal(False)
        self.flag_start = False
        self.flag_pause = False
        self.flag_end = False
        self.label_generated_number.setText('')
        self.label_bad_num.setText('')
        self.button_start.setText('Старт')
        self.button_pause.setText('Пауза')
        self.init_app()
        self.action_save.setEnabled(True)
        self.action_open.setEnabled(True)
        self.action_liters.setEnabled(True)
        self.action_colors.setEnabled(True)
        # self.button_pause.setEnabled(False)

    def pause(self):
        if self.flag_pause:
            self.flag_pause = False
            self.worker.stop_signal(True)
            self.button_pause.setText('Пауза')
            self.worker.start()
        else:
            # self.check_all_full_buckets()
            self.flag_pause = True
            self.worker.stop_signal(False)
            self.button_pause.setText('Продолжить')

    def change_speed(self):
        self.current_speed = self.slider_speed.value()
        self.label_speed.setText(str(self.current_speed))
        self.speed = self.current_speed
        self.tick_time = self.calculate_tick_time()
        self.shake_duration = int(self.tick_time / 3)
        # self.label_tick_time.setText(str(self.tick_time))
        self.worker.update_params(self.tick_time)

    def label_speed_check(self):
        try:
            if '+' in self.label_speed.text():
                self.label_speed.setText(self.label_speed.text().replace('+', ''))
            if len(self.label_speed.text()) == 0:
                self.label_speed.setText('0')
            if int(self.label_speed.text()) > 100:
                self.label_speed.setText('100')
            if len(self.label_speed.text()) > 1 and self.label_speed.text()[0] == '0':
                self.label_speed.setText(self.label_speed.text()[1:])
            if int(self.label_speed.text()) < 0:
                self.label_speed.setText('0')
            self.slider_speed.setValue(int(self.label_speed.text()))
        except Exception as ex:
            print(ex)

    def label_bad_chance_check(self):
        try:
            if '+' in self.label_bad_chance.text():
                self.label_bad_chance.setText(self.label_bad_chance.text().replace('+', ''))
            if len(self.label_bad_chance.text()) == 0:
                self.label_bad_chance.setText('0')
            if int(self.label_bad_chance.text()) > 100:
                self.label_bad_chance.setText('100')
            if len(self.label_bad_chance.text()) > 1 and self.label_bad_chance.text()[0] == '0':
                self.label_bad_chance.setText(self.label_bad_chance.text()[1:])
            if int(self.label_bad_chance.text()) < 0:
                self.label_bad_chance.setText('0')
            self.slider_bad_chance.setValue(int(self.label_bad_chance.text()))
        except Exception as ex:
            print(ex)


class Worker(QThread):
    generated_number = Signal(int, int)
    update_value_signal = Signal(int)

    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
        self.tick_time = 1000  # По умолчанию 1 секунда
        self.running = True
        self.updated_tick_time = False  # Флаг для мгновенного изменения

    def stop_signal(self, signal):
        self.running = signal

    def update_params(self, tick_time):
        self.tick_time = tick_time
        self.updated_tick_time = True  # Сигнализируем об изменении времени тика

    def run(self):
        self.generated_number.emit(round(random.randint(0, 9)), round(random.randint(0, 9)))
        while self.running:
            # print(self.running)
            start_time = time.time()  # Засекаем текущее время
            while time.time() - start_time < self.tick_time / 1000.0:
                if self.updated_tick_time:
                    # Если tick_time обновился, пересчитаем начальное время
                    elapsed = time.time() - start_time
                    start_time = time.time() - elapsed
                    self.updated_tick_time = False
                # time.sleep(0.01)  # Короткий сон для снижения нагрузки на CPU

            # Генерация "тика" после времени ожидания
            self.generated_number.emit(round(random.randint(0, 9)),
                                       round(random.randint(0, 9)))  # Пример, можете заменить на свою логику
            # print(f"Tick with tick_time: {self.tick_time}")

    def stop(self):
        self.running = False


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Main_window()
    window.show()
    app.exec_()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    main()

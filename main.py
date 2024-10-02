import configparser
import random
import sys
import time
import copy
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QGraphicsOpacityEffect
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal as Signal, QThread, Qt, QPropertyAnimation, QPoint, QEasingCurve
from PyQt5.QtGui import QIntValidator, QPixmap, QColor, QIcon, QBrush
from PyQt5.QtWidgets import QMainWindow, QWidget
from window_colors import Ui_colors
from window_main import Ui_MainWindow
from window_liters import Ui_liters_form

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
                        if bucket_values[1] > 9:
                            raise ValueError(
                                f"Общее количество литров в ведрах {bucket_values} не должно превышать 9!")  # Проверка на максимальную заполненность
                        default_liters.append(bucket_values)
                    except (SyntaxError, ValueError) as e:
                        raise ValueError(f"Ошибка при обработке ведер: {line}. {str(e)}")

            print(default_colors, default_liters, speed, bad_chance)
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
            f.write(f'[colors]\n{colors_f}[buckets]\n{buckets_f}[speed] {speed}\n[bad] {int(bad_chance * 100)}')


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


class Form_liters(QWidget, Ui_liters_form):
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)

        self.main_window = main_window  # Ссылка на главное окно
        self.change_chance()
        self.liter_boxes = [self.liters_bucket_1, self.liters_bucket_2, self.liters_bucket_3, self.liters_bucket_4,
                            self.liters_bucket_5, self.liters_bucket_6, self.liters_bucket_7, self.liters_bucket_8,
                            self.liters_bucket_9, self.liters_bucket_10]
        self.liters = []

        # Заполняем форму с настройками значениями из buckets_liters при первом запуске
        self.fill_liters_form()
        self.btn_rand_liters.clicked.connect(self.set_random_liters)
        self.btn_ok.clicked.connect(self.apply_liters)  # Применить новые литры и закрыть форму
        self.btn_otmena.clicked.connect(self.cancel)
        self.horizontalSlider.valueChanged.connect(self.change_chance)

    def set_random_liters(self):
        """Назначаем случайные значения литров для каждого ведра"""
        for i in range(len(self.liter_boxes)):
            random_liters = random.randint(0, 10)  # Генерируем случайное количество литров от 0 до 10
            self.liter_boxes[i].setValue(random_liters)

    def change_chance(self):
        self.main_window.bad_num_chance = self.horizontalSlider.value() / 100
        self.label.setText(f"Шанс на аварийную лампочку: {self.main_window.bad_num_chance}")

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

        self.main_window.show()  # Показываем главное окно
        self.close()  # Закрываем окно с настройками

    def cancel(self):
        """Отмена изменений, возврат в главное окно"""
        print("Liters adjustment canceled.")  # Debug output
        self.main_window.show()  # Показываем главное окно
        self.close()  # Закрываем текущее окно


class Main_window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.flag_start = False
        self.flag_pause = False
        self.default_buckets = copy.deepcopy(default_buckets)
        self.speed = 0
        self.zero_speed_time = 300_000
        self.max_speed_time = 1
        self.buckets = []
        self.tick_time = 0

        self.shake_duration = 200

        # Инициализация уникальных цветов для ведер
        self.cur_colors = [colors[i] for i in range(10)]  # Здесь `colors` — это список возможных цветов.
        self.Form_liters = Form_liters(self)
        self.Form_colors = Form_Colors(self)  # Теперь можно безопасно инициализировать Form_Colors

        self.thread = QThread()
        self.worker = Worker()
        self.flag_end = False
        self.bad_num_chance = 0.1  # шанс на генерацию аварийной лампы

        self.current_speed = self.slider_speed.value()
        self.label_speed.setValidator(QIntValidator(0, 100, self))
        self.label_speed.setText(str(self.current_speed))
        self.color_boxes = self.Form_colors.color_boxes

        self.Form_colors.btn_ok.clicked.connect(self.fc_ok)

        self.slider_speed.valueChanged.connect(self.change_speed)
        self.label_speed.textChanged.connect(self.label_speed_check)
        self.action_colors.triggered.connect(self.open_colors)
        self.action_liters.triggered.connect(self.open_liters)
        self.action_quit.triggered.connect(quit_app)
        self.action_save.triggered.connect(self.save_settings)
        self.action_open.triggered.connect(self.open_settings)

        self.button_exit.clicked.connect(quit_app)
        self.button_start.clicked.connect(self.start)
        self.button_pause.clicked.connect(self.pause)
        self.worker.generated_number.connect(self.test)
        self.init_app()
        self.speed = self.current_speed
        self.tick_time = self.calculate_tick_time()
        self.change_speed()

    def save_settings(self):
        save_custom_settings(self.cur_colors, self.default_buckets, self.speed, self.bad_num_chance)

    def open_settings(self):
        """Открывает файл с настройками и загружает данные."""
        colors, liters, speed, bad_chance = read_custom_settings()
        if colors and liters and speed and bad_chance:
            self.cur_colors = colors
            self.speed = speed
            self.bad_num_chance = bad_chance / 100  # Присваиваем цветам из файла
            default_buckets.clear()  # Очищаем старые значения ведер
            default_buckets.extend(liters)  # Записываем новые значения ведер
            self.update_buckets_liters()
            self.slider_speed.setValue(self.speed)
            self.Form_liters.horizontalSlider.setValue(bad_chance)  # Обновляем ведра в основном окне

    def update_buckets_liters(self):
        """Обновить отображение ведер на основе их текущих значений"""

        self.buckets = copy.deepcopy(default_buckets)  # Копируем обновленные данные из глобальных настроек
        self.fill_buckets_text()  # Обновляем текстовое отображение
        self.paint_buckets()

    def generate_buckets(self):
        self.buckets = copy.deepcopy(default_buckets)
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

    def open_liters(self):
        if self.flag_start: self.start()
        self.Form_liters.show()
        self.hide()

    def fc_ok(self):
        # При нажатии на ОК в окне выбора цветов
        self.Form_colors.apply_colors()

    def init_app(self):
        # В этом месте `cur_colors` уже инициализирован и готов к использованию
        self.buckets = self.generate_buckets()
        print(self.buckets)
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
            self.label_buckets_l[k].setText(f"  Bucket: {self.buckets[k][0]}\n  Liters: {self.buckets[k][1]}")

    def paint_buckets(self):
        print(f"Painting buckets with colors: {self.cur_colors}")  # Debug output
        for k in range(len(self.buckets_l)):
            print(f"Bucket {k}: Color {self.cur_colors[k]}")  # Debug output
            self.buckets_l[k].setPixmap(recolor_image(self.buckets_l[k].pixmap(), target_color=self.cur_colors[k]))

    def shake_bucket(self, index):
        bucket = self.buckets_l[index]  # Получаем ведро по индексу

        # Создаем эффект прозрачности
        opacity_effect = QGraphicsOpacityEffect(bucket)
        bucket.setGraphicsEffect(opacity_effect)

        # Создаем анимацию изменения прозрачности
        self.opacity_animation = QPropertyAnimation(opacity_effect, b"opacity")
        self.opacity_animation.setDuration(self.shake_duration)  # Длительность анимации
        self.opacity_animation.setStartValue(1.0)  # Начальная прозрачность (100%)
        self.opacity_animation.setKeyValueAt(0.5, 0.4)  # Прозрачность до 40% на середине анимации
        self.opacity_animation.setEndValue(1.0)  # Возвращаем прозрачность обратно до 100%

        self.opacity_animation.start()

    def hide_bucket(self, bucket_i):
        if bucket_i < len(self.buckets_l):
            # Скрываем виджет и метку
            self.buckets_l[bucket_i].hide()
            self.label_buckets_l[bucket_i].hide()

            # Удаляем виджет и метку из их списков
            del self.buckets_l[bucket_i]
            del self.label_buckets_l[bucket_i]

            # Удаляем данные ведра
            del self.buckets[bucket_i]
            # Ensure colors list stays in sync
            print(f"Bucket {bucket_i} removed. Remaining buckets: {len(self.buckets_l)}")  # Debug output

    def test(self, num, bad_num):
        if self.buckets:  # Проверяем, что ведра не пустые
            if self.flag_start:
                if random.random() <= self.bad_num_chance:
                    if bad_num % len(self.buckets) == num % len(self.buckets):
                        self.label_bad_num.setText("Аварийная лампа! Ведра совпадают, заливаем литр!")
                        self.add_water_to_bucket(num % len(self.buckets))
                    elif self.check_bucket_empty(bad_num % len(self.buckets)):
                        self.label_bad_num.setText("Аварийная лампа! Ведро пустое, пропускаем!")
                        self.label_generated_number.setText(
                            f"Gen: {str(num)}  Добавили в ведро: {str(num % len(self.buckets))}")
                        self.add_water_to_bucket(num % len(self.buckets))
                    else:
                        self.label_bad_num.setText(
                            f"Аварийная лампа! Из ведра {str(bad_num % len(self.buckets))} выбежал литр(")
                        self.remove_water_from_bucket(bad_num % len(self.buckets))
                        self.label_generated_number.setText(
                            f"Gen: {str(num)} Av: {str(bad_num)}  Добавили в ведро: {str(num % len(self.buckets))}")
                        self.add_water_to_bucket(num % len(self.buckets))
                    self.shake_bucket(num % len(self.buckets))
                else:
                    self.label_bad_num.setText("Все работает без ошибок :)")
                    self.label_generated_number.setText(
                        f"Gen: {str(num)}  Добавили в ведро: {str(num % len(self.buckets))}")
                    self.add_water_to_bucket(num % len(self.buckets))
                    self.shake_bucket(num % len(self.buckets))

                if not self.check_bucket_full(num % len(self.buckets)):
                    self.hide_bucket(num % len(self.buckets))

                self.fill_buckets_text()

        elif not self.flag_end:
            self.flag_end = True
            self.label_generated_number.setText("Ведра заполнены! Нажмите 'СТОП' для перезапуска!")
            self.label_bad_num.setText("")

    def start(self):
        if self.flag_start:
            self.stop()
        else:
            self.action_save.setEnabled(False)
            self.action_open.setEnabled(False)
            self.action_liters.setEnabled(False)
            self.action_colors.setEnabled(False)
            self.flag_start = True
            self.button_start.setText('Стоп')
            self.button_pause.setEnabled(True)
            self.worker.stop_signal(True)
            self.worker.update_params(self.tick_time)
            self.worker.start()

    def stop(self):  # сбрасывать ведра на НУ !доделать!
        self.worker.stop_signal(False)
        self.flag_start = False
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
        self.button_pause.setEnabled(False)

    def pause(self):  # пауза на поток
        if self.flag_pause:
            self.flag_pause = False
            self.worker.stop_signal(True)
            self.button_pause.setText('Пауза')
            self.worker.start()
        else:
            self.flag_pause = True
            self.worker.stop_signal(False)
            self.button_pause.setText('Продолжить')

    def resume(self):
        pass

    def change_speed(self):
        self.current_speed = self.slider_speed.value()
        self.label_speed.setText(str(self.current_speed))
        self.speed = self.current_speed
        self.tick_time = self.calculate_tick_time()
        self.label_tick_time.setText(str(self.tick_time))
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

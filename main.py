import configparser
import random
import sys
import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal as Signal, QThread
from PyQt5.QtGui import QIntValidator, QPixmap, QColor, QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget

from Buckets import Buckets
from window_colors import Ui_colors
from window_main import Ui_MainWindow

config = configparser.ConfigParser()
config.read("settings.ini")
colors = []
for i in range(1, len(config['colors']) + 1):
    colors.append(list(map(int, config['colors'][f'col{i}'].split(', '))))
aval_colors = colors


def quit_app():
    sys.exit(0)


def recolor_image(pixmap, target_color=(0, 0, 255), tolerance=180):
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
        self.main_window = main_window  # ссылка на главное окно
        self.color_boxes = [self.color_box_1, self.color_box_2, self.color_box_3,
                            self.color_box_4, self.color_box_5, self.color_box_6,
                            self.color_box_7, self.color_box_8, self.color_box_9,
                            self.color_box_10]

        # Хранение предыдущего выбора цветов для каждого ведра
        self.previous_colors = self.main_window.cur_colors.copy()

        self.btn_ok.clicked.connect(self.apply_colors)  # Применить цвета и закрыть окно

        # Подключаем обработчики изменения каждого комбо бокса
        for i, combo_box in enumerate(self.color_boxes):
            combo_box.currentIndexChanged.connect(lambda _, i=i: self.color_changed(i))

    def color_changed(self, index):
        """Обработчик изменения цвета в комбо боксе"""
        current_color = list(map(int, self.color_boxes[index].currentText().split()))  # Новый выбранный цвет
        previous_color = self.previous_colors[index]  # Предыдущий цвет

        # Обновляем список предыдущих цветов
        self.previous_colors[index] = current_color

        # Обновляем доступные цвета для всех комбо боксов
        self.update_color_boxes()

    def apply_colors(self):
        # Применяем новые цвета ведер из комбо боксов
        new_colors = []
        for i in range(len(self.color_boxes)):
            color_text = self.color_boxes[i].currentText().split()
            new_colors.append(list(map(int, color_text)))

        # Устанавливаем новые цвета в главное окно
        self.main_window.cur_colors = new_colors
        self.main_window.paint_buckets()  # Перекрасить ведра

        # Закрываем окно после применения цветов
        self.main_window.show()
        self.close()

    def update_color_boxes(self):
        """Обновляем комбо боксы, чтобы отображать только доступные цвета"""
        used_colors = self.previous_colors[:]  # Используемые цвета

        for i, combo_box in enumerate(self.color_boxes):
            current_color = self.previous_colors[i]  # Текущий выбранный цвет в этом комбо боксе
            combo_box.blockSignals(True)  # Отключаем сигналы, чтобы избежать повторных срабатываний

            # Очищаем текущий комбо бокс и добавляем текущий цвет ведра и все доступные
            combo_box.clear()
            combo_box.addItem(f'{current_color[0]} {current_color[1]} {current_color[2]}')

            # Добавляем все цвета, кроме уже использованных другими комбо боксами
            for color in colors:
                if color not in used_colors or color == current_color:
                    combo_box.addItem(f'{color[0]} {color[1]} {color[2]}')

            combo_box.blockSignals(False)  # Включаем сигналы обратно


class Main_window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.flag_start = False
        self.flag_pause = False
        self.Buckets = Buckets()

        # Инициализация уникальных цветов для ведер
        self.cur_colors = [colors[i] for i in range(10)]  # Здесь `colors` — это список возможных цветов.

        self.Form_colors = Form_Colors(self)  # Теперь можно безопасно инициализировать Form_Colors

        self.thread = QThread()
        self.worker = Worker()
        self.flag_end = False
        self.bad_num_chance = 0.1  # шанс на генерацию аварийной лампы

        self.current_speed = self.slider_speed.value()
        self.label_speed.setValidator(QIntValidator(0, 100, self))
        self.label_speed.setText(str(self.current_speed))
        self.color_boxes = [self.Form_colors.color_box_1, self.Form_colors.color_box_2, self.Form_colors.color_box_3,
                            self.Form_colors.color_box_4, self.Form_colors.color_box_5, self.Form_colors.color_box_6,
                            self.Form_colors.color_box_7, self.Form_colors.color_box_8, self.Form_colors.color_box_9,
                            self.Form_colors.color_box_10]

        self.Form_colors.btn_ok.clicked.connect(self.fc_ok)

        self.slider_speed.valueChanged.connect(self.change_speed)
        self.label_speed.textChanged.connect(self.label_speed_check)
        self.action_colors.triggered.connect(self.open_colors)
        self.action_quit.triggered.connect(quit_app)
        self.button_exit.clicked.connect(quit_app)
        self.button_start.clicked.connect(self.start)
        self.button_pause.clicked.connect(self.pause)
        self.worker.generated_number.connect(self.test)
        self.init_app()
        self.Buckets.speed = self.current_speed
        self.Buckets.tick_time = self.Buckets.calculate_tick_time()
        self.change_speed()

    def fc_ok(self):
        # При нажатии на ОК в окне выбора цветов
        self.Form_colors.apply_colors()

    def init_app(self):
        self.buckets = []

        # В этом месте `cur_colors` уже инициализирован и готов к использованию
        self.buckets = self.Buckets.generate_buckets()
        self.buckets_l = [self.bucket_1, self.bucket_2, self.bucket_3,
                          self.bucket_4, self.bucket_5, self.bucket_6, self.bucket_7,
                          self.bucket_8, self.bucket_9, self.bucket_10]

        self.label_buckets_l = [self.label_bucket_1, self.label_bucket_2, self.label_bucket_3,
                                self.label_bucket_4, self.label_bucket_5, self.label_bucket_6, self.label_bucket_7,
                                self.label_bucket_8, self.label_bucket_9, self.label_bucket_10]
        for i in range(10):
            self.buckets_l[i].show()
            self.label_buckets_l[i].show()
        self.paint_buckets()
        self.fill_buckets_text()

    def open_colors(self):
        self.Form_colors.update_color_boxes()  # Обновляем комбо боксы перед открытием окна
        self.Form_colors.show()
        self.hide()

    def fill_buckets_text(self):
        for k in range(len(self.buckets)):
            self.label_buckets_l[k].setText(f"  Bucket: {self.buckets[k][0] + 1}\n  Liters: {self.buckets[k][1]}")

    def paint_buckets(self):
        for k in range(10):
            self.buckets_l[k].setPixmap(recolor_image(self.buckets_l[k].pixmap(), target_color=self.cur_colors[k]))

    # Остальные функции остаются без изменений...

    # Остальные функции остаются без изменений...

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

    def test(self, num, bad_num):
        if not len(self.buckets) == 0:
            if self.flag_start:
                if random.random() <= self.bad_num_chance:
                    if bad_num == num:
                        self.label_bad_num.setText(f"Аварийная лампа! Ведра сопадают, пропускаем!")
                    elif self.Buckets.check_bucket_empty(bad_num % len(self.buckets)):
                        self.label_bad_num.setText(f"Аварийная лампа! Ведро пустое, пропускаем!")
                        self.label_generated_number.setText(
                            f"Gen num: {str(num)}  Buc i: {str((num + 1) % len(self.buckets))}")
                        self.Buckets.add_water_to_bucket(num % len(self.buckets))
                    else:
                        # print(self.buckets)
                        # print(bad_num, len(self.buckets), f"Аварийная лампа! Из ведра {str((bad_num + 1) % len(self.buckets))} выбежал литр(")
                        self.label_bad_num.setText(
                            f"Аварийная лампа! Из ведра {str((bad_num + 1) % len(self.buckets))} выбежал литр(")
                        self.Buckets.remove_water_from_bucket(bad_num % len(self.buckets))
                        self.label_generated_number.setText(
                            f"Gen: {str(num)}  Добавили в ведро: {str((num + 1) % len(self.buckets))}")
                        self.Buckets.add_water_to_bucket(num % len(self.buckets))
                        # print(self.buckets)
                else:
                    self.label_bad_num.setText(f"Все работает без ошибок:)")
                    self.label_generated_number.setText(
                        f"Gen: {str(num)}  Добавили в ведро: {str((num + 1) % len(self.buckets))}")
                    self.Buckets.add_water_to_bucket(num % len(self.buckets))
            if not self.Buckets.check_bucket_full(num % len(self.buckets)):
                self.hide_bucket(num % len(self.buckets))
            self.fill_buckets_text()
            # print(self.buckets, num, bad_num)
        elif not self.flag_end:
            self.flag_end = True
            # self.start()
            self.label_generated_number.setText(f"Ведра заполнены!")
            self.label_bad_num.setText(f"")

    def start(self):
        if self.flag_start:
            self.stop()
        else:
            self.flag_start = True
            self.button_start.setText('Стоп')
            self.button_pause.setEnabled(True)
            self.worker.stop_signal(True)
            self.worker.update_params(self.Buckets.tick_time)
            self.worker.start()

    def stop(self):  # сбрасывать ведра на НУ !доделать!
        self.worker.stop_signal(False)
        self.flag_start = False
        self.label_generated_number.setText('')
        self.label_bad_num.setText('')
        self.button_start.setText('Старт')
        self.button_pause.setText('Пауза')
        self.init_app()
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
        self.Buckets.speed = self.current_speed
        self.Buckets.tick_time = self.Buckets.calculate_tick_time()
        self.label_tick_time.setText(str(self.Buckets.tick_time))
        self.worker.update_params(self.Buckets.tick_time)

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

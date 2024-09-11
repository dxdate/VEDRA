import configparser
import random
import sys
import time


from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal as Signal, QThread
from PyQt5.QtGui import QIntValidator, QPixmap, QColor
from PyQt5.QtWidgets import QMainWindow

from Buckets import Buckets
from window_main import Ui_MainWindow

config = configparser.ConfigParser()
config.read("settings.ini")
colors = []
for i in range(1, len(config['colors']) + 1):
    colors.append(list(map(int, config['colors'][f'col{i}'].split(', '))))


def quit_app():
    sys.exit(0)


class Main_window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.flag_start = False
        self.flag_pause = False
        self.Buckets = Buckets()
        self.thread = QThread()
        self.worker = Worker()
        self.buckets_l = [self.bucket_1, self.bucket_2, self.bucket_3,
                          self.bucket_4, self.bucket_5, self.bucket_6, self.bucket_7,
                          self.bucket_8, self.bucket_9, self.bucket_10]

        self.label_buckets_l = [self.label_bucket_1, self.label_bucket_2, self.label_bucket_3,
                          self.label_bucket_4, self.label_bucket_5, self.label_bucket_6, self.label_bucket_7,
                          self.label_bucket_8, self.label_bucket_9, self.label_bucket_10]

        self.current_speed = self.slider_speed.value()
        self.label_speed.setValidator(QIntValidator(0, 100, self))
        self.label_speed.setText(str(self.current_speed))

        self.slider_speed.valueChanged.connect(self.change_speed)
        self.label_speed.textChanged.connect(self.label_speed_check)
        self.action_quit.triggered.connect(quit_app)
        self.button_exit.clicked.connect(quit_app)
        self.button_start.clicked.connect(self.start)
        self.button_pause.clicked.connect(self.pause)
        self.worker.generated_number.connect(self.test)
        self.Buckets.speed = self.current_speed
        self.Buckets.tick_time = self.Buckets.calculate_tick_time()
        self.change_speed()
        self.buckets = self.Buckets.generate_buckets()
        self.paint_buckets()
        self.fill_buckets_text()

    def fill_buckets_text(self):
        for i in range(len(self.buckets)):
            self.label_buckets_l[i].setText(f"  Bucket: {self.buckets[i][0] + 1}\n  Liters: {self.buckets[i][1]}")


    def paint_buckets(self):
        for i in range(10):
            self.buckets_l[i].setPixmap(self.recolor_image(self.buckets_l[i].pixmap(), target_color=colors[i]))

    def recolor_image(self, pixmap, target_color=(0, 0, 255), tolerance=180):
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
    def test(self, num):
        self.label_generated_number.setText(f"Gen num: {str(num)}  Buc i: {str(num + 1)}")
        if num == len(self.buckets):
            self.Buckets.add_water_to_bucket(num)
        else:
            self.Buckets.add_water_to_bucket(num % len(self.buckets))
        if not self.Buckets.check_bucket(num):
            self.hide_bucket(num)
        self.fill_buckets_text()

    def start(self):
        if self.flag_start:
            self.stop()
            self.flag_start = False
            self.label_generated_number.setText('')
            self.button_start.setText('Старт')
            self.button_pause.setEnabled(False)
        else:
            self.flag_start = True
            self.button_start.setText('Стоп')
            self.button_pause.setEnabled(True)
            self.worker.stop_signal(True)
            self.worker.update_params(self.Buckets.tick_time)
            self.worker.start()



    def stop(self):  # сбрасывать ведра на НУ !доделать!
        self.worker.stop_signal(False)

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
    generated_number = Signal(int)
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
            self.generated_number.emit(round(random.randint(0, 9)))  # Пример, можете заменить на свою логику
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


class Form_liters(QWidget, Ui_liters_form):
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)

        self.main_window = main_window  # Ссылка на главное окно
        self.liter_boxes = [self.liters_bucket_1, self.liters_bucket_2, self.liters_bucket_3, self.liters_bucket_4,
                            self.liters_bucket_5, self.liters_bucket_6, self.liters_bucket_7, self.liters_bucket_8,
                            self.liters_bucket_9, self.liters_bucket_10]
        self.liters = []

        # Хранение предыдущего выбора цветов для каждого ведра
        self.previous_colors = self.main_window.cur_colors.copy()

        self.btn_ok.clicked.connect(self.apply_liters)  # Применить цвета и закрыть окно
        self.btn_otmena.clicked.connect(self.cancel)  # Кнопка отмены
        self.btn_rand_liters.clicked.connect(self.assign_random_liters)

    # Случайные цвета

    def apply_liters(self):
        self.liters.clear()
        for i in range(10):
            self.liters.append([i, self.liter_boxes[i].value()])
        print(self.liters)


    def cancel(self):
        self.main_window.show()  # Показываем главное окно
        self.close()  # Закрываем текущее окно

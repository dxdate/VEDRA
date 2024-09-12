# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window_main.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(525, 600)
        MainWindow.setMinimumSize(QtCore.QSize(525, 600))
        MainWindow.setMaximumSize(QtCore.QSize(525, 600))
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        MainWindow.setInputMethodHints(QtCore.Qt.ImhNone)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_speed = QtWidgets.QLineEdit(self.centralwidget)
        self.label_speed.setGeometry(QtCore.QRect(177, 358, 50, 20))
        self.label_speed.setMaximumSize(QtCore.QSize(50, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_speed.setFont(font)
        self.label_speed.setInputMethodHints(QtCore.Qt.ImhNone)
        self.label_speed.setInputMask("")
        self.label_speed.setMaxLength(3)
        self.label_speed.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.label_speed.setObjectName("label_speed")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(290, 320, 121, 106))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.button_start = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.button_start.setObjectName("button_start")
        self.verticalLayout.addWidget(self.button_start)
        self.button_pause = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.button_pause.setEnabled(False)
        self.button_pause.setObjectName("button_pause")
        self.verticalLayout.addWidget(self.button_pause)
        self.button_exit = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.button_exit.setObjectName("button_exit")
        self.verticalLayout.addWidget(self.button_exit)
        self.label_generated_number = QtWidgets.QLabel(self.centralwidget)
        self.label_generated_number.setGeometry(QtCore.QRect(10, 10, 401, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_generated_number.setFont(font)
        self.label_generated_number.setText("")
        self.label_generated_number.setObjectName("label_generated_number")
        self.label_tick_time = QtWidgets.QLabel(self.centralwidget)
        self.label_tick_time.setGeometry(QtCore.QRect(187, 380, 40, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setKerning(False)
        self.label_tick_time.setFont(font)
        self.label_tick_time.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_tick_time.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_tick_time.setObjectName("label_tick_time")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 40, 405, 271))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.buckets_layout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.buckets_layout.setContentsMargins(0, 0, 0, 0)
        self.buckets_layout.setObjectName("buckets_layout")
        self.label_bucket_1 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_bucket_1.setFont(font)
        self.label_bucket_1.setObjectName("label_bucket_1")
        self.buckets_layout.addWidget(self.label_bucket_1, 1, 0, 1, 1)
        self.bucket_1 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.bucket_1.setMaximumSize(QtCore.QSize(16777215, 77))
        self.bucket_1.setText("")
        self.bucket_1.setPixmap(QtGui.QPixmap("images/bucket.png"))
        self.bucket_1.setObjectName("bucket_1")
        self.buckets_layout.addWidget(self.bucket_1, 0, 0, 1, 1)
        self.bucket_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.bucket_3.setMaximumSize(QtCore.QSize(16777215, 77))
        self.bucket_3.setText("")
        self.bucket_3.setPixmap(QtGui.QPixmap("images/bucket.png"))
        self.bucket_3.setObjectName("bucket_3")
        self.buckets_layout.addWidget(self.bucket_3, 0, 2, 1, 1)
        self.label_bucket_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_bucket_2.setFont(font)
        self.label_bucket_2.setObjectName("label_bucket_2")
        self.buckets_layout.addWidget(self.label_bucket_2, 1, 1, 1, 1)
        self.label_bucket_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_bucket_5.setFont(font)
        self.label_bucket_5.setObjectName("label_bucket_5")
        self.buckets_layout.addWidget(self.label_bucket_5, 1, 4, 1, 1)
        self.bucket_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.bucket_2.setMinimumSize(QtCore.QSize(0, 0))
        self.bucket_2.setMaximumSize(QtCore.QSize(75, 77))
        self.bucket_2.setText("")
        self.bucket_2.setPixmap(QtGui.QPixmap("images/bucket.png"))
        self.bucket_2.setScaledContents(False)
        self.bucket_2.setObjectName("bucket_2")
        self.buckets_layout.addWidget(self.bucket_2, 0, 1, 1, 1)
        self.label_bucket_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_bucket_3.setFont(font)
        self.label_bucket_3.setObjectName("label_bucket_3")
        self.buckets_layout.addWidget(self.label_bucket_3, 1, 2, 1, 1)
        self.bucket_8 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.bucket_8.setText("")
        self.bucket_8.setPixmap(QtGui.QPixmap("images/bucket.png"))
        self.bucket_8.setObjectName("bucket_8")
        self.buckets_layout.addWidget(self.bucket_8, 2, 2, 1, 1)
        self.bucket_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.bucket_6.setText("")
        self.bucket_6.setPixmap(QtGui.QPixmap("images/bucket.png"))
        self.bucket_6.setObjectName("bucket_6")
        self.buckets_layout.addWidget(self.bucket_6, 2, 0, 1, 1)
        self.bucket_7 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.bucket_7.setText("")
        self.bucket_7.setPixmap(QtGui.QPixmap("images/bucket.png"))
        self.bucket_7.setObjectName("bucket_7")
        self.buckets_layout.addWidget(self.bucket_7, 2, 1, 1, 1)
        self.bucket_9 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.bucket_9.setText("")
        self.bucket_9.setPixmap(QtGui.QPixmap("images/bucket.png"))
        self.bucket_9.setObjectName("bucket_9")
        self.buckets_layout.addWidget(self.bucket_9, 2, 3, 1, 1)
        self.bucket_10 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.bucket_10.setText("")
        self.bucket_10.setPixmap(QtGui.QPixmap("images/bucket.png"))
        self.bucket_10.setObjectName("bucket_10")
        self.buckets_layout.addWidget(self.bucket_10, 2, 4, 1, 1)
        self.label_bucket_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_bucket_4.setFont(font)
        self.label_bucket_4.setObjectName("label_bucket_4")
        self.buckets_layout.addWidget(self.label_bucket_4, 1, 3, 1, 1)
        self.bucket_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.bucket_4.setMaximumSize(QtCore.QSize(16777215, 77))
        self.bucket_4.setText("")
        self.bucket_4.setPixmap(QtGui.QPixmap("images/bucket.png"))
        self.bucket_4.setObjectName("bucket_4")
        self.buckets_layout.addWidget(self.bucket_4, 0, 3, 1, 1)
        self.bucket_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.bucket_5.setMaximumSize(QtCore.QSize(16777215, 77))
        self.bucket_5.setText("")
        self.bucket_5.setPixmap(QtGui.QPixmap("images/bucket.png"))
        self.bucket_5.setObjectName("bucket_5")
        self.buckets_layout.addWidget(self.bucket_5, 0, 4, 1, 1)
        self.label_bucket_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_bucket_6.setFont(font)
        self.label_bucket_6.setObjectName("label_bucket_6")
        self.buckets_layout.addWidget(self.label_bucket_6, 3, 0, 1, 1)
        self.label_bucket_7 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_bucket_7.setFont(font)
        self.label_bucket_7.setObjectName("label_bucket_7")
        self.buckets_layout.addWidget(self.label_bucket_7, 3, 1, 1, 1)
        self.label_bucket_8 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_bucket_8.setFont(font)
        self.label_bucket_8.setObjectName("label_bucket_8")
        self.buckets_layout.addWidget(self.label_bucket_8, 3, 2, 1, 1)
        self.label_bucket_9 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_bucket_9.setFont(font)
        self.label_bucket_9.setObjectName("label_bucket_9")
        self.buckets_layout.addWidget(self.label_bucket_9, 3, 3, 1, 1)
        self.label_bucket_10 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_bucket_10.setFont(font)
        self.label_bucket_10.setObjectName("label_bucket_10")
        self.buckets_layout.addWidget(self.label_bucket_10, 3, 4, 1, 1)
        self.no_edit_10 = QtWidgets.QLabel(self.centralwidget)
        self.no_edit_10.setGeometry(QtCore.QRect(144, 381, 21, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setKerning(False)
        self.no_edit_10.setFont(font)
        self.no_edit_10.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.no_edit_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.no_edit_10.setObjectName("no_edit_10")
        self.no_edit_0 = QtWidgets.QLabel(self.centralwidget)
        self.no_edit_0.setGeometry(QtCore.QRect(12, 381, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.no_edit_0.setFont(font)
        self.no_edit_0.setObjectName("no_edit_0")
        self.slider_speed = QtWidgets.QSlider(self.centralwidget)
        self.slider_speed.setGeometry(QtCore.QRect(10, 360, 150, 20))
        self.slider_speed.setMinimumSize(QtCore.QSize(150, 20))
        self.slider_speed.setMaximumSize(QtCore.QSize(150, 20))
        self.slider_speed.setMaximum(100)
        self.slider_speed.setProperty("value", 40)
        self.slider_speed.setOrientation(QtCore.Qt.Horizontal)
        self.slider_speed.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slider_speed.setTickInterval(5)
        self.slider_speed.setObjectName("slider_speed")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 525, 29))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_4 = QtWidgets.QMenu(self.menubar)
        self.menu_4.setObjectName("menu_4")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_open = QtWidgets.QAction(MainWindow)
        self.action_open.setObjectName("action_open")
        self.action_save = QtWidgets.QAction(MainWindow)
        self.action_save.setObjectName("action_save")
        self.action_quit = QtWidgets.QAction(MainWindow)
        self.action_quit.setObjectName("action_quit")
        self.action_colors = QtWidgets.QAction(MainWindow)
        self.action_colors.setObjectName("action_colors")
        self.action_about = QtWidgets.QAction(MainWindow)
        self.action_about.setObjectName("action_about")
        self.action_help = QtWidgets.QAction(MainWindow)
        self.action_help.setObjectName("action_help")
        self.action_2 = QtWidgets.QAction(MainWindow)
        self.action_2.setObjectName("action_2")
        self.menu.addAction(self.action_open)
        self.menu.addAction(self.action_save)
        self.menu.addAction(self.action_quit)
        self.menu_2.addAction(self.action_colors)
        self.menu_4.addAction(self.action_help)
        self.menu_4.addAction(self.action_2)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ведра пока без лампы( А еще рома гей"))
        self.button_start.setText(_translate("MainWindow", "Старт"))
        self.button_pause.setText(_translate("MainWindow", "Пауза"))
        self.button_exit.setText(_translate("MainWindow", "Выход"))
        self.label_tick_time.setText(_translate("MainWindow", "10000"))
        self.label_bucket_1.setText(_translate("MainWindow", "TextLabel"))
        self.label_bucket_2.setText(_translate("MainWindow", "TextLabel"))
        self.label_bucket_5.setText(_translate("MainWindow", "TextLabel"))
        self.label_bucket_3.setText(_translate("MainWindow", "TextLabel"))
        self.label_bucket_4.setText(_translate("MainWindow", "TextLabel"))
        self.label_bucket_6.setText(_translate("MainWindow", "TextLabel"))
        self.label_bucket_7.setText(_translate("MainWindow", "TextLabel"))
        self.label_bucket_8.setText(_translate("MainWindow", "TextLabel"))
        self.label_bucket_9.setText(_translate("MainWindow", "TextLabel"))
        self.label_bucket_10.setText(_translate("MainWindow", "TextLabel"))
        self.no_edit_10.setText(_translate("MainWindow", "100"))
        self.no_edit_0.setText(_translate("MainWindow", "0"))
        self.menu.setTitle(_translate("MainWindow", "Файл"))
        self.menu_2.setTitle(_translate("MainWindow", "Настройки"))
        self.menu_4.setTitle(_translate("MainWindow", "Справка"))
        self.action_open.setText(_translate("MainWindow", "Открыть"))
        self.action_save.setText(_translate("MainWindow", "Сохранить"))
        self.action_quit.setText(_translate("MainWindow", "Выход"))
        self.action_colors.setText(_translate("MainWindow", "Цвет"))
        self.action_about.setText(_translate("MainWindow", "Об авторе"))
        self.action_help.setText(_translate("MainWindow", "Руководство"))
        self.action_2.setText(_translate("MainWindow", "Об авторе"))

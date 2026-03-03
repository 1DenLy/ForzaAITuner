# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'api_v1.1.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(470, 600)
        self.actionCar = QAction(MainWindow)
        self.actionCar.setObjectName(u"actionCar")
        self.actionTuning = QAction(MainWindow)
        self.actionTuning.setObjectName(u"actionTuning")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.center = QVBoxLayout(self.centralwidget)
        self.center.setSpacing(5)
        self.center.setObjectName(u"center")
        self.center.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_up = QHBoxLayout()
        self.horizontalLayout_up.setObjectName(u"horizontalLayout_up")
        self.horizontalLayout_car = QHBoxLayout()
        self.horizontalLayout_car.setSpacing(10)
        self.horizontalLayout_car.setObjectName(u"horizontalLayout_car")
        self.label_name_car = QLabel(self.centralwidget)
        self.label_name_car.setObjectName(u"label_name_car")
        self.label_name_car.setMinimumSize(QSize(100, 20))
        self.label_name_car.setMaximumSize(QSize(200, 40))
        font = QFont()
        font.setPointSize(12)
        self.label_name_car.setFont(font)
        self.label_name_car.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_car.addWidget(self.label_name_car)

        self.label_class_car = QLabel(self.centralwidget)
        self.label_class_car.setObjectName(u"label_class_car")
        self.label_class_car.setMinimumSize(QSize(20, 20))
        self.label_class_car.setMaximumSize(QSize(40, 40))
        self.label_class_car.setFont(font)
        self.label_class_car.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_car.addWidget(self.label_class_car)

        self.label_class_number = QLabel(self.centralwidget)
        self.label_class_number.setObjectName(u"label_class_number")
        self.label_class_number.setMinimumSize(QSize(30, 20))
        self.label_class_number.setMaximumSize(QSize(40, 40))
        self.label_class_number.setFont(font)
        self.label_class_number.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_car.addWidget(self.label_class_number)


        self.horizontalLayout_up.addLayout(self.horizontalLayout_car)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_up.addItem(self.horizontalSpacer)

        self.verticalLayout_status_time = QVBoxLayout()
        self.verticalLayout_status_time.setSpacing(5)
        self.verticalLayout_status_time.setObjectName(u"verticalLayout_status_time")
        self.verticalLayout_status_time.setContentsMargins(5, 2, 5, 5)
        self.horizontalLayout_status = QHBoxLayout()
        self.horizontalLayout_status.setSpacing(10)
        self.horizontalLayout_status.setObjectName(u"horizontalLayout_status")
        self.horizontalLayout_status.setContentsMargins(2, 2, 2, 2)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_status.addWidget(self.label_3)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_status.addWidget(self.label_4)


        self.verticalLayout_status_time.addLayout(self.horizontalLayout_status)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMaximumSize(QSize(16777215, 30))
        self.label_6.setFont(font)
        self.label_6.setAlignment(Qt.AlignCenter)

        self.verticalLayout_status_time.addWidget(self.label_6)


        self.horizontalLayout_up.addLayout(self.verticalLayout_status_time)


        self.center.addLayout(self.horizontalLayout_up)

        self.verticalLayout_buttons = QVBoxLayout()
        self.verticalLayout_buttons.setObjectName(u"verticalLayout_buttons")
        self.pushButton_Start = QPushButton(self.centralwidget)
        self.pushButton_Start.setObjectName(u"pushButton_Start")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Start.sizePolicy().hasHeightForWidth())
        self.pushButton_Start.setSizePolicy(sizePolicy)
        self.pushButton_Start.setMinimumSize(QSize(80, 20))
        self.pushButton_Start.setMaximumSize(QSize(180, 40))
        self.pushButton_Start.setFont(font)

        self.verticalLayout_buttons.addWidget(self.pushButton_Start, 0, Qt.AlignHCenter)

        self.pushButton_Stop = QPushButton(self.centralwidget)
        self.pushButton_Stop.setObjectName(u"pushButton_Stop")
        sizePolicy.setHeightForWidth(self.pushButton_Stop.sizePolicy().hasHeightForWidth())
        self.pushButton_Stop.setSizePolicy(sizePolicy)
        self.pushButton_Stop.setMinimumSize(QSize(80, 20))
        self.pushButton_Stop.setMaximumSize(QSize(180, 40))
        self.pushButton_Stop.setFont(font)

        self.verticalLayout_buttons.addWidget(self.pushButton_Stop, 0, Qt.AlignHCenter)

        self.pushButton_Config = QPushButton(self.centralwidget)
        self.pushButton_Config.setObjectName(u"pushButton_Config")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_Config.sizePolicy().hasHeightForWidth())
        self.pushButton_Config.setSizePolicy(sizePolicy1)
        self.pushButton_Config.setMinimumSize(QSize(80, 20))
        self.pushButton_Config.setMaximumSize(QSize(180, 40))
        self.pushButton_Config.setFont(font)

        self.verticalLayout_buttons.addWidget(self.pushButton_Config, 0, Qt.AlignHCenter)

        self.verticalSpacer_buttons = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_buttons.addItem(self.verticalSpacer_buttons)

        self.pushButton_Settings = QPushButton(self.centralwidget)
        self.pushButton_Settings.setObjectName(u"pushButton_Settings")
        sizePolicy1.setHeightForWidth(self.pushButton_Settings.sizePolicy().hasHeightForWidth())
        self.pushButton_Settings.setSizePolicy(sizePolicy1)
        self.pushButton_Settings.setMinimumSize(QSize(80, 20))
        self.pushButton_Settings.setMaximumSize(QSize(180, 40))
        self.pushButton_Settings.setFont(font)

        self.verticalLayout_buttons.addWidget(self.pushButton_Settings, 0, Qt.AlignHCenter)

        self.pushButton_Exit = QPushButton(self.centralwidget)
        self.pushButton_Exit.setObjectName(u"pushButton_Exit")
        sizePolicy1.setHeightForWidth(self.pushButton_Exit.sizePolicy().hasHeightForWidth())
        self.pushButton_Exit.setSizePolicy(sizePolicy1)
        self.pushButton_Exit.setMinimumSize(QSize(80, 20))
        self.pushButton_Exit.setMaximumSize(QSize(180, 40))
        self.pushButton_Exit.setFont(font)

        self.verticalLayout_buttons.addWidget(self.pushButton_Exit, 0, Qt.AlignHCenter)


        self.center.addLayout(self.verticalLayout_buttons)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 470, 21))
        self.menuBar.setDefaultUp(False)
        self.menuMenu = QMenu(self.menuBar)
        self.menuMenu.setObjectName(u"menuMenu")
        self.menuEdit = QMenu(self.menuBar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuSettings = QMenu(self.menuBar)
        self.menuSettings.setObjectName(u"menuSettings")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuMenu.menuAction())
        self.menuBar.addAction(self.menuEdit.menuAction())
        self.menuBar.addAction(self.menuSettings.menuAction())
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionCar)
        self.menuEdit.addAction(self.actionTuning)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionCar.setText(QCoreApplication.translate("MainWindow", u"Car", None))
        self.actionTuning.setText(QCoreApplication.translate("MainWindow", u"Tuning", None))
        self.label_name_car.setText(QCoreApplication.translate("MainWindow", u"Name", None))
        self.label_class_car.setText(QCoreApplication.translate("MainWindow", u"00", None))
        self.label_class_number.setText(QCoreApplication.translate("MainWindow", u"000", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Status", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"00:00", None))
        self.pushButton_Start.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.pushButton_Stop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.pushButton_Config.setText(QCoreApplication.translate("MainWindow", u"Config", None))
        self.pushButton_Settings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.pushButton_Exit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.menuMenu.setTitle(QCoreApplication.translate("MainWindow", u"Main", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'config_library.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QLabel, QMainWindow, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(675, 571)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_main = QGridLayout()
        self.gridLayout_main.setObjectName(u"gridLayout_main")
        self.gridLayout_main.setHorizontalSpacing(10)
        self.gridLayout_main.setVerticalSpacing(5)
        self.gridLayout_main.setContentsMargins(5, 5, 5, 5)
        self.scrollArea_list = QScrollArea(self.centralwidget)
        self.scrollArea_list.setObjectName(u"scrollArea_list")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_list.sizePolicy().hasHeightForWidth())
        self.scrollArea_list.setSizePolicy(sizePolicy)
        self.scrollArea_list.setMinimumSize(QSize(400, 300))
        font = QFont()
        font.setPointSize(10)
        self.scrollArea_list.setFont(font)
        self.scrollArea_list.setWidgetResizable(True)
        self.scrollArea_list.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.library_list = QWidget()
        self.library_list.setObjectName(u"library_list")
        self.library_list.setGeometry(QRect(0, 0, 561, 457))
        self.verticalLayout_2 = QVBoxLayout(self.library_list)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.scrollArea_list.setWidget(self.library_list)

        self.gridLayout_main.addWidget(self.scrollArea_list, 2, 1, 10, 4)

        self.pushButton_back_to_main = QPushButton(self.centralwidget)
        self.pushButton_back_to_main.setObjectName(u"pushButton_back_to_main")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_back_to_main.sizePolicy().hasHeightForWidth())
        self.pushButton_back_to_main.setSizePolicy(sizePolicy1)
        self.pushButton_back_to_main.setMinimumSize(QSize(50, 15))
        self.pushButton_back_to_main.setMaximumSize(QSize(100, 25))
        self.pushButton_back_to_main.setFont(font)

        self.gridLayout_main.addWidget(self.pushButton_back_to_main, 12, 4, 1, 1)

        self.horizontalSpacer_sort_by = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_main.addItem(self.horizontalSpacer_sort_by, 1, 3, 1, 2)

        self.verticalSpacer_filter = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_main.addItem(self.verticalSpacer_filter, 9, 0, 3, 1)

        self.label_main_name = QLabel(self.centralwidget)
        self.label_main_name.setObjectName(u"label_main_name")
        self.label_main_name.setMinimumSize(QSize(0, 15))
        self.label_main_name.setMaximumSize(QSize(1000, 25))
        font1 = QFont()
        font1.setPointSize(16)
        self.label_main_name.setFont(font1)
        self.label_main_name.setAlignment(Qt.AlignCenter)

        self.gridLayout_main.addWidget(self.label_main_name, 0, 0, 1, 5)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_main.addWidget(self.line_2, 8, 0, 1, 1)

        self.label_filter_drive_type = QLabel(self.centralwidget)
        self.label_filter_drive_type.setObjectName(u"label_filter_drive_type")
        self.label_filter_drive_type.setMinimumSize(QSize(50, 15))
        self.label_filter_drive_type.setMaximumSize(QSize(80, 25))
        font2 = QFont()
        font2.setPointSize(14)
        self.label_filter_drive_type.setFont(font2)

        self.gridLayout_main.addWidget(self.label_filter_drive_type, 4, 0, 1, 1)

        self.comboBox_sort_by = QComboBox(self.centralwidget)
        self.comboBox_sort_by.setObjectName(u"comboBox_sort_by")
        self.comboBox_sort_by.setMinimumSize(QSize(80, 15))
        self.comboBox_sort_by.setMaximumSize(QSize(120, 25))

        self.gridLayout_main.addWidget(self.comboBox_sort_by, 1, 2, 1, 1)

        self.checkBox_drive_type_awd = QCheckBox(self.centralwidget)
        self.checkBox_drive_type_awd.setObjectName(u"checkBox_drive_type_awd")
        sizePolicy1.setHeightForWidth(self.checkBox_drive_type_awd.sizePolicy().hasHeightForWidth())
        self.checkBox_drive_type_awd.setSizePolicy(sizePolicy1)
        self.checkBox_drive_type_awd.setMinimumSize(QSize(50, 15))
        self.checkBox_drive_type_awd.setMaximumSize(QSize(80, 20))
        font3 = QFont()
        font3.setPointSize(12)
        self.checkBox_drive_type_awd.setFont(font3)

        self.gridLayout_main.addWidget(self.checkBox_drive_type_awd, 5, 0, 1, 1)

        self.checkBox_drive_type_rwd = QCheckBox(self.centralwidget)
        self.checkBox_drive_type_rwd.setObjectName(u"checkBox_drive_type_rwd")
        sizePolicy1.setHeightForWidth(self.checkBox_drive_type_rwd.sizePolicy().hasHeightForWidth())
        self.checkBox_drive_type_rwd.setSizePolicy(sizePolicy1)
        self.checkBox_drive_type_rwd.setMinimumSize(QSize(50, 15))
        self.checkBox_drive_type_rwd.setMaximumSize(QSize(80, 20))
        self.checkBox_drive_type_rwd.setFont(font3)

        self.gridLayout_main.addWidget(self.checkBox_drive_type_rwd, 6, 0, 1, 1)

        self.label_filter = QLabel(self.centralwidget)
        self.label_filter.setObjectName(u"label_filter")
        self.label_filter.setMinimumSize(QSize(50, 15))
        self.label_filter.setMaximumSize(QSize(80, 25))
        self.label_filter.setFont(font1)

        self.gridLayout_main.addWidget(self.label_filter, 2, 0, 1, 1)

        self.checkBox_drive_type_fwd = QCheckBox(self.centralwidget)
        self.checkBox_drive_type_fwd.setObjectName(u"checkBox_drive_type_fwd")
        sizePolicy1.setHeightForWidth(self.checkBox_drive_type_fwd.sizePolicy().hasHeightForWidth())
        self.checkBox_drive_type_fwd.setSizePolicy(sizePolicy1)
        self.checkBox_drive_type_fwd.setMinimumSize(QSize(50, 15))
        self.checkBox_drive_type_fwd.setMaximumSize(QSize(80, 20))
        self.checkBox_drive_type_fwd.setFont(font3)

        self.gridLayout_main.addWidget(self.checkBox_drive_type_fwd, 7, 0, 1, 1)

        self.line_1 = QFrame(self.centralwidget)
        self.line_1.setObjectName(u"line_1")
        self.line_1.setFrameShape(QFrame.Shape.HLine)
        self.line_1.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_main.addWidget(self.line_1, 3, 0, 1, 1)

        self.label_sort_by = QLabel(self.centralwidget)
        self.label_sort_by.setObjectName(u"label_sort_by")
        self.label_sort_by.setMinimumSize(QSize(60, 15))
        self.label_sort_by.setMaximumSize(QSize(40, 25))
        self.label_sort_by.setFont(font1)

        self.gridLayout_main.addWidget(self.label_sort_by, 1, 1, 1, 1)

        self.pushButton_new_config = QPushButton(self.centralwidget)
        self.pushButton_new_config.setObjectName(u"pushButton_new_config")
        sizePolicy1.setHeightForWidth(self.pushButton_new_config.sizePolicy().hasHeightForWidth())
        self.pushButton_new_config.setSizePolicy(sizePolicy1)
        self.pushButton_new_config.setMinimumSize(QSize(50, 15))
        self.pushButton_new_config.setMaximumSize(QSize(80, 25))
        self.pushButton_new_config.setFont(font)

        self.gridLayout_main.addWidget(self.pushButton_new_config, 12, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_main, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton_back_to_main.setText(QCoreApplication.translate("MainWindow", u"Back to Main", None))
        self.label_main_name.setText(QCoreApplication.translate("MainWindow", u"Config Library", None))
        self.label_filter_drive_type.setText(QCoreApplication.translate("MainWindow", u"Drive Type", None))
        self.checkBox_drive_type_awd.setText(QCoreApplication.translate("MainWindow", u"AWD", None))
        self.checkBox_drive_type_rwd.setText(QCoreApplication.translate("MainWindow", u"RWD", None))
        self.label_filter.setText(QCoreApplication.translate("MainWindow", u"Filters", None))
        self.checkBox_drive_type_fwd.setText(QCoreApplication.translate("MainWindow", u"FWD", None))
        self.label_sort_by.setText(QCoreApplication.translate("MainWindow", u"Sort by", None))
        self.pushButton_new_config.setText(QCoreApplication.translate("MainWindow", u"New config", None))
    # retranslateUi


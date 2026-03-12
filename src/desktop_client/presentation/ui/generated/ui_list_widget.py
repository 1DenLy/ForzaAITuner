# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'list widget.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QPushButton,
    QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(463, 74)
        self.gridLayout_2 = QGridLayout(Form)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(8)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.label_name = QLabel(Form)
        self.label_name.setObjectName(u"label_name")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_name.sizePolicy().hasHeightForWidth())
        self.label_name.setSizePolicy(sizePolicy)
        self.label_name.setMinimumSize(QSize(60, 15))
        self.label_name.setMaximumSize(QSize(16777215, 25))
        font = QFont()
        font.setPointSize(16)
        self.label_name.setFont(font)
        self.label_name.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_name, 0, 1, 1, 3)

        self.label_date = QLabel(Form)
        self.label_date.setObjectName(u"label_date")
        sizePolicy.setHeightForWidth(self.label_date.sizePolicy().hasHeightForWidth())
        self.label_date.setSizePolicy(sizePolicy)
        self.label_date.setMinimumSize(QSize(60, 15))
        self.label_date.setMaximumSize(QSize(16777215, 25))
        self.label_date.setFont(font)
        self.label_date.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_date, 2, 1, 1, 3)

        self.label_pi_rang = QLabel(Form)
        self.label_pi_rang.setObjectName(u"label_pi_rang")
        self.label_pi_rang.setMinimumSize(QSize(20, 0))
        self.label_pi_rang.setFont(font)
        self.label_pi_rang.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_pi_rang, 1, 1, 1, 1)

        self.label_car = QLabel(Form)
        self.label_car.setObjectName(u"label_car")
        sizePolicy.setHeightForWidth(self.label_car.sizePolicy().hasHeightForWidth())
        self.label_car.setSizePolicy(sizePolicy)
        self.label_car.setMinimumSize(QSize(60, 15))
        self.label_car.setMaximumSize(QSize(16777215, 25))
        self.label_car.setFont(font)
        self.label_car.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_car, 1, 3, 1, 1)

        self.label_1 = QLabel(Form)
        self.label_1.setObjectName(u"label_1")
        self.label_1.setMinimumSize(QSize(50, 15))
        self.label_1.setMaximumSize(QSize(80, 25))
        font1 = QFont()
        font1.setPointSize(14)
        self.label_1.setFont(font1)

        self.gridLayout.addWidget(self.label_1, 0, 0, 1, 1)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(50, 15))
        self.label_2.setMaximumSize(QSize(80, 25))
        self.label_2.setFont(font1)

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(50, 15))
        self.label_3.setMaximumSize(QSize(80, 25))
        self.label_3.setFont(font1)

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.label_pi_value = QLabel(Form)
        self.label_pi_value.setObjectName(u"label_pi_value")
        self.label_pi_value.setMinimumSize(QSize(30, 0))
        self.label_pi_value.setFont(font)
        self.label_pi_value.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_pi_value, 1, 2, 1, 1)

        self.pushButton_change = QPushButton(Form)
        self.pushButton_change.setObjectName(u"pushButton_change")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_change.sizePolicy().hasHeightForWidth())
        self.pushButton_change.setSizePolicy(sizePolicy1)
        self.pushButton_change.setMinimumSize(QSize(20, 20))
        self.pushButton_change.setMaximumSize(QSize(30, 30))
        font2 = QFont()
        font2.setPointSize(12)
        self.pushButton_change.setFont(font2)

        self.gridLayout.addWidget(self.pushButton_change, 0, 4, 3, 1)

        self.pushButton_edit = QPushButton(Form)
        self.pushButton_edit.setObjectName(u"pushButton_edit")
        sizePolicy1.setHeightForWidth(self.pushButton_edit.sizePolicy().hasHeightForWidth())
        self.pushButton_edit.setSizePolicy(sizePolicy1)
        self.pushButton_edit.setMinimumSize(QSize(20, 20))
        self.pushButton_edit.setMaximumSize(QSize(30, 30))
        self.pushButton_edit.setFont(font2)

        self.gridLayout.addWidget(self.pushButton_edit, 0, 5, 3, 1)

        self.pushButton_delete = QPushButton(Form)
        self.pushButton_delete.setObjectName(u"pushButton_delete")
        sizePolicy1.setHeightForWidth(self.pushButton_delete.sizePolicy().hasHeightForWidth())
        self.pushButton_delete.setSizePolicy(sizePolicy1)
        self.pushButton_delete.setMinimumSize(QSize(20, 20))
        self.pushButton_delete.setMaximumSize(QSize(30, 30))
        self.pushButton_delete.setFont(font2)

        self.gridLayout.addWidget(self.pushButton_delete, 0, 6, 3, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_name.setText("")
        self.label_date.setText("")
        self.label_pi_rang.setText(QCoreApplication.translate("Form", u"SS", None))
        self.label_car.setText("")
        self.label_1.setText(QCoreApplication.translate("Form", u"Name", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Car", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Date Edit", None))
        self.label_pi_value.setText(QCoreApplication.translate("Form", u"000", None))
        self.pushButton_change.setText(QCoreApplication.translate("Form", u"+", None))
        self.pushButton_edit.setText(QCoreApplication.translate("Form", u"Ed", None))
        self.pushButton_delete.setText(QCoreApplication.translate("Form", u"D", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QGridLayout, QLabel, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        if not SettingsDialog.objectName():
            SettingsDialog.setObjectName(u"SettingsDialog")
        SettingsDialog.resize(400, 300)
        self.verticalLayout = QVBoxLayout(SettingsDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout_main_assists = QGridLayout()
        self.gridLayout_main_assists.setSpacing(10)
        self.gridLayout_main_assists.setObjectName(u"gridLayout_main_assists")
        self.gridLayout_main_assists.setContentsMargins(10, 10, 10, 10)
        self.label_assists_steering = QLabel(SettingsDialog)
        self.label_assists_steering.setObjectName(u"label_assists_steering")
        self.label_assists_steering.setMinimumSize(QSize(50, 20))
        self.label_assists_steering.setMaximumSize(QSize(16777215, 40))
        font = QFont()
        font.setPointSize(12)
        self.label_assists_steering.setFont(font)
        self.label_assists_steering.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_assists.addWidget(self.label_assists_steering, 4, 0, 1, 1)

        self.comboBox_assists_abs = QComboBox(SettingsDialog)
        self.comboBox_assists_abs.setObjectName(u"comboBox_assists_abs")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_assists_abs.sizePolicy().hasHeightForWidth())
        self.comboBox_assists_abs.setSizePolicy(sizePolicy)
        self.comboBox_assists_abs.setMinimumSize(QSize(50, 20))
        self.comboBox_assists_abs.setMaximumSize(QSize(16777215, 30))

        self.gridLayout_main_assists.addWidget(self.comboBox_assists_abs, 0, 1, 1, 1)

        self.comboBox_assists_stm = QComboBox(SettingsDialog)
        self.comboBox_assists_stm.setObjectName(u"comboBox_assists_stm")
        sizePolicy.setHeightForWidth(self.comboBox_assists_stm.sizePolicy().hasHeightForWidth())
        self.comboBox_assists_stm.setSizePolicy(sizePolicy)
        self.comboBox_assists_stm.setMinimumSize(QSize(50, 20))
        self.comboBox_assists_stm.setMaximumSize(QSize(16777215, 30))

        self.gridLayout_main_assists.addWidget(self.comboBox_assists_stm, 2, 1, 1, 1)

        self.comboBox_assists_shifting = QComboBox(SettingsDialog)
        self.comboBox_assists_shifting.setObjectName(u"comboBox_assists_shifting")
        sizePolicy.setHeightForWidth(self.comboBox_assists_shifting.sizePolicy().hasHeightForWidth())
        self.comboBox_assists_shifting.setSizePolicy(sizePolicy)
        self.comboBox_assists_shifting.setMinimumSize(QSize(50, 20))
        self.comboBox_assists_shifting.setMaximumSize(QSize(16777215, 30))

        self.gridLayout_main_assists.addWidget(self.comboBox_assists_shifting, 3, 1, 1, 1)

        self.comboBox_assists_tcs = QComboBox(SettingsDialog)
        self.comboBox_assists_tcs.setObjectName(u"comboBox_assists_tcs")
        sizePolicy.setHeightForWidth(self.comboBox_assists_tcs.sizePolicy().hasHeightForWidth())
        self.comboBox_assists_tcs.setSizePolicy(sizePolicy)
        self.comboBox_assists_tcs.setMinimumSize(QSize(50, 20))
        self.comboBox_assists_tcs.setMaximumSize(QSize(16777215, 30))

        self.gridLayout_main_assists.addWidget(self.comboBox_assists_tcs, 1, 1, 1, 1)

        self.label_assists_shifting = QLabel(SettingsDialog)
        self.label_assists_shifting.setObjectName(u"label_assists_shifting")
        self.label_assists_shifting.setMinimumSize(QSize(50, 20))
        self.label_assists_shifting.setMaximumSize(QSize(16777215, 30))
        self.label_assists_shifting.setFont(font)
        self.label_assists_shifting.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_assists.addWidget(self.label_assists_shifting, 3, 0, 1, 1)

        self.label_assists_abs = QLabel(SettingsDialog)
        self.label_assists_abs.setObjectName(u"label_assists_abs")
        self.label_assists_abs.setMinimumSize(QSize(50, 20))
        self.label_assists_abs.setMaximumSize(QSize(16777215, 30))
        self.label_assists_abs.setFont(font)
        self.label_assists_abs.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_assists.addWidget(self.label_assists_abs, 0, 0, 1, 1)

        self.label_assists_tcs = QLabel(SettingsDialog)
        self.label_assists_tcs.setObjectName(u"label_assists_tcs")
        self.label_assists_tcs.setMinimumSize(QSize(50, 20))
        self.label_assists_tcs.setMaximumSize(QSize(16777215, 30))
        self.label_assists_tcs.setFont(font)
        self.label_assists_tcs.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_assists.addWidget(self.label_assists_tcs, 1, 0, 1, 1)

        self.label_assists_stm = QLabel(SettingsDialog)
        self.label_assists_stm.setObjectName(u"label_assists_stm")
        self.label_assists_stm.setMinimumSize(QSize(50, 20))
        self.label_assists_stm.setMaximumSize(QSize(16777215, 30))
        self.label_assists_stm.setFont(font)
        self.label_assists_stm.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_assists.addWidget(self.label_assists_stm, 2, 0, 1, 1)

        self.comboBox_assists_steering = QComboBox(SettingsDialog)
        self.comboBox_assists_steering.setObjectName(u"comboBox_assists_steering")
        self.comboBox_assists_steering.setMinimumSize(QSize(50, 20))
        self.comboBox_assists_steering.setMaximumSize(QSize(16777215, 40))

        self.gridLayout_main_assists.addWidget(self.comboBox_assists_steering, 4, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_main_assists)

        self.buttonBox = QDialogButtonBox(SettingsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        font1 = QFont()
        font1.setPointSize(10)
        self.buttonBox.setFont(font1)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok|QDialogButtonBox.Reset)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(SettingsDialog)
        self.buttonBox.accepted.connect(SettingsDialog.accept)
        self.buttonBox.rejected.connect(SettingsDialog.reject)

        QMetaObject.connectSlotsByName(SettingsDialog)
    # setupUi

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(QCoreApplication.translate("SettingsDialog", u"Settings", None))
        self.label_assists_steering.setText(QCoreApplication.translate("SettingsDialog", u"Steering", None))
        self.label_assists_shifting.setText(QCoreApplication.translate("SettingsDialog", u"Shifting", None))
        self.label_assists_abs.setText(QCoreApplication.translate("SettingsDialog", u"ABS", None))
        self.label_assists_tcs.setText(QCoreApplication.translate("SettingsDialog", u"TCS", None))
        self.label_assists_stm.setText(QCoreApplication.translate("SettingsDialog", u"STM", None))
    # retranslateUi


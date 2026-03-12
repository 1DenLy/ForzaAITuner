# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'config_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialog, QDialogButtonBox, QDoubleSpinBox, QFrame,
    QGridLayout, QLabel, QLayout, QLineEdit,
    QSizePolicy, QSlider, QSpacerItem, QSpinBox,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_ConfigDialog(object):
    def setupUi(self, ConfigDialog):
        if not ConfigDialog.objectName():
            ConfigDialog.setObjectName(u"ConfigDialog")
        ConfigDialog.resize(500, 400)
        ConfigDialog.setMinimumSize(QSize(400, 300))
        self.verticalLayout = QVBoxLayout(ConfigDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_info = QLabel(ConfigDialog)
        self.label_info.setObjectName(u"label_info")
        font = QFont()
        font.setPointSize(10)
        self.label_info.setFont(font)
        self.label_info.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_info)

        self.tabWidget = QTabWidget(ConfigDialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMinimumSize(QSize(0, 170))
        self.tabWidget.setFont(font)
        self.tab_session = QWidget()
        self.tab_session.setObjectName(u"tab_session")
        self.gridLayout_14 = QGridLayout(self.tab_session)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.horizontalSpacer_session_r = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer_session_r, 1, 2, 1, 1)

        self.horizontalSpacer_session_l = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer_session_l, 1, 0, 1, 1)

        self.gridLayout_main_session = QGridLayout()
        self.gridLayout_main_session.setObjectName(u"gridLayout_main_session")
        self.gridLayout_main_session.setHorizontalSpacing(20)
        self.gridLayout_main_session.setVerticalSpacing(15)
        self.gridLayout_main_session.setContentsMargins(5, 5, 5, 5)
        self.label_session_class = QLabel(self.tab_session)
        self.label_session_class.setObjectName(u"label_session_class")
        self.label_session_class.setMinimumSize(QSize(40, 20))
        self.label_session_class.setMaximumSize(QSize(16777215, 30))
        font1 = QFont()
        font1.setPointSize(12)
        self.label_session_class.setFont(font1)
        self.label_session_class.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_session.addWidget(self.label_session_class, 2, 0, 1, 1)

        self.spinBox_session_class = QSpinBox(self.tab_session)
        self.spinBox_session_class.setObjectName(u"spinBox_session_class")
        self.spinBox_session_class.setAlignment(Qt.AlignJustify|Qt.AlignVCenter)
        self.spinBox_session_class.setMinimum(-10000)
        self.spinBox_session_class.setMaximum(10000)

        self.gridLayout_main_session.addWidget(self.spinBox_session_class, 2, 1, 1, 1)

        self.lineEdit_session_car = QLineEdit(self.tab_session)
        self.lineEdit_session_car.setObjectName(u"lineEdit_session_car")
        self.lineEdit_session_car.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_session.addWidget(self.lineEdit_session_car, 1, 1, 1, 1)

        self.label_session_car = QLabel(self.tab_session)
        self.label_session_car.setObjectName(u"label_session_car")
        self.label_session_car.setMinimumSize(QSize(40, 20))
        self.label_session_car.setMaximumSize(QSize(16777215, 30))
        self.label_session_car.setFont(font1)
        self.label_session_car.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_session.addWidget(self.label_session_car, 1, 0, 1, 1)

        self.label_session_location = QLabel(self.tab_session)
        self.label_session_location.setObjectName(u"label_session_location")
        self.label_session_location.setMinimumSize(QSize(40, 20))
        self.label_session_location.setMaximumSize(QSize(70, 30))
        self.label_session_location.setFont(font1)
        self.label_session_location.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_session.addWidget(self.label_session_location, 4, 0, 1, 1)

        self.label_session_surface = QLabel(self.tab_session)
        self.label_session_surface.setObjectName(u"label_session_surface")
        self.label_session_surface.setMinimumSize(QSize(40, 20))
        self.label_session_surface.setMaximumSize(QSize(70, 30))
        self.label_session_surface.setFont(font1)
        self.label_session_surface.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_session.addWidget(self.label_session_surface, 5, 0, 1, 1)

        self.label_session_road_type = QLabel(self.tab_session)
        self.label_session_road_type.setObjectName(u"label_session_road_type")
        self.label_session_road_type.setMinimumSize(QSize(40, 20))
        self.label_session_road_type.setMaximumSize(QSize(70, 30))
        self.label_session_road_type.setFont(font1)
        self.label_session_road_type.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_session.addWidget(self.label_session_road_type, 3, 0, 1, 1)

        self.comboBox_session_surface = QComboBox(self.tab_session)
        self.comboBox_session_surface.addItem("")
        self.comboBox_session_surface.setObjectName(u"comboBox_session_surface")
        self.comboBox_session_surface.setMinimumSize(QSize(70, 15))
        self.comboBox_session_surface.setMaximumSize(QSize(16777215, 25))
        self.comboBox_session_surface.setFont(font)

        self.gridLayout_main_session.addWidget(self.comboBox_session_surface, 5, 1, 1, 1)

        self.comboBox_session_location = QComboBox(self.tab_session)
        self.comboBox_session_location.addItem("")
        self.comboBox_session_location.setObjectName(u"comboBox_session_location")
        self.comboBox_session_location.setMinimumSize(QSize(70, 15))
        self.comboBox_session_location.setMaximumSize(QSize(16777215, 25))
        self.comboBox_session_location.setFont(font)

        self.gridLayout_main_session.addWidget(self.comboBox_session_location, 4, 1, 1, 1)

        self.label_session_name = QLabel(self.tab_session)
        self.label_session_name.setObjectName(u"label_session_name")
        self.label_session_name.setMinimumSize(QSize(40, 20))
        self.label_session_name.setMaximumSize(QSize(70, 30))
        self.label_session_name.setFont(font1)
        self.label_session_name.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_session.addWidget(self.label_session_name, 0, 0, 1, 1)

        self.comboBox_session_road_type = QComboBox(self.tab_session)
        self.comboBox_session_road_type.addItem("")
        self.comboBox_session_road_type.setObjectName(u"comboBox_session_road_type")
        self.comboBox_session_road_type.setMinimumSize(QSize(70, 15))
        self.comboBox_session_road_type.setMaximumSize(QSize(16777215, 25))
        self.comboBox_session_road_type.setFont(font)

        self.gridLayout_main_session.addWidget(self.comboBox_session_road_type, 3, 1, 1, 1)

        self.lineEdit_session_name = QLineEdit(self.tab_session)
        self.lineEdit_session_name.setObjectName(u"lineEdit_session_name")
        self.lineEdit_session_name.setMinimumSize(QSize(70, 15))
        self.lineEdit_session_name.setMaximumSize(QSize(16777215, 25))
        self.lineEdit_session_name.setFont(font)
        self.lineEdit_session_name.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_session.addWidget(self.lineEdit_session_name, 0, 1, 1, 1)


        self.gridLayout_14.addLayout(self.gridLayout_main_session, 1, 1, 1, 1)

        self.verticalSpacer_session_d = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.gridLayout_14.addItem(self.verticalSpacer_session_d, 2, 1, 1, 1)

        self.verticalSpacer_session_u = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.gridLayout_14.addItem(self.verticalSpacer_session_u, 0, 1, 1, 1)

        self.tabWidget.addTab(self.tab_session, "")
        self.tab_info = QWidget()
        self.tab_info.setObjectName(u"tab_info")
        self.gridLayout_5 = QGridLayout(self.tab_info)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.verticalSpacer_info_u = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.gridLayout_5.addItem(self.verticalSpacer_info_u, 0, 1, 1, 1)

        self.verticalSpacer_info_d = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.gridLayout_5.addItem(self.verticalSpacer_info_d, 2, 1, 1, 1)

        self.gridLayout_main_info = QGridLayout()
        self.gridLayout_main_info.setObjectName(u"gridLayout_main_info")
        self.gridLayout_main_info.setHorizontalSpacing(20)
        self.gridLayout_main_info.setVerticalSpacing(15)
        self.gridLayout_main_info.setContentsMargins(10, 10, 10, 10)
        self.spinBox_info_weight = QSpinBox(self.tab_info)
        self.spinBox_info_weight.setObjectName(u"spinBox_info_weight")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_info_weight.sizePolicy().hasHeightForWidth())
        self.spinBox_info_weight.setSizePolicy(sizePolicy)
        self.spinBox_info_weight.setMinimumSize(QSize(60, 20))
        self.spinBox_info_weight.setMaximumSize(QSize(200, 30))
        self.spinBox_info_weight.setFont(font1)
        self.spinBox_info_weight.setAlignment(Qt.AlignCenter)
        self.spinBox_info_weight.setMinimum(-10000)
        self.spinBox_info_weight.setMaximum(10000)
        self.spinBox_info_weight.setValue(0)

        self.gridLayout_main_info.addWidget(self.spinBox_info_weight, 0, 1, 1, 1)

        self.spinBox_info_power = QSpinBox(self.tab_info)
        self.spinBox_info_power.setObjectName(u"spinBox_info_power")
        sizePolicy.setHeightForWidth(self.spinBox_info_power.sizePolicy().hasHeightForWidth())
        self.spinBox_info_power.setSizePolicy(sizePolicy)
        self.spinBox_info_power.setMinimumSize(QSize(60, 20))
        self.spinBox_info_power.setMaximumSize(QSize(200, 30))
        self.spinBox_info_power.setFont(font1)
        self.spinBox_info_power.setAlignment(Qt.AlignCenter)
        self.spinBox_info_power.setMinimum(-10000)
        self.spinBox_info_power.setMaximum(10000)

        self.gridLayout_main_info.addWidget(self.spinBox_info_power, 2, 1, 1, 1)

        self.label_info_power = QLabel(self.tab_info)
        self.label_info_power.setObjectName(u"label_info_power")
        self.label_info_power.setMinimumSize(QSize(50, 15))
        self.label_info_power.setMaximumSize(QSize(120, 25))
        self.label_info_power.setFont(font1)
        self.label_info_power.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_info.addWidget(self.label_info_power, 2, 0, 1, 1, Qt.AlignHCenter)

        self.label_info_front_weight = QLabel(self.tab_info)
        self.label_info_front_weight.setObjectName(u"label_info_front_weight")
        self.label_info_front_weight.setMinimumSize(QSize(50, 15))
        self.label_info_front_weight.setMaximumSize(QSize(120, 25))
        self.label_info_front_weight.setFont(font1)
        self.label_info_front_weight.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_info.addWidget(self.label_info_front_weight, 1, 0, 1, 1, Qt.AlignHCenter)

        self.label_info_drive_type = QLabel(self.tab_info)
        self.label_info_drive_type.setObjectName(u"label_info_drive_type")
        self.label_info_drive_type.setMinimumSize(QSize(50, 15))
        self.label_info_drive_type.setMaximumSize(QSize(120, 25))
        self.label_info_drive_type.setFont(font1)
        self.label_info_drive_type.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_info.addWidget(self.label_info_drive_type, 5, 0, 1, 1, Qt.AlignHCenter)

        self.label_info_power_unit = QLabel(self.tab_info)
        self.label_info_power_unit.setObjectName(u"label_info_power_unit")
        sizePolicy.setHeightForWidth(self.label_info_power_unit.sizePolicy().hasHeightForWidth())
        self.label_info_power_unit.setSizePolicy(sizePolicy)
        self.label_info_power_unit.setMinimumSize(QSize(15, 15))
        self.label_info_power_unit.setMaximumSize(QSize(25, 25))
        self.label_info_power_unit.setFont(font)
        self.label_info_power_unit.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_main_info.addWidget(self.label_info_power_unit, 2, 2, 1, 1)

        self.label_info_drive_type_unit = QLabel(self.tab_info)
        self.label_info_drive_type_unit.setObjectName(u"label_info_drive_type_unit")
        sizePolicy.setHeightForWidth(self.label_info_drive_type_unit.sizePolicy().hasHeightForWidth())
        self.label_info_drive_type_unit.setSizePolicy(sizePolicy)
        self.label_info_drive_type_unit.setMinimumSize(QSize(15, 15))
        self.label_info_drive_type_unit.setMaximumSize(QSize(25, 25))
        self.label_info_drive_type_unit.setFont(font)
        self.label_info_drive_type_unit.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_main_info.addWidget(self.label_info_drive_type_unit, 5, 2, 1, 1)

        self.label_info_front_weight_unit = QLabel(self.tab_info)
        self.label_info_front_weight_unit.setObjectName(u"label_info_front_weight_unit")
        sizePolicy.setHeightForWidth(self.label_info_front_weight_unit.sizePolicy().hasHeightForWidth())
        self.label_info_front_weight_unit.setSizePolicy(sizePolicy)
        self.label_info_front_weight_unit.setMinimumSize(QSize(15, 15))
        self.label_info_front_weight_unit.setMaximumSize(QSize(25, 25))
        self.label_info_front_weight_unit.setFont(font)
        self.label_info_front_weight_unit.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_main_info.addWidget(self.label_info_front_weight_unit, 1, 2, 1, 1)

        self.label_info_engine_placement_unit = QLabel(self.tab_info)
        self.label_info_engine_placement_unit.setObjectName(u"label_info_engine_placement_unit")
        sizePolicy.setHeightForWidth(self.label_info_engine_placement_unit.sizePolicy().hasHeightForWidth())
        self.label_info_engine_placement_unit.setSizePolicy(sizePolicy)
        self.label_info_engine_placement_unit.setMinimumSize(QSize(15, 15))
        self.label_info_engine_placement_unit.setMaximumSize(QSize(25, 25))
        self.label_info_engine_placement_unit.setFont(font)
        self.label_info_engine_placement_unit.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_main_info.addWidget(self.label_info_engine_placement_unit, 6, 2, 1, 1)

        self.spinBox_info_suspension_travel = QSpinBox(self.tab_info)
        self.spinBox_info_suspension_travel.setObjectName(u"spinBox_info_suspension_travel")
        sizePolicy.setHeightForWidth(self.spinBox_info_suspension_travel.sizePolicy().hasHeightForWidth())
        self.spinBox_info_suspension_travel.setSizePolicy(sizePolicy)
        self.spinBox_info_suspension_travel.setMinimumSize(QSize(60, 20))
        self.spinBox_info_suspension_travel.setMaximumSize(QSize(200, 30))
        self.spinBox_info_suspension_travel.setFont(font1)
        self.spinBox_info_suspension_travel.setAlignment(Qt.AlignCenter)
        self.spinBox_info_suspension_travel.setMinimum(-10000)
        self.spinBox_info_suspension_travel.setMaximum(10000)

        self.gridLayout_main_info.addWidget(self.spinBox_info_suspension_travel, 4, 1, 1, 1)

        self.label_info_suspension_travel = QLabel(self.tab_info)
        self.label_info_suspension_travel.setObjectName(u"label_info_suspension_travel")
        self.label_info_suspension_travel.setMinimumSize(QSize(50, 15))
        self.label_info_suspension_travel.setMaximumSize(QSize(120, 25))
        self.label_info_suspension_travel.setFont(font1)
        self.label_info_suspension_travel.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_info.addWidget(self.label_info_suspension_travel, 4, 0, 1, 1, Qt.AlignHCenter)

        self.label_info_suspension_travel_unit = QLabel(self.tab_info)
        self.label_info_suspension_travel_unit.setObjectName(u"label_info_suspension_travel_unit")
        self.label_info_suspension_travel_unit.setMinimumSize(QSize(15, 15))
        self.label_info_suspension_travel_unit.setMaximumSize(QSize(25, 25))
        self.label_info_suspension_travel_unit.setFont(font)
        self.label_info_suspension_travel_unit.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_main_info.addWidget(self.label_info_suspension_travel_unit, 4, 2, 1, 1)

        self.comboBox_info_drive_type = QComboBox(self.tab_info)
        self.comboBox_info_drive_type.addItem("")
        self.comboBox_info_drive_type.setObjectName(u"comboBox_info_drive_type")
        sizePolicy.setHeightForWidth(self.comboBox_info_drive_type.sizePolicy().hasHeightForWidth())
        self.comboBox_info_drive_type.setSizePolicy(sizePolicy)
        self.comboBox_info_drive_type.setMinimumSize(QSize(60, 20))
        self.comboBox_info_drive_type.setMaximumSize(QSize(200, 30))
        self.comboBox_info_drive_type.setFont(font1)

        self.gridLayout_main_info.addWidget(self.comboBox_info_drive_type, 5, 1, 1, 1)

        self.label_info_weight = QLabel(self.tab_info)
        self.label_info_weight.setObjectName(u"label_info_weight")
        self.label_info_weight.setMinimumSize(QSize(50, 15))
        self.label_info_weight.setMaximumSize(QSize(120, 25))
        self.label_info_weight.setFont(font1)
        self.label_info_weight.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_info.addWidget(self.label_info_weight, 0, 0, 1, 1, Qt.AlignHCenter)

        self.label_info_weight_unit = QLabel(self.tab_info)
        self.label_info_weight_unit.setObjectName(u"label_info_weight_unit")
        sizePolicy.setHeightForWidth(self.label_info_weight_unit.sizePolicy().hasHeightForWidth())
        self.label_info_weight_unit.setSizePolicy(sizePolicy)
        self.label_info_weight_unit.setMinimumSize(QSize(15, 15))
        self.label_info_weight_unit.setMaximumSize(QSize(25, 25))
        self.label_info_weight_unit.setFont(font)
        self.label_info_weight_unit.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_main_info.addWidget(self.label_info_weight_unit, 0, 2, 1, 1)

        self.comboBox_info_engine_placement = QComboBox(self.tab_info)
        self.comboBox_info_engine_placement.addItem("")
        self.comboBox_info_engine_placement.setObjectName(u"comboBox_info_engine_placement")
        sizePolicy.setHeightForWidth(self.comboBox_info_engine_placement.sizePolicy().hasHeightForWidth())
        self.comboBox_info_engine_placement.setSizePolicy(sizePolicy)
        self.comboBox_info_engine_placement.setMinimumSize(QSize(60, 20))
        self.comboBox_info_engine_placement.setMaximumSize(QSize(200, 30))
        self.comboBox_info_engine_placement.setFont(font1)

        self.gridLayout_main_info.addWidget(self.comboBox_info_engine_placement, 6, 1, 1, 1)

        self.label_info_engine_placement = QLabel(self.tab_info)
        self.label_info_engine_placement.setObjectName(u"label_info_engine_placement")
        self.label_info_engine_placement.setMinimumSize(QSize(50, 15))
        self.label_info_engine_placement.setMaximumSize(QSize(120, 25))
        self.label_info_engine_placement.setFont(font1)
        self.label_info_engine_placement.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_info.addWidget(self.label_info_engine_placement, 6, 0, 1, 1, Qt.AlignHCenter)

        self.label_info_torque = QLabel(self.tab_info)
        self.label_info_torque.setObjectName(u"label_info_torque")
        self.label_info_torque.setMinimumSize(QSize(50, 15))
        self.label_info_torque.setMaximumSize(QSize(120, 25))
        self.label_info_torque.setFont(font1)
        self.label_info_torque.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_info.addWidget(self.label_info_torque, 3, 0, 1, 1, Qt.AlignHCenter)

        self.spinBox_info_torque = QSpinBox(self.tab_info)
        self.spinBox_info_torque.setObjectName(u"spinBox_info_torque")
        sizePolicy.setHeightForWidth(self.spinBox_info_torque.sizePolicy().hasHeightForWidth())
        self.spinBox_info_torque.setSizePolicy(sizePolicy)
        self.spinBox_info_torque.setMinimumSize(QSize(60, 20))
        self.spinBox_info_torque.setMaximumSize(QSize(200, 30))
        self.spinBox_info_torque.setFont(font1)
        self.spinBox_info_torque.setAlignment(Qt.AlignCenter)
        self.spinBox_info_torque.setMinimum(-10000)
        self.spinBox_info_torque.setMaximum(10000)

        self.gridLayout_main_info.addWidget(self.spinBox_info_torque, 3, 1, 1, 1)

        self.label_info_torque_unit = QLabel(self.tab_info)
        self.label_info_torque_unit.setObjectName(u"label_info_torque_unit")
        self.label_info_torque_unit.setMinimumSize(QSize(15, 15))
        self.label_info_torque_unit.setMaximumSize(QSize(25, 25))
        self.label_info_torque_unit.setFont(font)
        self.label_info_torque_unit.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_main_info.addWidget(self.label_info_torque_unit, 3, 2, 1, 1)

        self.doubleSpinBox_info_front_weight = QDoubleSpinBox(self.tab_info)
        self.doubleSpinBox_info_front_weight.setObjectName(u"doubleSpinBox_info_front_weight")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_info_front_weight.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_info_front_weight.setSizePolicy(sizePolicy)
        self.doubleSpinBox_info_front_weight.setMinimumSize(QSize(60, 20))
        self.doubleSpinBox_info_front_weight.setMaximumSize(QSize(200, 30))
        self.doubleSpinBox_info_front_weight.setFont(font1)
        self.doubleSpinBox_info_front_weight.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_info_front_weight.setDecimals(1)
        self.doubleSpinBox_info_front_weight.setMinimum(-10000.000000000000000)
        self.doubleSpinBox_info_front_weight.setMaximum(10000.000000000000000)

        self.gridLayout_main_info.addWidget(self.doubleSpinBox_info_front_weight, 1, 1, 1, 1)


        self.gridLayout_5.addLayout(self.gridLayout_main_info, 1, 1, 1, 1)

        self.horizontalSpacer_info_r = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_info_r, 1, 2, 1, 1)

        self.horizontalSpacer_info_l = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_info_l, 1, 0, 1, 1)

        self.tabWidget.addTab(self.tab_info, "")
        self.tab_tires = QWidget()
        self.tab_tires.setObjectName(u"tab_tires")
        self.gridLayout_3 = QGridLayout(self.tab_tires)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalSpacer_tire_d = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.gridLayout_3.addItem(self.horizontalSpacer_tire_d, 2, 1, 1, 1)

        self.gridLayout_tire = QGridLayout()
        self.gridLayout_tire.setObjectName(u"gridLayout_tire")
        self.gridLayout_tire.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout_tire.setHorizontalSpacing(20)
        self.gridLayout_tire.setVerticalSpacing(15)
        self.gridLayout_tire.setContentsMargins(5, 5, 5, 5)
        self.label_tire_tier = QLabel(self.tab_tires)
        self.label_tire_tier.setObjectName(u"label_tire_tier")
        self.label_tire_tier.setMinimumSize(QSize(40, 15))
        self.label_tire_tier.setMaximumSize(QSize(50, 25))
        self.label_tire_tier.setFont(font1)
        self.label_tire_tier.setAlignment(Qt.AlignCenter)

        self.gridLayout_tire.addWidget(self.label_tire_tier, 0, 0, 1, 1)

        self.horizontalSlider_tire_front_pressure = QSlider(self.tab_tires)
        self.horizontalSlider_tire_front_pressure.setObjectName(u"horizontalSlider_tire_front_pressure")
        self.horizontalSlider_tire_front_pressure.setMinimumSize(QSize(120, 15))
        self.horizontalSlider_tire_front_pressure.setMaximumSize(QSize(16777215, 25))
        self.horizontalSlider_tire_front_pressure.setMinimum(-10000)
        self.horizontalSlider_tire_front_pressure.setMaximum(10000)
        self.horizontalSlider_tire_front_pressure.setSingleStep(1)
        self.horizontalSlider_tire_front_pressure.setPageStep(1)
        self.horizontalSlider_tire_front_pressure.setValue(0)
        self.horizontalSlider_tire_front_pressure.setOrientation(Qt.Horizontal)

        self.gridLayout_tire.addWidget(self.horizontalSlider_tire_front_pressure, 1, 2, 1, 2)

        self.horizontalSlider_tire_rear_pressure = QSlider(self.tab_tires)
        self.horizontalSlider_tire_rear_pressure.setObjectName(u"horizontalSlider_tire_rear_pressure")
        self.horizontalSlider_tire_rear_pressure.setMinimumSize(QSize(120, 15))
        self.horizontalSlider_tire_rear_pressure.setMaximumSize(QSize(16777215, 25))
        self.horizontalSlider_tire_rear_pressure.setMinimum(-10000)
        self.horizontalSlider_tire_rear_pressure.setMaximum(10000)
        self.horizontalSlider_tire_rear_pressure.setPageStep(1)
        self.horizontalSlider_tire_rear_pressure.setValue(0)
        self.horizontalSlider_tire_rear_pressure.setOrientation(Qt.Horizontal)

        self.gridLayout_tire.addWidget(self.horizontalSlider_tire_rear_pressure, 2, 2, 1, 2)

        self.label_tire_rear_value = QLabel(self.tab_tires)
        self.label_tire_rear_value.setObjectName(u"label_tire_rear_value")
        self.label_tire_rear_value.setMinimumSize(QSize(25, 15))
        self.label_tire_rear_value.setMaximumSize(QSize(25, 25))
        self.label_tire_rear_value.setFont(font1)
        self.label_tire_rear_value.setAlignment(Qt.AlignCenter)

        self.gridLayout_tire.addWidget(self.label_tire_rear_value, 2, 4, 1, 1)

        self.label_tire_pressure = QLabel(self.tab_tires)
        self.label_tire_pressure.setObjectName(u"label_tire_pressure")
        self.label_tire_pressure.setMinimumSize(QSize(0, 15))
        self.label_tire_pressure.setMaximumSize(QSize(16777215, 25))
        self.label_tire_pressure.setFont(font1)
        self.label_tire_pressure.setAlignment(Qt.AlignCenter)

        self.gridLayout_tire.addWidget(self.label_tire_pressure, 0, 2, 1, 3)

        self.label_tire_front_value = QLabel(self.tab_tires)
        self.label_tire_front_value.setObjectName(u"label_tire_front_value")
        self.label_tire_front_value.setMinimumSize(QSize(25, 15))
        self.label_tire_front_value.setMaximumSize(QSize(25, 25))
        self.label_tire_front_value.setFont(font1)
        self.label_tire_front_value.setAlignment(Qt.AlignCenter)

        self.gridLayout_tire.addWidget(self.label_tire_front_value, 1, 4, 1, 1)

        self.line_2 = QFrame(self.tab_tires)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_tire.addWidget(self.line_2, 0, 5, 3, 1)

        self.label_tire_width = QLabel(self.tab_tires)
        self.label_tire_width.setObjectName(u"label_tire_width")
        self.label_tire_width.setMinimumSize(QSize(0, 15))
        self.label_tire_width.setMaximumSize(QSize(16777215, 25))
        self.label_tire_width.setFont(font1)
        self.label_tire_width.setAlignment(Qt.AlignCenter)

        self.gridLayout_tire.addWidget(self.label_tire_width, 0, 6, 1, 1)

        self.spinBox_tire_width_front = QSpinBox(self.tab_tires)
        self.spinBox_tire_width_front.setObjectName(u"spinBox_tire_width_front")
        sizePolicy.setHeightForWidth(self.spinBox_tire_width_front.sizePolicy().hasHeightForWidth())
        self.spinBox_tire_width_front.setSizePolicy(sizePolicy)
        self.spinBox_tire_width_front.setMinimumSize(QSize(60, 15))
        self.spinBox_tire_width_front.setMaximumSize(QSize(80, 25))
        self.spinBox_tire_width_front.setFont(font1)
        self.spinBox_tire_width_front.setAlignment(Qt.AlignCenter)
        self.spinBox_tire_width_front.setMinimum(-10000)
        self.spinBox_tire_width_front.setMaximum(10000)

        self.gridLayout_tire.addWidget(self.spinBox_tire_width_front, 1, 6, 1, 1)

        self.spinBox_tire_width_rear = QSpinBox(self.tab_tires)
        self.spinBox_tire_width_rear.setObjectName(u"spinBox_tire_width_rear")
        sizePolicy.setHeightForWidth(self.spinBox_tire_width_rear.sizePolicy().hasHeightForWidth())
        self.spinBox_tire_width_rear.setSizePolicy(sizePolicy)
        self.spinBox_tire_width_rear.setMinimumSize(QSize(60, 15))
        self.spinBox_tire_width_rear.setMaximumSize(QSize(80, 25))
        self.spinBox_tire_width_rear.setFont(font1)
        self.spinBox_tire_width_rear.setAlignment(Qt.AlignCenter)
        self.spinBox_tire_width_rear.setMinimum(-10000)
        self.spinBox_tire_width_rear.setMaximum(10000)

        self.gridLayout_tire.addWidget(self.spinBox_tire_width_rear, 2, 6, 1, 1)

        self.label_tire_rear = QLabel(self.tab_tires)
        self.label_tire_rear.setObjectName(u"label_tire_rear")
        self.label_tire_rear.setMinimumSize(QSize(40, 15))
        self.label_tire_rear.setMaximumSize(QSize(50, 25))
        self.label_tire_rear.setFont(font1)
        self.label_tire_rear.setAlignment(Qt.AlignCenter)

        self.gridLayout_tire.addWidget(self.label_tire_rear, 2, 0, 1, 1)

        self.label_tire_front = QLabel(self.tab_tires)
        self.label_tire_front.setObjectName(u"label_tire_front")
        self.label_tire_front.setMinimumSize(QSize(40, 15))
        self.label_tire_front.setMaximumSize(QSize(50, 25))
        self.label_tire_front.setFont(font1)
        self.label_tire_front.setAlignment(Qt.AlignCenter)

        self.gridLayout_tire.addWidget(self.label_tire_front, 1, 0, 1, 1)

        self.label_tire_compound = QLabel(self.tab_tires)
        self.label_tire_compound.setObjectName(u"label_tire_compound")
        self.label_tire_compound.setMinimumSize(QSize(0, 15))
        self.label_tire_compound.setMaximumSize(QSize(16777215, 25))
        self.label_tire_compound.setFont(font1)
        self.label_tire_compound.setAlignment(Qt.AlignCenter)

        self.gridLayout_tire.addWidget(self.label_tire_compound, 0, 8, 1, 1)

        self.comboBox_tire_compound = QComboBox(self.tab_tires)
        self.comboBox_tire_compound.setObjectName(u"comboBox_tire_compound")
        self.comboBox_tire_compound.setMinimumSize(QSize(60, 15))
        self.comboBox_tire_compound.setMaximumSize(QSize(90, 25))
        self.comboBox_tire_compound.setFont(font)

        self.gridLayout_tire.addWidget(self.comboBox_tire_compound, 1, 8, 2, 1)

        self.line_1 = QFrame(self.tab_tires)
        self.line_1.setObjectName(u"line_1")
        self.line_1.setFrameShape(QFrame.Shape.VLine)
        self.line_1.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_tire.addWidget(self.line_1, 0, 1, 3, 1)

        self.line_3 = QFrame(self.tab_tires)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_tire.addWidget(self.line_3, 0, 7, 3, 1)


        self.gridLayout_3.addLayout(self.gridLayout_tire, 1, 1, 1, 1)

        self.horizontalSpacer_tire_l = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_tire_l, 1, 0, 1, 1)

        self.horizontalSpacer_tire_r = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_tire_r, 1, 2, 1, 1)

        self.horizontalSpacer_tire_u = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.gridLayout_3.addItem(self.horizontalSpacer_tire_u, 0, 1, 1, 1)

        self.tabWidget.addTab(self.tab_tires, "")
        self.tab_alignment = QWidget()
        self.tab_alignment.setObjectName(u"tab_alignment")
        self.gridLayout_4 = QGridLayout(self.tab_alignment)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.verticalSpacer_alignment_d = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.gridLayout_4.addItem(self.verticalSpacer_alignment_d, 2, 1, 1, 1)

        self.gridLayout_castor_toe = QGridLayout()
        self.gridLayout_castor_toe.setSpacing(20)
        self.gridLayout_castor_toe.setObjectName(u"gridLayout_castor_toe")
        self.gridLayout_castor_toe.setContentsMargins(10, 10, 10, 10)
        self.horizontalSlider_alignment_rear_camber = QSlider(self.tab_alignment)
        self.horizontalSlider_alignment_rear_camber.setObjectName(u"horizontalSlider_alignment_rear_camber")
        sizePolicy.setHeightForWidth(self.horizontalSlider_alignment_rear_camber.sizePolicy().hasHeightForWidth())
        self.horizontalSlider_alignment_rear_camber.setSizePolicy(sizePolicy)
        self.horizontalSlider_alignment_rear_camber.setMinimumSize(QSize(40, 10))
        self.horizontalSlider_alignment_rear_camber.setMaximumSize(QSize(16777215, 20))
        self.horizontalSlider_alignment_rear_camber.setMinimum(-10000)
        self.horizontalSlider_alignment_rear_camber.setMaximum(10000)
        self.horizontalSlider_alignment_rear_camber.setPageStep(1)
        self.horizontalSlider_alignment_rear_camber.setValue(0)
        self.horizontalSlider_alignment_rear_camber.setOrientation(Qt.Horizontal)

        self.gridLayout_castor_toe.addWidget(self.horizontalSlider_alignment_rear_camber, 2, 1, 1, 1)

        self.label_alignment_camber = QLabel(self.tab_alignment)
        self.label_alignment_camber.setObjectName(u"label_alignment_camber")
        self.label_alignment_camber.setMinimumSize(QSize(40, 10))
        self.label_alignment_camber.setMaximumSize(QSize(16777215, 20))
        self.label_alignment_camber.setFont(font1)
        self.label_alignment_camber.setAlignment(Qt.AlignCenter)

        self.gridLayout_castor_toe.addWidget(self.label_alignment_camber, 0, 1, 1, 2)

        self.label_alignment_toe = QLabel(self.tab_alignment)
        self.label_alignment_toe.setObjectName(u"label_alignment_toe")
        self.label_alignment_toe.setMinimumSize(QSize(40, 10))
        self.label_alignment_toe.setMaximumSize(QSize(16777215, 20))
        self.label_alignment_toe.setFont(font1)
        self.label_alignment_toe.setAlignment(Qt.AlignCenter)

        self.gridLayout_castor_toe.addWidget(self.label_alignment_toe, 0, 3, 1, 2)

        self.horizontalSlider_alignment_front_toe = QSlider(self.tab_alignment)
        self.horizontalSlider_alignment_front_toe.setObjectName(u"horizontalSlider_alignment_front_toe")
        sizePolicy.setHeightForWidth(self.horizontalSlider_alignment_front_toe.sizePolicy().hasHeightForWidth())
        self.horizontalSlider_alignment_front_toe.setSizePolicy(sizePolicy)
        self.horizontalSlider_alignment_front_toe.setMinimumSize(QSize(40, 10))
        self.horizontalSlider_alignment_front_toe.setMaximumSize(QSize(16777215, 20))
        self.horizontalSlider_alignment_front_toe.setMinimum(-10000)
        self.horizontalSlider_alignment_front_toe.setMaximum(10000)
        self.horizontalSlider_alignment_front_toe.setPageStep(1)
        self.horizontalSlider_alignment_front_toe.setValue(0)
        self.horizontalSlider_alignment_front_toe.setOrientation(Qt.Horizontal)

        self.gridLayout_castor_toe.addWidget(self.horizontalSlider_alignment_front_toe, 1, 3, 1, 1)

        self.label_alignment_rear = QLabel(self.tab_alignment)
        self.label_alignment_rear.setObjectName(u"label_alignment_rear")
        self.label_alignment_rear.setMinimumSize(QSize(40, 10))
        self.label_alignment_rear.setMaximumSize(QSize(50, 20))
        self.label_alignment_rear.setFont(font1)
        self.label_alignment_rear.setAlignment(Qt.AlignCenter)

        self.gridLayout_castor_toe.addWidget(self.label_alignment_rear, 2, 0, 1, 1)

        self.label_alignment_rear_toe_value = QLabel(self.tab_alignment)
        self.label_alignment_rear_toe_value.setObjectName(u"label_alignment_rear_toe_value")
        self.label_alignment_rear_toe_value.setMinimumSize(QSize(20, 10))
        self.label_alignment_rear_toe_value.setMaximumSize(QSize(30, 20))
        self.label_alignment_rear_toe_value.setFont(font1)
        self.label_alignment_rear_toe_value.setAlignment(Qt.AlignCenter)

        self.gridLayout_castor_toe.addWidget(self.label_alignment_rear_toe_value, 2, 4, 1, 1)

        self.label_alignment_rear_camber_value = QLabel(self.tab_alignment)
        self.label_alignment_rear_camber_value.setObjectName(u"label_alignment_rear_camber_value")
        self.label_alignment_rear_camber_value.setMinimumSize(QSize(20, 10))
        self.label_alignment_rear_camber_value.setMaximumSize(QSize(30, 20))
        self.label_alignment_rear_camber_value.setFont(font1)
        self.label_alignment_rear_camber_value.setAlignment(Qt.AlignCenter)

        self.gridLayout_castor_toe.addWidget(self.label_alignment_rear_camber_value, 2, 2, 1, 1)

        self.horizontalSlider_alignment_rear_toe = QSlider(self.tab_alignment)
        self.horizontalSlider_alignment_rear_toe.setObjectName(u"horizontalSlider_alignment_rear_toe")
        sizePolicy.setHeightForWidth(self.horizontalSlider_alignment_rear_toe.sizePolicy().hasHeightForWidth())
        self.horizontalSlider_alignment_rear_toe.setSizePolicy(sizePolicy)
        self.horizontalSlider_alignment_rear_toe.setMinimumSize(QSize(40, 10))
        self.horizontalSlider_alignment_rear_toe.setMaximumSize(QSize(16777215, 20))
        self.horizontalSlider_alignment_rear_toe.setMinimum(-10000)
        self.horizontalSlider_alignment_rear_toe.setMaximum(10000)
        self.horizontalSlider_alignment_rear_toe.setPageStep(1)
        self.horizontalSlider_alignment_rear_toe.setValue(0)
        self.horizontalSlider_alignment_rear_toe.setOrientation(Qt.Horizontal)

        self.gridLayout_castor_toe.addWidget(self.horizontalSlider_alignment_rear_toe, 2, 3, 1, 1)

        self.label_alignment_front_camber_value = QLabel(self.tab_alignment)
        self.label_alignment_front_camber_value.setObjectName(u"label_alignment_front_camber_value")
        self.label_alignment_front_camber_value.setMinimumSize(QSize(20, 10))
        self.label_alignment_front_camber_value.setMaximumSize(QSize(30, 20))
        self.label_alignment_front_camber_value.setFont(font1)
        self.label_alignment_front_camber_value.setAlignment(Qt.AlignCenter)

        self.gridLayout_castor_toe.addWidget(self.label_alignment_front_camber_value, 1, 2, 1, 1)

        self.label_alignment_front = QLabel(self.tab_alignment)
        self.label_alignment_front.setObjectName(u"label_alignment_front")
        self.label_alignment_front.setMinimumSize(QSize(40, 10))
        self.label_alignment_front.setMaximumSize(QSize(50, 20))
        self.label_alignment_front.setFont(font1)
        self.label_alignment_front.setAlignment(Qt.AlignCenter)

        self.gridLayout_castor_toe.addWidget(self.label_alignment_front, 1, 0, 1, 1)

        self.label_alignment_front_toe_value = QLabel(self.tab_alignment)
        self.label_alignment_front_toe_value.setObjectName(u"label_alignment_front_toe_value")
        self.label_alignment_front_toe_value.setMinimumSize(QSize(20, 10))
        self.label_alignment_front_toe_value.setMaximumSize(QSize(30, 20))
        self.label_alignment_front_toe_value.setFont(font1)
        self.label_alignment_front_toe_value.setAlignment(Qt.AlignCenter)

        self.gridLayout_castor_toe.addWidget(self.label_alignment_front_toe_value, 1, 4, 1, 1)

        self.label_alignment_side = QLabel(self.tab_alignment)
        self.label_alignment_side.setObjectName(u"label_alignment_side")
        self.label_alignment_side.setMinimumSize(QSize(30, 10))
        self.label_alignment_side.setMaximumSize(QSize(50, 20))
        self.label_alignment_side.setFont(font1)
        self.label_alignment_side.setAlignment(Qt.AlignCenter)

        self.gridLayout_castor_toe.addWidget(self.label_alignment_side, 0, 0, 1, 1)

        self.horizontalSlider_alignment_front_camber = QSlider(self.tab_alignment)
        self.horizontalSlider_alignment_front_camber.setObjectName(u"horizontalSlider_alignment_front_camber")
        sizePolicy.setHeightForWidth(self.horizontalSlider_alignment_front_camber.sizePolicy().hasHeightForWidth())
        self.horizontalSlider_alignment_front_camber.setSizePolicy(sizePolicy)
        self.horizontalSlider_alignment_front_camber.setMinimumSize(QSize(40, 10))
        self.horizontalSlider_alignment_front_camber.setMaximumSize(QSize(16777215, 20))
        self.horizontalSlider_alignment_front_camber.setMinimum(-10000)
        self.horizontalSlider_alignment_front_camber.setMaximum(10000)
        self.horizontalSlider_alignment_front_camber.setPageStep(1)
        self.horizontalSlider_alignment_front_camber.setValue(0)
        self.horizontalSlider_alignment_front_camber.setOrientation(Qt.Horizontal)
        self.horizontalSlider_alignment_front_camber.setInvertedAppearance(False)
        self.horizontalSlider_alignment_front_camber.setInvertedControls(False)
        self.horizontalSlider_alignment_front_camber.setTickPosition(QSlider.NoTicks)

        self.gridLayout_castor_toe.addWidget(self.horizontalSlider_alignment_front_camber, 1, 1, 1, 1)

        self.label_alignment_caster = QLabel(self.tab_alignment)
        self.label_alignment_caster.setObjectName(u"label_alignment_caster")
        self.label_alignment_caster.setMinimumSize(QSize(40, 10))
        self.label_alignment_caster.setMaximumSize(QSize(50, 20))
        self.label_alignment_caster.setFont(font1)
        self.label_alignment_caster.setAlignment(Qt.AlignCenter)

        self.gridLayout_castor_toe.addWidget(self.label_alignment_caster, 3, 0, 1, 1)

        self.label_alignment_front_caster_value = QLabel(self.tab_alignment)
        self.label_alignment_front_caster_value.setObjectName(u"label_alignment_front_caster_value")
        self.label_alignment_front_caster_value.setMinimumSize(QSize(20, 10))
        self.label_alignment_front_caster_value.setMaximumSize(QSize(30, 20))
        self.label_alignment_front_caster_value.setFont(font1)
        self.label_alignment_front_caster_value.setAlignment(Qt.AlignCenter)

        self.gridLayout_castor_toe.addWidget(self.label_alignment_front_caster_value, 3, 4, 1, 1)

        self.horizontalSlider_alignment_front_caster = QSlider(self.tab_alignment)
        self.horizontalSlider_alignment_front_caster.setObjectName(u"horizontalSlider_alignment_front_caster")
        sizePolicy.setHeightForWidth(self.horizontalSlider_alignment_front_caster.sizePolicy().hasHeightForWidth())
        self.horizontalSlider_alignment_front_caster.setSizePolicy(sizePolicy)
        self.horizontalSlider_alignment_front_caster.setMinimumSize(QSize(100, 10))
        self.horizontalSlider_alignment_front_caster.setMaximumSize(QSize(16777215, 20))
        self.horizontalSlider_alignment_front_caster.setMinimum(-10000)
        self.horizontalSlider_alignment_front_caster.setMaximum(10000)
        self.horizontalSlider_alignment_front_caster.setPageStep(1)
        self.horizontalSlider_alignment_front_caster.setValue(0)
        self.horizontalSlider_alignment_front_caster.setOrientation(Qt.Horizontal)

        self.gridLayout_castor_toe.addWidget(self.horizontalSlider_alignment_front_caster, 3, 1, 1, 3)


        self.gridLayout_4.addLayout(self.gridLayout_castor_toe, 1, 1, 1, 1)

        self.verticalSpacer_alignment_u = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.gridLayout_4.addItem(self.verticalSpacer_alignment_u, 0, 1, 1, 1)

        self.horizontalSpacer_alignment_l = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_alignment_l, 1, 0, 1, 1)

        self.horizontalSpacer_alignment_r = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_alignment_r, 1, 2, 1, 1)

        self.tabWidget.addTab(self.tab_alignment, "")
        self.tab_spring = QWidget()
        self.tab_spring.setObjectName(u"tab_spring")
        self.gridLayout_8 = QGridLayout(self.tab_spring)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_spring = QGridLayout()
        self.gridLayout_spring.setSpacing(15)
        self.gridLayout_spring.setObjectName(u"gridLayout_spring")
        self.gridLayout_spring.setContentsMargins(10, 10, 10, 10)
        self.label_spring_max = QLabel(self.tab_spring)
        self.label_spring_max.setObjectName(u"label_spring_max")
        self.label_spring_max.setMinimumSize(QSize(20, 15))
        self.label_spring_max.setMaximumSize(QSize(30, 25))
        self.label_spring_max.setFont(font1)
        self.label_spring_max.setAlignment(Qt.AlignCenter)

        self.gridLayout_spring.addWidget(self.label_spring_max, 1, 3, 1, 1, Qt.AlignHCenter)

        self.label_spring_min = QLabel(self.tab_spring)
        self.label_spring_min.setObjectName(u"label_spring_min")
        self.label_spring_min.setMinimumSize(QSize(20, 15))
        self.label_spring_min.setMaximumSize(QSize(30, 25))
        self.label_spring_min.setFont(font1)
        self.label_spring_min.setAlignment(Qt.AlignCenter)

        self.gridLayout_spring.addWidget(self.label_spring_min, 1, 2, 1, 1, Qt.AlignHCenter)

        self.line_spring_1 = QFrame(self.tab_spring)
        self.line_spring_1.setObjectName(u"line_spring_1")
        self.line_spring_1.setFrameShape(QFrame.Shape.HLine)
        self.line_spring_1.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_spring.addWidget(self.line_spring_1, 3, 0, 1, 4)

        self.label_spring_spring = QLabel(self.tab_spring)
        self.label_spring_spring.setObjectName(u"label_spring_spring")
        self.label_spring_spring.setMinimumSize(QSize(50, 15))
        self.label_spring_spring.setMaximumSize(QSize(16777215, 25))
        self.label_spring_spring.setFont(font1)
        self.label_spring_spring.setAlignment(Qt.AlignCenter)

        self.gridLayout_spring.addWidget(self.label_spring_spring, 0, 0, 1, 4)

        self.label_spring_rear = QLabel(self.tab_spring)
        self.label_spring_rear.setObjectName(u"label_spring_rear")
        sizePolicy.setHeightForWidth(self.label_spring_rear.sizePolicy().hasHeightForWidth())
        self.label_spring_rear.setSizePolicy(sizePolicy)
        self.label_spring_rear.setMinimumSize(QSize(30, 10))
        self.label_spring_rear.setMaximumSize(QSize(50, 25))
        self.label_spring_rear.setFont(font1)
        self.label_spring_rear.setAlignment(Qt.AlignCenter)

        self.gridLayout_spring.addWidget(self.label_spring_rear, 1, 1, 1, 1, Qt.AlignHCenter)

        self.label_spring_clearance = QLabel(self.tab_spring)
        self.label_spring_clearance.setObjectName(u"label_spring_clearance")
        sizePolicy.setHeightForWidth(self.label_spring_clearance.sizePolicy().hasHeightForWidth())
        self.label_spring_clearance.setSizePolicy(sizePolicy)
        self.label_spring_clearance.setMinimumSize(QSize(50, 15))
        self.label_spring_clearance.setMaximumSize(QSize(16777215, 25))
        self.label_spring_clearance.setFont(font1)
        self.label_spring_clearance.setAlignment(Qt.AlignCenter)

        self.gridLayout_spring.addWidget(self.label_spring_clearance, 4, 0, 1, 4)

        self.label_spring_front = QLabel(self.tab_spring)
        self.label_spring_front.setObjectName(u"label_spring_front")
        sizePolicy.setHeightForWidth(self.label_spring_front.sizePolicy().hasHeightForWidth())
        self.label_spring_front.setSizePolicy(sizePolicy)
        self.label_spring_front.setMinimumSize(QSize(30, 10))
        self.label_spring_front.setMaximumSize(QSize(50, 25))
        self.label_spring_front.setFont(font1)
        self.label_spring_front.setAlignment(Qt.AlignCenter)

        self.gridLayout_spring.addWidget(self.label_spring_front, 1, 0, 1, 1, Qt.AlignHCenter)

        self.doubleSpinBox_spring_front = QDoubleSpinBox(self.tab_spring)
        self.doubleSpinBox_spring_front.setObjectName(u"doubleSpinBox_spring_front")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_spring_front.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_spring_front.setSizePolicy(sizePolicy)
        self.doubleSpinBox_spring_front.setMinimumSize(QSize(70, 15))
        self.doubleSpinBox_spring_front.setMaximumSize(QSize(16777215, 25))
        self.doubleSpinBox_spring_front.setFont(font1)
        self.doubleSpinBox_spring_front.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_spring_front.setDecimals(1)
        self.doubleSpinBox_spring_front.setMinimum(-10000.000000000000000)
        self.doubleSpinBox_spring_front.setMaximum(10000.000000000000000)

        self.gridLayout_spring.addWidget(self.doubleSpinBox_spring_front, 2, 0, 1, 1)

        self.doubleSpinBox_spring_rear = QDoubleSpinBox(self.tab_spring)
        self.doubleSpinBox_spring_rear.setObjectName(u"doubleSpinBox_spring_rear")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_spring_rear.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_spring_rear.setSizePolicy(sizePolicy)
        self.doubleSpinBox_spring_rear.setMinimumSize(QSize(70, 15))
        self.doubleSpinBox_spring_rear.setMaximumSize(QSize(16777215, 25))
        self.doubleSpinBox_spring_rear.setFont(font1)
        self.doubleSpinBox_spring_rear.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_spring_rear.setDecimals(1)
        self.doubleSpinBox_spring_rear.setMinimum(-10000.000000000000000)
        self.doubleSpinBox_spring_rear.setMaximum(10000.000000000000000)

        self.gridLayout_spring.addWidget(self.doubleSpinBox_spring_rear, 2, 1, 1, 1)

        self.doubleSpinBox_spring_min = QDoubleSpinBox(self.tab_spring)
        self.doubleSpinBox_spring_min.setObjectName(u"doubleSpinBox_spring_min")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_spring_min.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_spring_min.setSizePolicy(sizePolicy)
        self.doubleSpinBox_spring_min.setMinimumSize(QSize(70, 15))
        self.doubleSpinBox_spring_min.setMaximumSize(QSize(16777215, 25))
        self.doubleSpinBox_spring_min.setFont(font1)
        self.doubleSpinBox_spring_min.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_spring_min.setDecimals(1)
        self.doubleSpinBox_spring_min.setMinimum(-10000.000000000000000)
        self.doubleSpinBox_spring_min.setMaximum(10000.000000000000000)

        self.gridLayout_spring.addWidget(self.doubleSpinBox_spring_min, 2, 2, 1, 1)

        self.doubleSpinBox_spring_max = QDoubleSpinBox(self.tab_spring)
        self.doubleSpinBox_spring_max.setObjectName(u"doubleSpinBox_spring_max")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_spring_max.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_spring_max.setSizePolicy(sizePolicy)
        self.doubleSpinBox_spring_max.setMinimumSize(QSize(70, 15))
        self.doubleSpinBox_spring_max.setMaximumSize(QSize(16777215, 25))
        self.doubleSpinBox_spring_max.setFont(font1)
        self.doubleSpinBox_spring_max.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_spring_max.setDecimals(1)
        self.doubleSpinBox_spring_max.setMinimum(-10000.000000000000000)
        self.doubleSpinBox_spring_max.setMaximum(10000.000000000000000)

        self.gridLayout_spring.addWidget(self.doubleSpinBox_spring_max, 2, 3, 1, 1)

        self.doubleSpinBox_clearance_front = QDoubleSpinBox(self.tab_spring)
        self.doubleSpinBox_clearance_front.setObjectName(u"doubleSpinBox_clearance_front")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_clearance_front.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_clearance_front.setSizePolicy(sizePolicy)
        self.doubleSpinBox_clearance_front.setMinimumSize(QSize(70, 15))
        self.doubleSpinBox_clearance_front.setMaximumSize(QSize(16777215, 25))
        self.doubleSpinBox_clearance_front.setFont(font1)
        self.doubleSpinBox_clearance_front.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_clearance_front.setDecimals(1)
        self.doubleSpinBox_clearance_front.setMinimum(-10000.000000000000000)
        self.doubleSpinBox_clearance_front.setMaximum(10000.000000000000000)

        self.gridLayout_spring.addWidget(self.doubleSpinBox_clearance_front, 5, 0, 1, 1)

        self.doubleSpinBox_clearance_rear = QDoubleSpinBox(self.tab_spring)
        self.doubleSpinBox_clearance_rear.setObjectName(u"doubleSpinBox_clearance_rear")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_clearance_rear.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_clearance_rear.setSizePolicy(sizePolicy)
        self.doubleSpinBox_clearance_rear.setMinimumSize(QSize(70, 15))
        self.doubleSpinBox_clearance_rear.setMaximumSize(QSize(16777215, 25))
        self.doubleSpinBox_clearance_rear.setFont(font1)
        self.doubleSpinBox_clearance_rear.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_clearance_rear.setDecimals(1)
        self.doubleSpinBox_clearance_rear.setMinimum(-10000.000000000000000)
        self.doubleSpinBox_clearance_rear.setMaximum(10000.000000000000000)

        self.gridLayout_spring.addWidget(self.doubleSpinBox_clearance_rear, 5, 1, 1, 1)

        self.doubleSpinBox_clearance_min = QDoubleSpinBox(self.tab_spring)
        self.doubleSpinBox_clearance_min.setObjectName(u"doubleSpinBox_clearance_min")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_clearance_min.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_clearance_min.setSizePolicy(sizePolicy)
        self.doubleSpinBox_clearance_min.setMinimumSize(QSize(70, 15))
        self.doubleSpinBox_clearance_min.setMaximumSize(QSize(16777215, 25))
        self.doubleSpinBox_clearance_min.setFont(font1)
        self.doubleSpinBox_clearance_min.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_clearance_min.setDecimals(1)
        self.doubleSpinBox_clearance_min.setMinimum(-10000.000000000000000)
        self.doubleSpinBox_clearance_min.setMaximum(10000.000000000000000)

        self.gridLayout_spring.addWidget(self.doubleSpinBox_clearance_min, 5, 2, 1, 1)

        self.doubleSpinBox_clearance_max = QDoubleSpinBox(self.tab_spring)
        self.doubleSpinBox_clearance_max.setObjectName(u"doubleSpinBox_clearance_max")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_clearance_max.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_clearance_max.setSizePolicy(sizePolicy)
        self.doubleSpinBox_clearance_max.setMinimumSize(QSize(70, 15))
        self.doubleSpinBox_clearance_max.setMaximumSize(QSize(16777215, 25))
        self.doubleSpinBox_clearance_max.setFont(font1)
        self.doubleSpinBox_clearance_max.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_clearance_max.setDecimals(1)
        self.doubleSpinBox_clearance_max.setMinimum(-10000.000000000000000)
        self.doubleSpinBox_clearance_max.setMaximum(10000.000000000000000)

        self.gridLayout_spring.addWidget(self.doubleSpinBox_clearance_max, 5, 3, 1, 1)


        self.gridLayout_8.addLayout(self.gridLayout_spring, 1, 1, 1, 1)

        self.verticalSpacer_spring_u = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.gridLayout_8.addItem(self.verticalSpacer_spring_u, 0, 1, 1, 1)

        self.horizontalSpacer_spring_l = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_spring_l, 1, 0, 1, 1)

        self.horizontalSpacer_spring_r = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_spring_r, 1, 2, 1, 1)

        self.verticalSpacer_spring_d = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.gridLayout_8.addItem(self.verticalSpacer_spring_d, 2, 1, 1, 1)

        self.tabWidget.addTab(self.tab_spring, "")
        self.tab_damping = QWidget()
        self.tab_damping.setObjectName(u"tab_damping")
        self.gridLayout_2 = QGridLayout(self.tab_damping)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_main_damping = QGridLayout()
        self.gridLayout_main_damping.setObjectName(u"gridLayout_main_damping")
        self.gridLayout_main_damping.setHorizontalSpacing(15)
        self.gridLayout_main_damping.setVerticalSpacing(10)
        self.gridLayout_main_damping.setContentsMargins(10, 10, 10, 10)
        self.label_damping_rear = QLabel(self.tab_damping)
        self.label_damping_rear.setObjectName(u"label_damping_rear")
        self.label_damping_rear.setMinimumSize(QSize(50, 15))
        self.label_damping_rear.setMaximumSize(QSize(16777215, 25))
        self.label_damping_rear.setFont(font1)
        self.label_damping_rear.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_damping.addWidget(self.label_damping_rear, 2, 2, 1, 1)

        self.label_damping_front = QLabel(self.tab_damping)
        self.label_damping_front.setObjectName(u"label_damping_front")
        self.label_damping_front.setMinimumSize(QSize(50, 15))
        self.label_damping_front.setMaximumSize(QSize(16777215, 25))
        self.label_damping_front.setFont(font1)
        self.label_damping_front.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_damping.addWidget(self.label_damping_front, 2, 1, 1, 1)

        self.label_damping_min = QLabel(self.tab_damping)
        self.label_damping_min.setObjectName(u"label_damping_min")
        self.label_damping_min.setMinimumSize(QSize(50, 15))
        self.label_damping_min.setMaximumSize(QSize(16777215, 25))
        self.label_damping_min.setFont(font1)
        self.label_damping_min.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_damping.addWidget(self.label_damping_min, 2, 3, 1, 1)

        self.label_damping_max = QLabel(self.tab_damping)
        self.label_damping_max.setObjectName(u"label_damping_max")
        self.label_damping_max.setMinimumSize(QSize(50, 15))
        self.label_damping_max.setMaximumSize(QSize(16777215, 25))
        self.label_damping_max.setFont(font1)
        self.label_damping_max.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_damping.addWidget(self.label_damping_max, 2, 4, 1, 1)

        self.label_damping_Damping = QLabel(self.tab_damping)
        self.label_damping_Damping.setObjectName(u"label_damping_Damping")
        self.label_damping_Damping.setMinimumSize(QSize(50, 15))
        self.label_damping_Damping.setMaximumSize(QSize(16777215, 25))
        self.label_damping_Damping.setFont(font1)
        self.label_damping_Damping.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_damping.addWidget(self.label_damping_Damping, 0, 0, 1, 5)

        self.line_damping_1 = QFrame(self.tab_damping)
        self.line_damping_1.setObjectName(u"line_damping_1")
        self.line_damping_1.setFrameShape(QFrame.Shape.HLine)
        self.line_damping_1.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_main_damping.addWidget(self.line_damping_1, 1, 0, 1, 5)

        self.label_damping_rebound = QLabel(self.tab_damping)
        self.label_damping_rebound.setObjectName(u"label_damping_rebound")
        self.label_damping_rebound.setMinimumSize(QSize(60, 15))
        self.label_damping_rebound.setMaximumSize(QSize(80, 25))
        self.label_damping_rebound.setFont(font1)
        self.label_damping_rebound.setTextFormat(Qt.AutoText)
        self.label_damping_rebound.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_damping.addWidget(self.label_damping_rebound, 3, 0, 1, 1)

        self.label_damping_bump = QLabel(self.tab_damping)
        self.label_damping_bump.setObjectName(u"label_damping_bump")
        self.label_damping_bump.setMinimumSize(QSize(60, 15))
        self.label_damping_bump.setMaximumSize(QSize(80, 25))
        self.label_damping_bump.setFont(font1)
        self.label_damping_bump.setTextFormat(Qt.AutoText)
        self.label_damping_bump.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_damping.addWidget(self.label_damping_bump, 4, 0, 1, 1)

        self.doubleSpinBox_damping_rebound_max = QDoubleSpinBox(self.tab_damping)
        self.doubleSpinBox_damping_rebound_max.setObjectName(u"doubleSpinBox_damping_rebound_max")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_damping_rebound_max.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_damping_rebound_max.setSizePolicy(sizePolicy)
        self.doubleSpinBox_damping_rebound_max.setMinimumSize(QSize(70, 10))
        self.doubleSpinBox_damping_rebound_max.setMaximumSize(QSize(16777215, 20))
        self.doubleSpinBox_damping_rebound_max.setFont(font1)
        self.doubleSpinBox_damping_rebound_max.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_damping_rebound_max.setDecimals(1)
        self.doubleSpinBox_damping_rebound_max.setMinimum(-10000.000000000000000)
        self.doubleSpinBox_damping_rebound_max.setMaximum(10000.000000000000000)

        self.gridLayout_main_damping.addWidget(self.doubleSpinBox_damping_rebound_max, 3, 4, 1, 1)

        self.doubleSpinBox_damping_bump_max = QDoubleSpinBox(self.tab_damping)
        self.doubleSpinBox_damping_bump_max.setObjectName(u"doubleSpinBox_damping_bump_max")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_damping_bump_max.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_damping_bump_max.setSizePolicy(sizePolicy)
        self.doubleSpinBox_damping_bump_max.setMinimumSize(QSize(70, 10))
        self.doubleSpinBox_damping_bump_max.setMaximumSize(QSize(16777215, 20))
        self.doubleSpinBox_damping_bump_max.setFont(font1)
        self.doubleSpinBox_damping_bump_max.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_damping_bump_max.setDecimals(1)
        self.doubleSpinBox_damping_bump_max.setMinimum(-10000.000000000000000)
        self.doubleSpinBox_damping_bump_max.setMaximum(10000.000000000000000)

        self.gridLayout_main_damping.addWidget(self.doubleSpinBox_damping_bump_max, 4, 4, 1, 1)

        self.doubleSpinBox_damping_bump_min = QDoubleSpinBox(self.tab_damping)
        self.doubleSpinBox_damping_bump_min.setObjectName(u"doubleSpinBox_damping_bump_min")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_damping_bump_min.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_damping_bump_min.setSizePolicy(sizePolicy)
        self.doubleSpinBox_damping_bump_min.setMinimumSize(QSize(70, 10))
        self.doubleSpinBox_damping_bump_min.setMaximumSize(QSize(16777215, 20))
        self.doubleSpinBox_damping_bump_min.setFont(font1)
        self.doubleSpinBox_damping_bump_min.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_damping_bump_min.setDecimals(1)
        self.doubleSpinBox_damping_bump_min.setMinimum(-10000.000000000000000)
        self.doubleSpinBox_damping_bump_min.setMaximum(10000.000000000000000)

        self.gridLayout_main_damping.addWidget(self.doubleSpinBox_damping_bump_min, 4, 3, 1, 1)

        self.doubleSpinBox_damping_rebound_min = QDoubleSpinBox(self.tab_damping)
        self.doubleSpinBox_damping_rebound_min.setObjectName(u"doubleSpinBox_damping_rebound_min")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_damping_rebound_min.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_damping_rebound_min.setSizePolicy(sizePolicy)
        self.doubleSpinBox_damping_rebound_min.setMinimumSize(QSize(70, 10))
        self.doubleSpinBox_damping_rebound_min.setMaximumSize(QSize(16777215, 20))
        self.doubleSpinBox_damping_rebound_min.setFont(font1)
        self.doubleSpinBox_damping_rebound_min.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_damping_rebound_min.setDecimals(1)
        self.doubleSpinBox_damping_rebound_min.setMinimum(-10000.000000000000000)
        self.doubleSpinBox_damping_rebound_min.setMaximum(10000.000000000000000)

        self.gridLayout_main_damping.addWidget(self.doubleSpinBox_damping_rebound_min, 3, 3, 1, 1)

        self.doubleSpinBox_damping_rebound_rear = QDoubleSpinBox(self.tab_damping)
        self.doubleSpinBox_damping_rebound_rear.setObjectName(u"doubleSpinBox_damping_rebound_rear")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_damping_rebound_rear.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_damping_rebound_rear.setSizePolicy(sizePolicy)
        self.doubleSpinBox_damping_rebound_rear.setMinimumSize(QSize(70, 10))
        self.doubleSpinBox_damping_rebound_rear.setMaximumSize(QSize(16777215, 20))
        self.doubleSpinBox_damping_rebound_rear.setFont(font1)
        self.doubleSpinBox_damping_rebound_rear.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_damping_rebound_rear.setDecimals(1)
        self.doubleSpinBox_damping_rebound_rear.setMinimum(-10000.000000000000000)
        self.doubleSpinBox_damping_rebound_rear.setMaximum(10000.000000000000000)

        self.gridLayout_main_damping.addWidget(self.doubleSpinBox_damping_rebound_rear, 3, 2, 1, 1)

        self.doubleSpinBox_damping_bump_rear = QDoubleSpinBox(self.tab_damping)
        self.doubleSpinBox_damping_bump_rear.setObjectName(u"doubleSpinBox_damping_bump_rear")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_damping_bump_rear.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_damping_bump_rear.setSizePolicy(sizePolicy)
        self.doubleSpinBox_damping_bump_rear.setMinimumSize(QSize(70, 10))
        self.doubleSpinBox_damping_bump_rear.setMaximumSize(QSize(16777215, 20))
        self.doubleSpinBox_damping_bump_rear.setFont(font1)
        self.doubleSpinBox_damping_bump_rear.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_damping_bump_rear.setDecimals(1)
        self.doubleSpinBox_damping_bump_rear.setMinimum(-10000.000000000000000)
        self.doubleSpinBox_damping_bump_rear.setMaximum(10000.000000000000000)

        self.gridLayout_main_damping.addWidget(self.doubleSpinBox_damping_bump_rear, 4, 2, 1, 1)

        self.doubleSpinBox_damping_rebound_front = QDoubleSpinBox(self.tab_damping)
        self.doubleSpinBox_damping_rebound_front.setObjectName(u"doubleSpinBox_damping_rebound_front")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_damping_rebound_front.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_damping_rebound_front.setSizePolicy(sizePolicy)
        self.doubleSpinBox_damping_rebound_front.setMinimumSize(QSize(70, 10))
        self.doubleSpinBox_damping_rebound_front.setMaximumSize(QSize(16777215, 20))
        self.doubleSpinBox_damping_rebound_front.setFont(font1)
        self.doubleSpinBox_damping_rebound_front.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_damping_rebound_front.setDecimals(1)
        self.doubleSpinBox_damping_rebound_front.setMinimum(-10000.000000000000000)
        self.doubleSpinBox_damping_rebound_front.setMaximum(10000.000000000000000)

        self.gridLayout_main_damping.addWidget(self.doubleSpinBox_damping_rebound_front, 3, 1, 1, 1)

        self.doubleSpinBox_damping_bump_front = QDoubleSpinBox(self.tab_damping)
        self.doubleSpinBox_damping_bump_front.setObjectName(u"doubleSpinBox_damping_bump_front")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_damping_bump_front.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_damping_bump_front.setSizePolicy(sizePolicy)
        self.doubleSpinBox_damping_bump_front.setMinimumSize(QSize(70, 10))
        self.doubleSpinBox_damping_bump_front.setMaximumSize(QSize(16777215, 20))
        self.doubleSpinBox_damping_bump_front.setFont(font1)
        self.doubleSpinBox_damping_bump_front.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_damping_bump_front.setDecimals(1)
        self.doubleSpinBox_damping_bump_front.setMinimum(-10000.000000000000000)
        self.doubleSpinBox_damping_bump_front.setMaximum(10000.000000000000000)

        self.gridLayout_main_damping.addWidget(self.doubleSpinBox_damping_bump_front, 4, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_main_damping, 1, 1, 1, 1)

        self.verticalSpacer_damping_d = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.gridLayout_2.addItem(self.verticalSpacer_damping_d, 2, 1, 1, 1)

        self.verticalSpacer_damping_u = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.gridLayout_2.addItem(self.verticalSpacer_damping_u, 0, 1, 1, 1)

        self.horizontalSpacer_damping_r = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_damping_r, 1, 2, 1, 1)

        self.horizontalSpacer_damping_l = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_damping_l, 1, 0, 1, 1)

        self.tabWidget.addTab(self.tab_damping, "")
        self.tab_roll_bar = QWidget()
        self.tab_roll_bar.setObjectName(u"tab_roll_bar")
        self.gridLayout_10 = QGridLayout(self.tab_roll_bar)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_roll_bar = QGridLayout()
        self.gridLayout_roll_bar.setSpacing(10)
        self.gridLayout_roll_bar.setObjectName(u"gridLayout_roll_bar")
        self.gridLayout_roll_bar.setContentsMargins(5, 10, 5, 10)
        self.label_roll_bar_max = QLabel(self.tab_roll_bar)
        self.label_roll_bar_max.setObjectName(u"label_roll_bar_max")
        self.label_roll_bar_max.setMinimumSize(QSize(10, 10))
        self.label_roll_bar_max.setMaximumSize(QSize(20, 20))
        self.label_roll_bar_max.setFont(font)
        self.label_roll_bar_max.setAlignment(Qt.AlignCenter)

        self.gridLayout_roll_bar.addWidget(self.label_roll_bar_max, 0, 3, 1, 1)

        self.horizontalSpacer_roll_bar = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_roll_bar.addItem(self.horizontalSpacer_roll_bar, 0, 2, 1, 1)

        self.label_roll_bar_front = QLabel(self.tab_roll_bar)
        self.label_roll_bar_front.setObjectName(u"label_roll_bar_front")
        self.label_roll_bar_front.setMinimumSize(QSize(50, 10))
        self.label_roll_bar_front.setMaximumSize(QSize(60, 20))
        self.label_roll_bar_front.setFont(font)
        self.label_roll_bar_front.setAlignment(Qt.AlignCenter)

        self.gridLayout_roll_bar.addWidget(self.label_roll_bar_front, 1, 0, 1, 1)

        self.label_roll_bar_rear = QLabel(self.tab_roll_bar)
        self.label_roll_bar_rear.setObjectName(u"label_roll_bar_rear")
        self.label_roll_bar_rear.setMinimumSize(QSize(50, 10))
        self.label_roll_bar_rear.setMaximumSize(QSize(60, 20))
        self.label_roll_bar_rear.setFont(font)
        self.label_roll_bar_rear.setAlignment(Qt.AlignCenter)

        self.gridLayout_roll_bar.addWidget(self.label_roll_bar_rear, 2, 0, 1, 1)

        self.label_roll_bar_side = QLabel(self.tab_roll_bar)
        self.label_roll_bar_side.setObjectName(u"label_roll_bar_side")
        self.label_roll_bar_side.setMinimumSize(QSize(50, 10))
        self.label_roll_bar_side.setMaximumSize(QSize(60, 20))
        self.label_roll_bar_side.setFont(font)
        self.label_roll_bar_side.setAlignment(Qt.AlignCenter)

        self.gridLayout_roll_bar.addWidget(self.label_roll_bar_side, 0, 0, 1, 1)

        self.label_roll_bar_min = QLabel(self.tab_roll_bar)
        self.label_roll_bar_min.setObjectName(u"label_roll_bar_min")
        self.label_roll_bar_min.setMinimumSize(QSize(10, 10))
        self.label_roll_bar_min.setMaximumSize(QSize(20, 20))
        self.label_roll_bar_min.setFont(font)
        self.label_roll_bar_min.setAlignment(Qt.AlignCenter)

        self.gridLayout_roll_bar.addWidget(self.label_roll_bar_min, 0, 1, 1, 1)

        self.label_roll_bar_unit = QLabel(self.tab_roll_bar)
        self.label_roll_bar_unit.setObjectName(u"label_roll_bar_unit")
        self.label_roll_bar_unit.setMinimumSize(QSize(50, 10))
        self.label_roll_bar_unit.setMaximumSize(QSize(60, 20))
        self.label_roll_bar_unit.setFont(font1)
        self.label_roll_bar_unit.setAlignment(Qt.AlignCenter)

        self.gridLayout_roll_bar.addWidget(self.label_roll_bar_unit, 0, 4, 1, 1)

        self.label_roll_bar_front_value = QLabel(self.tab_roll_bar)
        self.label_roll_bar_front_value.setObjectName(u"label_roll_bar_front_value")
        self.label_roll_bar_front_value.setMinimumSize(QSize(50, 10))
        self.label_roll_bar_front_value.setMaximumSize(QSize(60, 20))
        self.label_roll_bar_front_value.setFont(font1)
        self.label_roll_bar_front_value.setAlignment(Qt.AlignCenter)

        self.gridLayout_roll_bar.addWidget(self.label_roll_bar_front_value, 1, 4, 1, 1)

        self.label_roll_bar_rear_value = QLabel(self.tab_roll_bar)
        self.label_roll_bar_rear_value.setObjectName(u"label_roll_bar_rear_value")
        self.label_roll_bar_rear_value.setMinimumSize(QSize(50, 10))
        self.label_roll_bar_rear_value.setMaximumSize(QSize(60, 20))
        self.label_roll_bar_rear_value.setFont(font1)
        self.label_roll_bar_rear_value.setAlignment(Qt.AlignCenter)

        self.gridLayout_roll_bar.addWidget(self.label_roll_bar_rear_value, 2, 4, 1, 1)

        self.horizontalSlider_roll_bar_front = QSlider(self.tab_roll_bar)
        self.horizontalSlider_roll_bar_front.setObjectName(u"horizontalSlider_roll_bar_front")
        sizePolicy.setHeightForWidth(self.horizontalSlider_roll_bar_front.sizePolicy().hasHeightForWidth())
        self.horizontalSlider_roll_bar_front.setSizePolicy(sizePolicy)
        self.horizontalSlider_roll_bar_front.setMinimumSize(QSize(120, 15))
        self.horizontalSlider_roll_bar_front.setMaximumSize(QSize(16777215, 20))
        self.horizontalSlider_roll_bar_front.setMinimum(-10000)
        self.horizontalSlider_roll_bar_front.setMaximum(10000)
        self.horizontalSlider_roll_bar_front.setSingleStep(1)
        self.horizontalSlider_roll_bar_front.setPageStep(1)
        self.horizontalSlider_roll_bar_front.setValue(0)
        self.horizontalSlider_roll_bar_front.setOrientation(Qt.Horizontal)

        self.gridLayout_roll_bar.addWidget(self.horizontalSlider_roll_bar_front, 1, 1, 1, 3)

        self.horizontalSlider_roll_bar_rear = QSlider(self.tab_roll_bar)
        self.horizontalSlider_roll_bar_rear.setObjectName(u"horizontalSlider_roll_bar_rear")
        sizePolicy.setHeightForWidth(self.horizontalSlider_roll_bar_rear.sizePolicy().hasHeightForWidth())
        self.horizontalSlider_roll_bar_rear.setSizePolicy(sizePolicy)
        self.horizontalSlider_roll_bar_rear.setMinimumSize(QSize(120, 15))
        self.horizontalSlider_roll_bar_rear.setMaximumSize(QSize(16777215, 20))
        self.horizontalSlider_roll_bar_rear.setMinimum(-10000)
        self.horizontalSlider_roll_bar_rear.setMaximum(10000)
        self.horizontalSlider_roll_bar_rear.setPageStep(1)
        self.horizontalSlider_roll_bar_rear.setValue(0)
        self.horizontalSlider_roll_bar_rear.setOrientation(Qt.Horizontal)

        self.gridLayout_roll_bar.addWidget(self.horizontalSlider_roll_bar_rear, 2, 1, 1, 3)


        self.gridLayout_10.addLayout(self.gridLayout_roll_bar, 0, 0, 1, 1)

        self.verticalSpacer_roll_bar = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_10.addItem(self.verticalSpacer_roll_bar, 1, 0, 1, 1)

        self.tabWidget.addTab(self.tab_roll_bar, "")
        self.tab_aero = QWidget()
        self.tab_aero.setObjectName(u"tab_aero")
        self.gridLayout_11 = QGridLayout(self.tab_aero)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.verticalSpacer_aero_d = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_11.addItem(self.verticalSpacer_aero_d, 2, 1, 1, 1)

        self.gridLayout_main_aero = QGridLayout()
        self.gridLayout_main_aero.setObjectName(u"gridLayout_main_aero")
        self.gridLayout_main_aero.setHorizontalSpacing(20)
        self.gridLayout_main_aero.setVerticalSpacing(10)
        self.gridLayout_main_aero.setContentsMargins(10, 10, 10, 10)
        self.label_aero_min = QLabel(self.tab_aero)
        self.label_aero_min.setObjectName(u"label_aero_min")
        self.label_aero_min.setMinimumSize(QSize(60, 10))
        self.label_aero_min.setMaximumSize(QSize(80, 20))
        self.label_aero_min.setFont(font1)
        self.label_aero_min.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_aero.addWidget(self.label_aero_min, 0, 2, 1, 1)

        self.spinBox_aero_rear = QSpinBox(self.tab_aero)
        self.spinBox_aero_rear.setObjectName(u"spinBox_aero_rear")
        sizePolicy.setHeightForWidth(self.spinBox_aero_rear.sizePolicy().hasHeightForWidth())
        self.spinBox_aero_rear.setSizePolicy(sizePolicy)
        self.spinBox_aero_rear.setMinimumSize(QSize(50, 15))
        self.spinBox_aero_rear.setMaximumSize(QSize(70, 25))
        self.spinBox_aero_rear.setMinimum(-10000)
        self.spinBox_aero_rear.setMaximum(10000)
        self.spinBox_aero_rear.setValue(0)

        self.gridLayout_main_aero.addWidget(self.spinBox_aero_rear, 2, 1, 1, 1, Qt.AlignHCenter)

        self.spinBox_aero_front = QSpinBox(self.tab_aero)
        self.spinBox_aero_front.setObjectName(u"spinBox_aero_front")
        sizePolicy.setHeightForWidth(self.spinBox_aero_front.sizePolicy().hasHeightForWidth())
        self.spinBox_aero_front.setSizePolicy(sizePolicy)
        self.spinBox_aero_front.setMinimumSize(QSize(50, 15))
        self.spinBox_aero_front.setMaximumSize(QSize(70, 25))
        self.spinBox_aero_front.setMinimum(-10000)
        self.spinBox_aero_front.setMaximum(10000)
        self.spinBox_aero_front.setValue(0)

        self.gridLayout_main_aero.addWidget(self.spinBox_aero_front, 1, 1, 1, 1, Qt.AlignHCenter)

        self.spinBox_aero_front_min = QSpinBox(self.tab_aero)
        self.spinBox_aero_front_min.setObjectName(u"spinBox_aero_front_min")
        sizePolicy.setHeightForWidth(self.spinBox_aero_front_min.sizePolicy().hasHeightForWidth())
        self.spinBox_aero_front_min.setSizePolicy(sizePolicy)
        self.spinBox_aero_front_min.setMinimumSize(QSize(50, 15))
        self.spinBox_aero_front_min.setMaximumSize(QSize(70, 25))
        self.spinBox_aero_front_min.setMinimum(-10000)
        self.spinBox_aero_front_min.setMaximum(10000)
        self.spinBox_aero_front_min.setValue(0)

        self.gridLayout_main_aero.addWidget(self.spinBox_aero_front_min, 1, 2, 1, 1, Qt.AlignHCenter)

        self.spinBox_aero_rear_min = QSpinBox(self.tab_aero)
        self.spinBox_aero_rear_min.setObjectName(u"spinBox_aero_rear_min")
        sizePolicy.setHeightForWidth(self.spinBox_aero_rear_min.sizePolicy().hasHeightForWidth())
        self.spinBox_aero_rear_min.setSizePolicy(sizePolicy)
        self.spinBox_aero_rear_min.setMinimumSize(QSize(50, 15))
        self.spinBox_aero_rear_min.setMaximumSize(QSize(70, 25))
        self.spinBox_aero_rear_min.setMinimum(-10000)
        self.spinBox_aero_rear_min.setMaximum(10000)
        self.spinBox_aero_rear_min.setValue(0)

        self.gridLayout_main_aero.addWidget(self.spinBox_aero_rear_min, 2, 2, 1, 1, Qt.AlignHCenter)

        self.spinBox_aero_front_max = QSpinBox(self.tab_aero)
        self.spinBox_aero_front_max.setObjectName(u"spinBox_aero_front_max")
        sizePolicy.setHeightForWidth(self.spinBox_aero_front_max.sizePolicy().hasHeightForWidth())
        self.spinBox_aero_front_max.setSizePolicy(sizePolicy)
        self.spinBox_aero_front_max.setMinimumSize(QSize(50, 15))
        self.spinBox_aero_front_max.setMaximumSize(QSize(70, 25))
        self.spinBox_aero_front_max.setMinimum(-10000)
        self.spinBox_aero_front_max.setMaximum(10000)
        self.spinBox_aero_front_max.setValue(0)

        self.gridLayout_main_aero.addWidget(self.spinBox_aero_front_max, 1, 3, 1, 1, Qt.AlignHCenter)

        self.label_aero = QLabel(self.tab_aero)
        self.label_aero.setObjectName(u"label_aero")
        self.label_aero.setMinimumSize(QSize(60, 10))
        self.label_aero.setMaximumSize(QSize(80, 20))
        self.label_aero.setFont(font1)
        self.label_aero.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_aero.addWidget(self.label_aero, 0, 1, 1, 1)

        self.label_aero_max = QLabel(self.tab_aero)
        self.label_aero_max.setObjectName(u"label_aero_max")
        self.label_aero_max.setMinimumSize(QSize(60, 10))
        self.label_aero_max.setMaximumSize(QSize(80, 20))
        self.label_aero_max.setFont(font1)
        self.label_aero_max.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_aero.addWidget(self.label_aero_max, 0, 3, 1, 1)

        self.checkBox_aero_front = QCheckBox(self.tab_aero)
        self.checkBox_aero_front.setObjectName(u"checkBox_aero_front")
        sizePolicy.setHeightForWidth(self.checkBox_aero_front.sizePolicy().hasHeightForWidth())
        self.checkBox_aero_front.setSizePolicy(sizePolicy)
        self.checkBox_aero_front.setMinimumSize(QSize(60, 15))
        self.checkBox_aero_front.setMaximumSize(QSize(80, 25))
        self.checkBox_aero_front.setFont(font1)
        self.checkBox_aero_front.setLayoutDirection(Qt.LeftToRight)
        self.checkBox_aero_front.setAutoFillBackground(False)
        self.checkBox_aero_front.setAutoRepeat(False)
        self.checkBox_aero_front.setAutoExclusive(False)
        self.checkBox_aero_front.setTristate(False)

        self.gridLayout_main_aero.addWidget(self.checkBox_aero_front, 1, 0, 1, 1)

        self.checkBox_aero_rear = QCheckBox(self.tab_aero)
        self.checkBox_aero_rear.setObjectName(u"checkBox_aero_rear")
        sizePolicy.setHeightForWidth(self.checkBox_aero_rear.sizePolicy().hasHeightForWidth())
        self.checkBox_aero_rear.setSizePolicy(sizePolicy)
        self.checkBox_aero_rear.setMinimumSize(QSize(60, 15))
        self.checkBox_aero_rear.setMaximumSize(QSize(80, 25))
        self.checkBox_aero_rear.setFont(font1)

        self.gridLayout_main_aero.addWidget(self.checkBox_aero_rear, 2, 0, 1, 1)

        self.spinBox_aero_rear_max = QSpinBox(self.tab_aero)
        self.spinBox_aero_rear_max.setObjectName(u"spinBox_aero_rear_max")
        sizePolicy.setHeightForWidth(self.spinBox_aero_rear_max.sizePolicy().hasHeightForWidth())
        self.spinBox_aero_rear_max.setSizePolicy(sizePolicy)
        self.spinBox_aero_rear_max.setMinimumSize(QSize(50, 15))
        self.spinBox_aero_rear_max.setMaximumSize(QSize(70, 25))
        self.spinBox_aero_rear_max.setMinimum(-10000)
        self.spinBox_aero_rear_max.setMaximum(10000)
        self.spinBox_aero_rear_max.setValue(0)

        self.gridLayout_main_aero.addWidget(self.spinBox_aero_rear_max, 2, 3, 1, 1, Qt.AlignHCenter)


        self.gridLayout_11.addLayout(self.gridLayout_main_aero, 1, 1, 1, 1)

        self.verticalSpacer_aero_u = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.gridLayout_11.addItem(self.verticalSpacer_aero_u, 0, 1, 1, 1)

        self.horizontalSpacer_aero_l = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_aero_l, 1, 0, 1, 1)

        self.horizontalSpacer_aero_r = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_aero_r, 1, 2, 1, 1)

        self.tabWidget.addTab(self.tab_aero, "")
        self.tab_brake_diff = QWidget()
        self.tab_brake_diff.setObjectName(u"tab_brake_diff")
        self.gridLayout_12 = QGridLayout(self.tab_brake_diff)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.verticalSpacer_differential = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.gridLayout_12.addItem(self.verticalSpacer_differential, 4, 0, 1, 1)

        self.gridLayout_differential = QGridLayout()
        self.gridLayout_differential.setObjectName(u"gridLayout_differential")
        self.gridLayout_differential.setHorizontalSpacing(10)
        self.gridLayout_differential.setVerticalSpacing(5)
        self.gridLayout_differential.setContentsMargins(5, 5, 5, 5)
        self.label_differential_rear = QLabel(self.tab_brake_diff)
        self.label_differential_rear.setObjectName(u"label_differential_rear")
        self.label_differential_rear.setMinimumSize(QSize(30, 15))
        self.label_differential_rear.setMaximumSize(QSize(16777215, 25))
        self.label_differential_rear.setFont(font1)
        self.label_differential_rear.setAlignment(Qt.AlignCenter)

        self.gridLayout_differential.addWidget(self.label_differential_rear, 5, 0, 1, 3)

        self.label_differential_front = QLabel(self.tab_brake_diff)
        self.label_differential_front.setObjectName(u"label_differential_front")
        self.label_differential_front.setMinimumSize(QSize(30, 15))
        self.label_differential_front.setMaximumSize(QSize(16777215, 25))
        self.label_differential_front.setFont(font1)
        self.label_differential_front.setAlignment(Qt.AlignCenter)

        self.gridLayout_differential.addWidget(self.label_differential_front, 1, 0, 1, 3)

        self.label_differential_deceleration_rear = QLabel(self.tab_brake_diff)
        self.label_differential_deceleration_rear.setObjectName(u"label_differential_deceleration_rear")
        self.label_differential_deceleration_rear.setMinimumSize(QSize(50, 15))
        self.label_differential_deceleration_rear.setMaximumSize(QSize(70, 25))
        self.label_differential_deceleration_rear.setFont(font1)

        self.gridLayout_differential.addWidget(self.label_differential_deceleration_rear, 7, 0, 1, 1)

        self.line_differential = QFrame(self.tab_brake_diff)
        self.line_differential.setObjectName(u"line_differential")
        self.line_differential.setFrameShape(QFrame.Shape.HLine)
        self.line_differential.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_differential.addWidget(self.line_differential, 4, 0, 1, 3)

        self.label_deceleration = QLabel(self.tab_brake_diff)
        self.label_deceleration.setObjectName(u"label_deceleration")
        self.label_deceleration.setMinimumSize(QSize(50, 15))
        self.label_deceleration.setMaximumSize(QSize(16777215, 25))
        self.label_deceleration.setFont(font1)
        self.label_deceleration.setAlignment(Qt.AlignCenter)

        self.gridLayout_differential.addWidget(self.label_deceleration, 0, 0, 1, 3)

        self.label_differential_acceleration_front_value = QLabel(self.tab_brake_diff)
        self.label_differential_acceleration_front_value.setObjectName(u"label_differential_acceleration_front_value")
        self.label_differential_acceleration_front_value.setMinimumSize(QSize(30, 15))
        self.label_differential_acceleration_front_value.setMaximumSize(QSize(50, 25))
        self.label_differential_acceleration_front_value.setFont(font1)
        self.label_differential_acceleration_front_value.setAlignment(Qt.AlignCenter)

        self.gridLayout_differential.addWidget(self.label_differential_acceleration_front_value, 2, 2, 1, 1)

        self.horizontalSlider_differential_acceleration_front = QSlider(self.tab_brake_diff)
        self.horizontalSlider_differential_acceleration_front.setObjectName(u"horizontalSlider_differential_acceleration_front")
        sizePolicy.setHeightForWidth(self.horizontalSlider_differential_acceleration_front.sizePolicy().hasHeightForWidth())
        self.horizontalSlider_differential_acceleration_front.setSizePolicy(sizePolicy)
        self.horizontalSlider_differential_acceleration_front.setMinimumSize(QSize(120, 20))
        self.horizontalSlider_differential_acceleration_front.setMaximumSize(QSize(16777215, 25))
        self.horizontalSlider_differential_acceleration_front.setMinimum(-10000)
        self.horizontalSlider_differential_acceleration_front.setMaximum(10000)
        self.horizontalSlider_differential_acceleration_front.setOrientation(Qt.Horizontal)

        self.gridLayout_differential.addWidget(self.horizontalSlider_differential_acceleration_front, 2, 1, 1, 1)

        self.label_differential_acceleration_rear = QLabel(self.tab_brake_diff)
        self.label_differential_acceleration_rear.setObjectName(u"label_differential_acceleration_rear")
        self.label_differential_acceleration_rear.setMinimumSize(QSize(50, 15))
        self.label_differential_acceleration_rear.setMaximumSize(QSize(70, 25))
        self.label_differential_acceleration_rear.setFont(font1)

        self.gridLayout_differential.addWidget(self.label_differential_acceleration_rear, 6, 0, 1, 1)

        self.label_differential_acceleration_front = QLabel(self.tab_brake_diff)
        self.label_differential_acceleration_front.setObjectName(u"label_differential_acceleration_front")
        self.label_differential_acceleration_front.setMinimumSize(QSize(30, 15))
        self.label_differential_acceleration_front.setMaximumSize(QSize(70, 25))
        self.label_differential_acceleration_front.setFont(font1)

        self.gridLayout_differential.addWidget(self.label_differential_acceleration_front, 2, 0, 1, 1)

        self.label_differential_deceleration_front_value = QLabel(self.tab_brake_diff)
        self.label_differential_deceleration_front_value.setObjectName(u"label_differential_deceleration_front_value")
        self.label_differential_deceleration_front_value.setMinimumSize(QSize(30, 15))
        self.label_differential_deceleration_front_value.setMaximumSize(QSize(50, 25))
        self.label_differential_deceleration_front_value.setFont(font1)
        self.label_differential_deceleration_front_value.setAlignment(Qt.AlignCenter)

        self.gridLayout_differential.addWidget(self.label_differential_deceleration_front_value, 3, 2, 1, 1)

        self.horizontalSlider_differential_acceleration_rear = QSlider(self.tab_brake_diff)
        self.horizontalSlider_differential_acceleration_rear.setObjectName(u"horizontalSlider_differential_acceleration_rear")
        sizePolicy.setHeightForWidth(self.horizontalSlider_differential_acceleration_rear.sizePolicy().hasHeightForWidth())
        self.horizontalSlider_differential_acceleration_rear.setSizePolicy(sizePolicy)
        self.horizontalSlider_differential_acceleration_rear.setMinimumSize(QSize(120, 20))
        self.horizontalSlider_differential_acceleration_rear.setMaximumSize(QSize(16777215, 25))
        self.horizontalSlider_differential_acceleration_rear.setMinimum(-10000)
        self.horizontalSlider_differential_acceleration_rear.setMaximum(10000)
        self.horizontalSlider_differential_acceleration_rear.setOrientation(Qt.Horizontal)

        self.gridLayout_differential.addWidget(self.horizontalSlider_differential_acceleration_rear, 6, 1, 1, 1)

        self.label_differential_acceleration_rear_value = QLabel(self.tab_brake_diff)
        self.label_differential_acceleration_rear_value.setObjectName(u"label_differential_acceleration_rear_value")
        sizePolicy.setHeightForWidth(self.label_differential_acceleration_rear_value.sizePolicy().hasHeightForWidth())
        self.label_differential_acceleration_rear_value.setSizePolicy(sizePolicy)
        self.label_differential_acceleration_rear_value.setMinimumSize(QSize(30, 15))
        self.label_differential_acceleration_rear_value.setMaximumSize(QSize(50, 25))
        self.label_differential_acceleration_rear_value.setFont(font1)
        self.label_differential_acceleration_rear_value.setAlignment(Qt.AlignCenter)

        self.gridLayout_differential.addWidget(self.label_differential_acceleration_rear_value, 6, 2, 1, 1)

        self.label_differential_deceleration_rear_value = QLabel(self.tab_brake_diff)
        self.label_differential_deceleration_rear_value.setObjectName(u"label_differential_deceleration_rear_value")
        self.label_differential_deceleration_rear_value.setMinimumSize(QSize(30, 15))
        self.label_differential_deceleration_rear_value.setMaximumSize(QSize(50, 25))
        self.label_differential_deceleration_rear_value.setFont(font1)
        self.label_differential_deceleration_rear_value.setAlignment(Qt.AlignCenter)

        self.gridLayout_differential.addWidget(self.label_differential_deceleration_rear_value, 7, 2, 1, 1)

        self.horizontalSlider_differential_deceleration_rear = QSlider(self.tab_brake_diff)
        self.horizontalSlider_differential_deceleration_rear.setObjectName(u"horizontalSlider_differential_deceleration_rear")
        sizePolicy.setHeightForWidth(self.horizontalSlider_differential_deceleration_rear.sizePolicy().hasHeightForWidth())
        self.horizontalSlider_differential_deceleration_rear.setSizePolicy(sizePolicy)
        self.horizontalSlider_differential_deceleration_rear.setMinimumSize(QSize(120, 20))
        self.horizontalSlider_differential_deceleration_rear.setMaximumSize(QSize(16777215, 25))
        self.horizontalSlider_differential_deceleration_rear.setMinimum(-10000)
        self.horizontalSlider_differential_deceleration_rear.setMaximum(10000)
        self.horizontalSlider_differential_deceleration_rear.setOrientation(Qt.Horizontal)

        self.gridLayout_differential.addWidget(self.horizontalSlider_differential_deceleration_rear, 7, 1, 1, 1)

        self.horizontalSlider_differential_deceleration_front = QSlider(self.tab_brake_diff)
        self.horizontalSlider_differential_deceleration_front.setObjectName(u"horizontalSlider_differential_deceleration_front")
        sizePolicy.setHeightForWidth(self.horizontalSlider_differential_deceleration_front.sizePolicy().hasHeightForWidth())
        self.horizontalSlider_differential_deceleration_front.setSizePolicy(sizePolicy)
        self.horizontalSlider_differential_deceleration_front.setMinimumSize(QSize(120, 20))
        self.horizontalSlider_differential_deceleration_front.setMaximumSize(QSize(16777215, 25))
        self.horizontalSlider_differential_deceleration_front.setMinimum(-10000)
        self.horizontalSlider_differential_deceleration_front.setMaximum(10000)
        self.horizontalSlider_differential_deceleration_front.setOrientation(Qt.Horizontal)

        self.gridLayout_differential.addWidget(self.horizontalSlider_differential_deceleration_front, 3, 1, 1, 1)

        self.label_differential_deceleration_front = QLabel(self.tab_brake_diff)
        self.label_differential_deceleration_front.setObjectName(u"label_differential_deceleration_front")
        self.label_differential_deceleration_front.setMinimumSize(QSize(30, 15))
        self.label_differential_deceleration_front.setMaximumSize(QSize(70, 25))
        self.label_differential_deceleration_front.setFont(font1)

        self.gridLayout_differential.addWidget(self.label_differential_deceleration_front, 3, 0, 1, 1)

        self.label_differential_balance = QLabel(self.tab_brake_diff)
        self.label_differential_balance.setObjectName(u"label_differential_balance")
        self.label_differential_balance.setMinimumSize(QSize(50, 15))
        self.label_differential_balance.setMaximumSize(QSize(16777215, 25))
        self.label_differential_balance.setFont(font1)
        self.label_differential_balance.setAlignment(Qt.AlignCenter)

        self.gridLayout_differential.addWidget(self.label_differential_balance, 8, 0, 1, 3)

        self.label_differential_differential = QLabel(self.tab_brake_diff)
        self.label_differential_differential.setObjectName(u"label_differential_differential")
        self.label_differential_differential.setMinimumSize(QSize(50, 15))
        self.label_differential_differential.setMaximumSize(QSize(70, 25))
        self.label_differential_differential.setFont(font1)
        self.label_differential_differential.setAlignment(Qt.AlignCenter)

        self.gridLayout_differential.addWidget(self.label_differential_differential, 9, 0, 1, 1)

        self.label_differential_balance_value = QLabel(self.tab_brake_diff)
        self.label_differential_balance_value.setObjectName(u"label_differential_balance_value")
        self.label_differential_balance_value.setMinimumSize(QSize(30, 15))
        self.label_differential_balance_value.setMaximumSize(QSize(50, 25))
        self.label_differential_balance_value.setFont(font1)
        self.label_differential_balance_value.setAlignment(Qt.AlignCenter)

        self.gridLayout_differential.addWidget(self.label_differential_balance_value, 9, 2, 1, 1)

        self.horizontalSlider_differential_balance = QSlider(self.tab_brake_diff)
        self.horizontalSlider_differential_balance.setObjectName(u"horizontalSlider_differential_balance")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.horizontalSlider_differential_balance.sizePolicy().hasHeightForWidth())
        self.horizontalSlider_differential_balance.setSizePolicy(sizePolicy1)
        self.horizontalSlider_differential_balance.setMinimumSize(QSize(120, 20))
        self.horizontalSlider_differential_balance.setMaximumSize(QSize(16777215, 25))
        self.horizontalSlider_differential_balance.setMinimum(-10000)
        self.horizontalSlider_differential_balance.setMaximum(10000)
        self.horizontalSlider_differential_balance.setOrientation(Qt.Horizontal)

        self.gridLayout_differential.addWidget(self.horizontalSlider_differential_balance, 9, 1, 1, 1)


        self.gridLayout_12.addLayout(self.gridLayout_differential, 2, 0, 1, 1)

        self.gridLayout_main_brake = QGridLayout()
        self.gridLayout_main_brake.setObjectName(u"gridLayout_main_brake")
        self.gridLayout_main_brake.setHorizontalSpacing(10)
        self.gridLayout_main_brake.setVerticalSpacing(5)
        self.gridLayout_main_brake.setContentsMargins(5, 5, 5, 5)
        self.label_brake_prower = QLabel(self.tab_brake_diff)
        self.label_brake_prower.setObjectName(u"label_brake_prower")
        self.label_brake_prower.setMinimumSize(QSize(50, 15))
        self.label_brake_prower.setMaximumSize(QSize(70, 25))
        self.label_brake_prower.setFont(font1)
        self.label_brake_prower.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_brake.addWidget(self.label_brake_prower, 2, 0, 1, 1)

        self.label_brake_balance = QLabel(self.tab_brake_diff)
        self.label_brake_balance.setObjectName(u"label_brake_balance")
        self.label_brake_balance.setMinimumSize(QSize(50, 15))
        self.label_brake_balance.setMaximumSize(QSize(70, 25))
        self.label_brake_balance.setFont(font1)
        self.label_brake_balance.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_brake.addWidget(self.label_brake_balance, 1, 0, 1, 1)

        self.label_brake = QLabel(self.tab_brake_diff)
        self.label_brake.setObjectName(u"label_brake")
        self.label_brake.setMinimumSize(QSize(50, 15))
        self.label_brake.setMaximumSize(QSize(16777215, 25))
        self.label_brake.setFont(font1)
        self.label_brake.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_brake.addWidget(self.label_brake, 0, 0, 1, 3, Qt.AlignHCenter)

        self.horizontalSlider_brake_balance = QSlider(self.tab_brake_diff)
        self.horizontalSlider_brake_balance.setObjectName(u"horizontalSlider_brake_balance")
        sizePolicy1.setHeightForWidth(self.horizontalSlider_brake_balance.sizePolicy().hasHeightForWidth())
        self.horizontalSlider_brake_balance.setSizePolicy(sizePolicy1)
        self.horizontalSlider_brake_balance.setMinimumSize(QSize(120, 20))
        self.horizontalSlider_brake_balance.setMinimum(-10000)
        self.horizontalSlider_brake_balance.setMaximum(10000)
        self.horizontalSlider_brake_balance.setSingleStep(1)
        self.horizontalSlider_brake_balance.setPageStep(1)
        self.horizontalSlider_brake_balance.setValue(0)
        self.horizontalSlider_brake_balance.setOrientation(Qt.Horizontal)

        self.gridLayout_main_brake.addWidget(self.horizontalSlider_brake_balance, 1, 1, 1, 1)

        self.horizontalSlider_brake_power = QSlider(self.tab_brake_diff)
        self.horizontalSlider_brake_power.setObjectName(u"horizontalSlider_brake_power")
        sizePolicy1.setHeightForWidth(self.horizontalSlider_brake_power.sizePolicy().hasHeightForWidth())
        self.horizontalSlider_brake_power.setSizePolicy(sizePolicy1)
        self.horizontalSlider_brake_power.setMinimumSize(QSize(120, 20))
        self.horizontalSlider_brake_power.setMinimum(-10000)
        self.horizontalSlider_brake_power.setMaximum(10000)
        self.horizontalSlider_brake_power.setPageStep(1)
        self.horizontalSlider_brake_power.setValue(0)
        self.horizontalSlider_brake_power.setOrientation(Qt.Horizontal)

        self.gridLayout_main_brake.addWidget(self.horizontalSlider_brake_power, 2, 1, 1, 1)

        self.label_brake_balance_value = QLabel(self.tab_brake_diff)
        self.label_brake_balance_value.setObjectName(u"label_brake_balance_value")
        sizePolicy.setHeightForWidth(self.label_brake_balance_value.sizePolicy().hasHeightForWidth())
        self.label_brake_balance_value.setSizePolicy(sizePolicy)
        self.label_brake_balance_value.setMinimumSize(QSize(30, 15))
        self.label_brake_balance_value.setMaximumSize(QSize(50, 25))
        self.label_brake_balance_value.setFont(font1)
        self.label_brake_balance_value.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_brake.addWidget(self.label_brake_balance_value, 1, 2, 1, 1)

        self.label_brake_power_value = QLabel(self.tab_brake_diff)
        self.label_brake_power_value.setObjectName(u"label_brake_power_value")
        sizePolicy.setHeightForWidth(self.label_brake_power_value.sizePolicy().hasHeightForWidth())
        self.label_brake_power_value.setSizePolicy(sizePolicy)
        self.label_brake_power_value.setMinimumSize(QSize(30, 15))
        self.label_brake_power_value.setMaximumSize(QSize(50, 25))
        self.label_brake_power_value.setFont(font1)
        self.label_brake_power_value.setAlignment(Qt.AlignCenter)

        self.gridLayout_main_brake.addWidget(self.label_brake_power_value, 2, 2, 1, 1)


        self.gridLayout_12.addLayout(self.gridLayout_main_brake, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.gridLayout_12.addItem(self.verticalSpacer, 1, 0, 1, 1)

        self.tabWidget.addTab(self.tab_brake_diff, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.buttonBox = QDialogButtonBox(ConfigDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close|QDialogButtonBox.Open|QDialogButtonBox.Reset|QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(False)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(ConfigDialog)
        self.buttonBox.accepted.connect(ConfigDialog.accept)
        self.buttonBox.rejected.connect(ConfigDialog.reject)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(ConfigDialog)
    # setupUi

    def retranslateUi(self, ConfigDialog):
        ConfigDialog.setWindowTitle(QCoreApplication.translate("ConfigDialog", u"Car Configuration", None))
        self.label_info.setText(QCoreApplication.translate("ConfigDialog", u"Enter configuration details for the race session.", None))
        self.label_session_class.setText(QCoreApplication.translate("ConfigDialog", u"Class PI", None))
        self.label_session_car.setText(QCoreApplication.translate("ConfigDialog", u"Car", None))
        self.label_session_location.setText(QCoreApplication.translate("ConfigDialog", u"Location", None))
        self.label_session_surface.setText(QCoreApplication.translate("ConfigDialog", u"Surface", None))
        self.label_session_road_type.setText(QCoreApplication.translate("ConfigDialog", u"Road Type", None))
        self.comboBox_session_surface.setItemText(0, QCoreApplication.translate("ConfigDialog", u"- - -", None))

        self.comboBox_session_location.setItemText(0, QCoreApplication.translate("ConfigDialog", u"- - -", None))

        self.label_session_name.setText(QCoreApplication.translate("ConfigDialog", u"Name", None))
        self.comboBox_session_road_type.setItemText(0, QCoreApplication.translate("ConfigDialog", u"- - -", None))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_session), QCoreApplication.translate("ConfigDialog", u"Session", None))
        self.label_info_power.setText(QCoreApplication.translate("ConfigDialog", u"Power", None))
        self.label_info_front_weight.setText(QCoreApplication.translate("ConfigDialog", u"Front %", None))
        self.label_info_drive_type.setText(QCoreApplication.translate("ConfigDialog", u"Drive Type", None))
        self.label_info_power_unit.setText(QCoreApplication.translate("ConfigDialog", u"Hp", None))
        self.label_info_drive_type_unit.setText(QCoreApplication.translate("ConfigDialog", u"Type", None))
        self.label_info_front_weight_unit.setText(QCoreApplication.translate("ConfigDialog", u"%", None))
        self.label_info_engine_placement_unit.setText(QCoreApplication.translate("ConfigDialog", u"Type", None))
        self.label_info_suspension_travel.setText(QCoreApplication.translate("ConfigDialog", u"Suspension Travel", None))
        self.label_info_suspension_travel_unit.setText(QCoreApplication.translate("ConfigDialog", u"mm", None))
        self.comboBox_info_drive_type.setItemText(0, QCoreApplication.translate("ConfigDialog", u"- - -", None))

        self.label_info_weight.setText(QCoreApplication.translate("ConfigDialog", u"Weight", None))
        self.label_info_weight_unit.setText(QCoreApplication.translate("ConfigDialog", u"kg", None))
        self.comboBox_info_engine_placement.setItemText(0, QCoreApplication.translate("ConfigDialog", u"- - -", None))

        self.label_info_engine_placement.setText(QCoreApplication.translate("ConfigDialog", u"Engine Placement", None))
        self.label_info_torque.setText(QCoreApplication.translate("ConfigDialog", u"Torque", None))
        self.label_info_torque_unit.setText(QCoreApplication.translate("ConfigDialog", u"Nm", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_info), QCoreApplication.translate("ConfigDialog", u"Info", None))
        self.label_tire_tier.setText(QCoreApplication.translate("ConfigDialog", u"Tire", None))
        self.label_tire_rear_value.setText(QCoreApplication.translate("ConfigDialog", u"num", None))
        self.label_tire_pressure.setText(QCoreApplication.translate("ConfigDialog", u"Pressure", None))
        self.label_tire_front_value.setText(QCoreApplication.translate("ConfigDialog", u"num", None))
        self.label_tire_width.setText(QCoreApplication.translate("ConfigDialog", u"Width", None))
        self.label_tire_rear.setText(QCoreApplication.translate("ConfigDialog", u"Rear", None))
        self.label_tire_front.setText(QCoreApplication.translate("ConfigDialog", u"Front", None))
        self.label_tire_compound.setText(QCoreApplication.translate("ConfigDialog", u"Compound", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_tires), QCoreApplication.translate("ConfigDialog", u"Tires", None))
        self.label_alignment_camber.setText(QCoreApplication.translate("ConfigDialog", u"\u0421amber", None))
        self.label_alignment_toe.setText(QCoreApplication.translate("ConfigDialog", u"Toe", None))
        self.label_alignment_rear.setText(QCoreApplication.translate("ConfigDialog", u"Rear", None))
        self.label_alignment_rear_toe_value.setText(QCoreApplication.translate("ConfigDialog", u"num", None))
        self.label_alignment_rear_camber_value.setText(QCoreApplication.translate("ConfigDialog", u"num", None))
        self.label_alignment_front_camber_value.setText(QCoreApplication.translate("ConfigDialog", u"num", None))
        self.label_alignment_front.setText(QCoreApplication.translate("ConfigDialog", u"Front", None))
        self.label_alignment_front_toe_value.setText(QCoreApplication.translate("ConfigDialog", u"num", None))
        self.label_alignment_side.setText(QCoreApplication.translate("ConfigDialog", u"Side", None))
        self.label_alignment_caster.setText(QCoreApplication.translate("ConfigDialog", u"Caster", None))
        self.label_alignment_front_caster_value.setText(QCoreApplication.translate("ConfigDialog", u"num", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_alignment), QCoreApplication.translate("ConfigDialog", u"Alignment", None))
        self.label_spring_max.setText(QCoreApplication.translate("ConfigDialog", u"MAX", None))
        self.label_spring_min.setText(QCoreApplication.translate("ConfigDialog", u"MIN", None))
        self.label_spring_spring.setText(QCoreApplication.translate("ConfigDialog", u"Spring", None))
        self.label_spring_rear.setText(QCoreApplication.translate("ConfigDialog", u"Rear", None))
        self.label_spring_clearance.setText(QCoreApplication.translate("ConfigDialog", u"Clearance", None))
        self.label_spring_front.setText(QCoreApplication.translate("ConfigDialog", u"Front", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_spring), QCoreApplication.translate("ConfigDialog", u"Spring", None))
        self.label_damping_rear.setText(QCoreApplication.translate("ConfigDialog", u"Rear", None))
        self.label_damping_front.setText(QCoreApplication.translate("ConfigDialog", u"Front", None))
        self.label_damping_min.setText(QCoreApplication.translate("ConfigDialog", u"Min", None))
        self.label_damping_max.setText(QCoreApplication.translate("ConfigDialog", u"Max", None))
        self.label_damping_Damping.setText(QCoreApplication.translate("ConfigDialog", u"Damping", None))
        self.label_damping_rebound.setText(QCoreApplication.translate("ConfigDialog", u"Rebound", None))
        self.label_damping_bump.setText(QCoreApplication.translate("ConfigDialog", u"Bump", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_damping), QCoreApplication.translate("ConfigDialog", u"Damping", None))
        self.label_roll_bar_max.setText(QCoreApplication.translate("ConfigDialog", u"64", None))
        self.label_roll_bar_front.setText(QCoreApplication.translate("ConfigDialog", u"Front", None))
        self.label_roll_bar_rear.setText(QCoreApplication.translate("ConfigDialog", u"Rear", None))
        self.label_roll_bar_side.setText(QCoreApplication.translate("ConfigDialog", u"Side", None))
        self.label_roll_bar_min.setText(QCoreApplication.translate("ConfigDialog", u"1", None))
        self.label_roll_bar_unit.setText(QCoreApplication.translate("ConfigDialog", u"N/mm", None))
        self.label_roll_bar_front_value.setText(QCoreApplication.translate("ConfigDialog", u"num", None))
        self.label_roll_bar_rear_value.setText(QCoreApplication.translate("ConfigDialog", u"num", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_roll_bar), QCoreApplication.translate("ConfigDialog", u"Roll-Bar", None))
        self.label_aero_min.setText(QCoreApplication.translate("ConfigDialog", u"Min", None))
        self.label_aero.setText(QCoreApplication.translate("ConfigDialog", u"Curent Num", None))
        self.label_aero_max.setText(QCoreApplication.translate("ConfigDialog", u"Max", None))
        self.checkBox_aero_front.setText(QCoreApplication.translate("ConfigDialog", u"Front", None))
        self.checkBox_aero_rear.setText(QCoreApplication.translate("ConfigDialog", u"Rear", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_aero), QCoreApplication.translate("ConfigDialog", u"Aero", None))
        self.label_differential_rear.setText(QCoreApplication.translate("ConfigDialog", u"Rear", None))
        self.label_differential_front.setText(QCoreApplication.translate("ConfigDialog", u"Front", None))
        self.label_differential_deceleration_rear.setText(QCoreApplication.translate("ConfigDialog", u"Deceleration", None))
        self.label_deceleration.setText(QCoreApplication.translate("ConfigDialog", u"Differential", None))
        self.label_differential_acceleration_front_value.setText(QCoreApplication.translate("ConfigDialog", u"num", None))
        self.label_differential_acceleration_rear.setText(QCoreApplication.translate("ConfigDialog", u"Acceleration", None))
        self.label_differential_acceleration_front.setText(QCoreApplication.translate("ConfigDialog", u"Acceleration", None))
        self.label_differential_deceleration_front_value.setText(QCoreApplication.translate("ConfigDialog", u"num", None))
        self.label_differential_acceleration_rear_value.setText(QCoreApplication.translate("ConfigDialog", u"num", None))
        self.label_differential_deceleration_rear_value.setText(QCoreApplication.translate("ConfigDialog", u"num", None))
        self.label_differential_deceleration_front.setText(QCoreApplication.translate("ConfigDialog", u"Deceleration", None))
        self.label_differential_balance.setText(QCoreApplication.translate("ConfigDialog", u"Balance", None))
        self.label_differential_differential.setText(QCoreApplication.translate("ConfigDialog", u"Differential", None))
        self.label_differential_balance_value.setText(QCoreApplication.translate("ConfigDialog", u"num", None))
        self.label_brake_prower.setText(QCoreApplication.translate("ConfigDialog", u"Power", None))
        self.label_brake_balance.setText(QCoreApplication.translate("ConfigDialog", u"Balance", None))
        self.label_brake.setText(QCoreApplication.translate("ConfigDialog", u"Brake", None))
        self.label_brake_balance_value.setText(QCoreApplication.translate("ConfigDialog", u"num", None))
        self.label_brake_power_value.setText(QCoreApplication.translate("ConfigDialog", u"num", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_brake_diff), QCoreApplication.translate("ConfigDialog", u"Brake|Differential", None))
    # retranslateUi


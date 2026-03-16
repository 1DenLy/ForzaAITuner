from PySide6.QtWidgets import QStyledItemDelegate, QStyle
from PySide6.QtCore import Qt, QRect, QSize, Signal, QObject
from PySide6.QtGui import QPainter, QColor, QFont, QPen, QBrush

class ConfigItemDelegate(QStyledItemDelegate):
    """
    Delegate for rendering configuration items in QListView.
    Provides a more performant and visually consistent look than setItemWidget.
    """

    PADDING = 10
    TITLE_FONT_SIZE = 12
    SUBTITLE_FONT_SIZE = 10

    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter: QPainter, option, index):
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)

        config = index.data(Qt.UserRole + 1) # DATA_ROLE from model
        if not config:
            painter.restore()
            return

        # Draw Background
        if option.state & QStyle.State_Selected:
            bg_color = QColor(60, 60, 80) # Dark blue/grey for selection
        elif option.state & QStyle.State_MouseOver:
            bg_color = QColor(45, 45, 55) # Slightly lighter for hover
        else:
            bg_color = QColor(30, 30, 35) # Default dark background

        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(option.rect.adjusted(2, 2, -2, -2), 5, 5)

        # Draw Text
        rect = option.rect.adjusted(self.PADDING, self.PADDING, -self.PADDING, -self.PADDING)
        
        # Car Name (Title)
        title_font = QFont()
        title_font.setPointSize(self.TITLE_FONT_SIZE)
        title_font.setBold(True)
        painter.setFont(title_font)
        painter.setPen(QPen(QColor(230, 230, 230)))
        
        car_name = config.get("car_name", "Unknown Car")
        painter.drawText(rect.adjusted(0, 0, 0, -20), Qt.AlignLeft | Qt.AlignTop, car_name)

        # Meta info (Subtitle: Class, Date)
        subtitle_font = QFont()
        subtitle_font.setPointSize(self.SUBTITLE_FONT_SIZE)
        painter.setFont(subtitle_font)
        painter.setPen(QPen(QColor(150, 150, 150)))
        
        pi_class = config.get("class_pi", "---")
        created_at = config.get("created_at", "--:--")
        meta_info = f"Class: {pi_class}  |  Created: {created_at}"
        painter.drawText(rect.adjusted(0, 20, 0, 0), Qt.AlignLeft | Qt.AlignTop, meta_info)

        painter.restore()

    def sizeHint(self, option, index):
        return QSize(200, 60)

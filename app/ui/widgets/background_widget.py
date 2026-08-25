from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPixmap
from app.utils.resource_path import resource_path

class BackgroundWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._bg_pixmap = QPixmap(str(resource_path("app/resources/icons/background.png")))

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self._bg_pixmap.isNull():
            painter = QPainter(self)
            painter.drawPixmap(self.rect(), self._bg_pixmap)

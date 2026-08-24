from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon
from PySide6 import QtCore

class IconButton(QPushButton):
    def __init__(self, normal_icon, hover_icon, parent=None):
        super().__init__(parent)
        self.normal_icon = QIcon(str(normal_icon))
        self.hover_icon = QIcon(str(hover_icon))
        self.setIcon(self.normal_icon)
        self.setIconSize(QtCore.QSize(22, 22))

        # animación persistente
        self._animation = QtCore.QPropertyAnimation(self, b"iconSize")
        self._animation.setDuration(150)  # transición más lenta
        self._animation.setEasingCurve(QtCore.QEasingCurve.OutCubic)

    def enterEvent(self, event):
        self.setIcon(self.hover_icon)
        self._animate_size(QtCore.QSize(24, 24))
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(self.normal_icon)
        self._animate_size(QtCore.QSize(22, 22))
        super().leaveEvent(event)

    def _animate_size(self, target_size):
        self._animation.stop()
        self._animation.setStartValue(self.iconSize())
        self._animation.setEndValue(target_size)
        self._animation.start()

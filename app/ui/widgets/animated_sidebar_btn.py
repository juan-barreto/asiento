from PySide6.QtCore import (
    QEasingCurve,
    Property,
    QPropertyAnimation
)

from PySide6.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor


class AnimatedSidebarButton(QPushButton):

    def __init__(self, text):
        super().__init__(text)

        self.setObjectName("sidebarButton")

        self._padding = 12

        self._animation = QPropertyAnimation(
            self,
            b"leftPadding"
        )

        self._animation.setDuration(170)
        self._animation.setEasingCurve(
            QEasingCurve.OutCubic
        )

        shadow = QGraphicsDropShadowEffect()

        shadow.setBlurRadius(0)
        shadow.setOffset(0, 0)

        self.setGraphicsEffect(shadow)

        self._shadow = shadow

    # ----------------------------------------
    # Propiedad animable
    # ----------------------------------------

    def getLeftPadding(self):
        return self._padding

    def setLeftPadding(self, value):

        self._padding = value

        self.setStyleSheet(
            f"""
            padding-left: {value}px;
            """
        )

    leftPadding = Property(
        int,
        getLeftPadding,
        setLeftPadding
    )

    # ----------------------------------------

    def enterEvent(self, event):

        self._animation.stop()

        self._animation.setStartValue(
            self._padding
        )

        self._animation.setEndValue(18)

        self._animation.start()

        self._shadow.setBlurRadius(18)
        self._shadow.setColor(
            QColor(37,99,235,120)
        )

        super().enterEvent(event)

    # ----------------------------------------

    def leaveEvent(self, event):

        self._animation.stop()

        self._animation.setStartValue(
            self._padding
        )

        self._animation.setEndValue(12)

        self._animation.start()

        self._shadow.setBlurRadius(0)

        super().leaveEvent(event)
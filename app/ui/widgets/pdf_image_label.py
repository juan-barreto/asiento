from PySide6.QtCore import Qt

from PySide6.QtWidgets import QLabel


class PdfImageLabel(QLabel):

    def __init__(self):

        super().__init__()

        self._scroll_area = None

        self._dragging = False

        self._last_position = None

        self.setAlignment(Qt.AlignCenter)

    # --------------------------------------------------

    def set_scroll_area(self, scroll_area):

        self._scroll_area = scroll_area

    # --------------------------------------------------

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:

            self._dragging = True

            self._last_position = event.globalPosition().toPoint()

            self.setCursor(Qt.ClosedHandCursor)

        super().mousePressEvent(event)

    # --------------------------------------------------

    def mouseMoveEvent(self, event):

        if not self._dragging:

            return

        if self._scroll_area is None:

            return

        current = event.globalPosition().toPoint()

        delta = current - self._last_position

        self._last_position = current

        h = self._scroll_area.horizontalScrollBar()

        v = self._scroll_area.verticalScrollBar()

        h.setValue(

            h.value() - delta.x()

        )

        v.setValue(

            v.value() - delta.y()

        )

        super().mouseMoveEvent(event)

    # --------------------------------------------------

    def mouseReleaseEvent(self, event):

        self._dragging = False

        self.setCursor(Qt.ArrowCursor)

        super().mouseReleaseEvent(event)
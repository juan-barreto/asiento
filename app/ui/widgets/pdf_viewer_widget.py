from PySide6.QtCore import Qt

from PySide6.QtGui import (
    QPixmap,
    QImage
)
from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea
)

from app.ui.widgets.pdf_image_label import PdfImageLabel

import fitz


class PdfViewerWidget(QWidget):

    def __init__(self):
        super().__init__()

        self._document = None

        self._current_page = 0

        self._zoom = 1.0

        self._create_widgets()
        self._create_layout()
        self._connect_signals()

    # ---------------------------------------------------------

    def _create_widgets(self):

        self._page_label = QLabel(
            "Página 0 / 0"
        )

        self._page_label.setAlignment(
            Qt.AlignCenter
        )

        self._image = PdfImageLabel()

        self._image.setAlignment(
            Qt.AlignCenter
        )

        self._image.setScaledContents(False)

 
        # Scroll Area


        self._scroll = QScrollArea()

        self._scroll.setWidget(
            self._image
        )

        self._image.set_scroll_area(
            self._scroll
        )

        self._scroll.setWidgetResizable(False)

        self._scroll.setAlignment(
        Qt.AlignCenter
        )

        self._btn_previous = QPushButton("◀")

        self._btn_next = QPushButton("▶")

        self._btn_zoom_out = QPushButton("−")

        self._btn_zoom_in = QPushButton("+")

        self._btn_previous.setEnabled(False)
        self._btn_next.setEnabled(False)

    # ---------------------------------------------------------

    def _create_layout(self):

        layout = QVBoxLayout()

        layout.addWidget(
            self._scroll,
            stretch=1
        )

        nav = QHBoxLayout()

        nav.addStretch()

        nav.addWidget(
            self._btn_previous
        )

        nav.addWidget(
            self._page_label
        )

        nav.addWidget(
            self._btn_next
        )

        nav.addSpacing(10)

        nav.addWidget(
            self._btn_zoom_out
        )

        nav.addWidget(
            self._btn_zoom_in
        )

        nav.addStretch()

        layout.addLayout(nav)

        self.setLayout(layout)

    # ---------------------------------------------------------

    def _connect_signals(self):

        self._btn_previous.clicked.connect(
            self._previous_page
        )

        self._btn_next.clicked.connect(
            self._next_page
        )

        self._btn_zoom_in.clicked.connect(
            self._zoom_in
        )

        self._btn_zoom_out.clicked.connect(
            self._zoom_out
        )

    # ---------------------------------------------------------

    def load_pdf(self, pdf_path):

        self._document = fitz.open(pdf_path)

        self._current_page = 0

        self._zoom = 1.0

        self._render_page()

    # ---------------------------------------------------------

    def _render_page(self):

        if self._document is None:
            return

        page = self._document.load_page(
            self._current_page
        )

        pix = page.get_pixmap(

            matrix=fitz.Matrix(
                self._zoom,
                self._zoom
            )

        )

        image_format = (

            QImage.Format_RGBA8888

            if pix.alpha

            else QImage.Format_RGB888

        )

        image = QImage(

            pix.samples,

            pix.width,

            pix.height,

            pix.stride,

            image_format

        )

        pixmap = QPixmap.fromImage(image)

        self._image.setPixmap(pixmap)

        self._image.resize(pixmap.size())

        self._page_label.setText(

            f"Página {self._current_page + 1} / {self._document.page_count}   |   {int(self._zoom*100)}%"

        )

        self._btn_previous.setEnabled(

            self._current_page > 0

        )

        self._btn_next.setEnabled(

            self._current_page < self._document.page_count - 1

        )

    # ---------------------------------------------------------

    def _previous_page(self):

        if self._document is None:
            return

        if self._current_page == 0:
            return

        self._current_page -= 1

        self._render_page()

    # ---------------------------------------------------------

    def _next_page(self):

        if self._document is None:
            return

        if self._current_page >= self._document.page_count - 1:
            return

        self._current_page += 1

        self._render_page()

    # ---------------------------------------------------------

    def _zoom_in(self):

        if self._document is None:
            return

        if self._zoom >= 4.0:
            return

        self._zoom += 0.25

        self._render_page()

    # ---------------------------------------------------------

    def _zoom_out(self):

        if self._document is None:
            return

        if self._zoom <= 0.25:
            return

        self._zoom -= 0.25

        self._render_page()

    # ---------------------------------------------------------

    def resizeEvent(self, event):

        if self._document is None:
                    return

        super().resizeEvent(event)

        if self._document:

            self._render_page()

    def wheelEvent(self, event):
        if self._document is None:
                    return

        if event.modifiers() & Qt.ControlModifier:

            delta = event.angleDelta().y()

            if delta > 0:
                  self._zoom_in()
            else:
                self._zoom_out()

            event.accept()

            return


        super().wheelEvent(event)

if __name__ == "__main__":

    import sys

    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    viewer = PdfViewerWidget()

    viewer.load_pdf(
        r"C:\Users\Juan\Desktop\ASIENTO\app\services\Extracto_Cuentas_Galicia_2026_01_30.pdf"
    )

    viewer.resize(
        900,
        800
    )

    viewer.show()

    sys.exit(app.exec())
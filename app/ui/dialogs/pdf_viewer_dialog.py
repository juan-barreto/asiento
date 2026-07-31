from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout
)

from app.ui.widgets.pdf_viewer_widget import PdfViewerWidget


class PdfViewerDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("ASIENTO Studio - Visor PDF")

        self.resize(1000, 800)

        self._create_widgets()
        self._create_layout()

    # --------------------------------------------------

    def _create_widgets(self):

        self._viewer = PdfViewerWidget()

    # --------------------------------------------------

    def _create_layout(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self._viewer)

        self.setLayout(layout)

    # --------------------------------------------------

    def load_pdf(self, pdf_path):

        self._viewer.load_pdf(pdf_path)

if __name__ == "__main__":

    import sys

    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    dialog = PdfViewerDialog()

    dialog.load_pdf(
        r"C:\Users\Juan\Desktop\ASIENTO\app\services\Extracto_Cuentas_Galicia_2026_01_30.pdf"
    )

    dialog.exec()

    sys.exit(app.exec())
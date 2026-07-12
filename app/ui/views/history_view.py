from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class HistoryView(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Historial"))

        self.setLayout(layout)
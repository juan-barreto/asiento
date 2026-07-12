from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class MetricCard(QWidget):

    def __init__(self, title: str):
        super().__init__()

        self._title = title

        self._create_widgets()
        self._create_layout()

    def _create_widgets(self):

        self._lbl_title = QLabel(self._title)
        self._lbl_value = QLabel("0")

    def _create_layout(self):

        layout = QVBoxLayout()

        layout.addWidget(self._lbl_title)
        layout.addWidget(self._lbl_value)

        self.setLayout(layout)

    # Metodos publicos para obtener el valor del card

    def set_value(self, value: int):

        self._lbl_value.setText(str(value))

        
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class MetricCard(QWidget):

    def __init__(self, title: str):
        super().__init__()

        self.setObjectName("metricCard")

        self._title = title

        self._create_widgets()
        self._create_layout()

    def _create_widgets(self):

        self._lbl_title = QLabel(self._title)
        self._lbl_value = QLabel("0")

        self._lbl_title.setObjectName("metricTitle")
        self._lbl_value.setObjectName("metricValue")

    def _create_layout(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(16,16,16,16)
        layout.setSpacing(6)

        layout.addWidget(self._lbl_title)
        layout.addWidget(self._lbl_value)

        self.setLayout(layout)

    # Metodos publicos para obtener el valor del card

    def set_value(self, value: int):

        self._lbl_value.setText(str(value))

        
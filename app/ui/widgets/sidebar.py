from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout



class Sidebar(QWidget):

    navigate = Signal(int)

    def __init__(self):
        super().__init__()

        self._create_widgets()
        self._create_layout()
        self._connect_signals()

    
    def _create_widgets(self):

        self._btn_converter = QPushButton("Conversión")
        self._btn_history = QPushButton("Historial")
        self._btn_settings = QPushButton("Configuración")

    def _create_layout(self):

        layout = QVBoxLayout()

        layout.addWidget(self._btn_converter)
        layout.addWidget(self._btn_history)
        layout.addWidget(self._btn_settings)

        layout.addStretch()

        self.setLayout(layout)

    def _connect_signals(self):

        self._btn_converter.clicked.connect(lambda: self.navigate.emit(0))
        self._btn_history.clicked.connect(lambda: self.navigate.emit(1))
        self._btn_settings.clicked.connect(lambda: self.navigate.emit(2))

    
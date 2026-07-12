from PySide6.QtWidgets import QWidget, QTextEdit, QVBoxLayout

class LogPanel(QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName("logPanel")

        self._create_widgets()
        self._create_layout()

    def _create_widgets(self):

        self._log = QTextEdit()

        self._log.setObjectName("logText")

        self._log.setReadOnly(True)

    def _create_layout(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(12,12,12,12)

        layout.addWidget(self._log)

        layout.addWidget(self._log)

        self.setLayout(layout)

    
    # Métodos públicos para añadir logs y limpiar texto

    def append_log(self, message: str):
        self._log.append(message)

    def clear(self):
        self._log.clear()
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class FileCard(QWidget):

    def __init__(self):

        super().__init__()

        self._create_widgets()
        self._create_layout()


    def _create_widgets(self):

        self._lbl_file = QLabel("Ningún archivo seleccionado")
        self._lbl_bank = QLabel("Banco: -")
        self._lbl_status = QLabel("Estado: Esperando archivo")

    def _create_layout(self):

        layout = QVBoxLayout()

        layout.addWidget(self._lbl_file)
        layout.addWidget(self._lbl_bank)
        layout.addWidget(self._lbl_status)

        self.setLayout(layout)

    def set_file_name(self, file_name: str):
        self._lbl_file.setText(f"{file_name}")

    def set_bank(self, bank: str):
        self._lbl_bank.setText(f"Banco: {bank}")

    def set_status(self, status: str):
        self._lbl_status.setText(f"{status}")



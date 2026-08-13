from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget , QPushButton, QHBoxLayout
from PySide6.QtCore import Qt

class ActionBar(QWidget):

    select_pdf = Signal()
    process = Signal()
    export = Signal()
    review = Signal()


    def __init__(self):

        super().__init__()
        
        # QSS
        # ----------------------------------------------------
        self.setObjectName("actionBar")
        self.setAttribute(Qt.WA_StyledBackground, True)
        # ----------------------------------------------------
        self._create_widgets()
        self._create_layout()
        self._connect_signals()

    def _create_widgets(self):

        self._btn_select_pdf = QPushButton("Seleccionar PDF")
        self._btn_process = QPushButton("Procesar")
        self._btn_review = QPushButton("Editar movimientos")
        self._btn_export = QPushButton("Exportar Excel")

        # QSS
        # ----------------------------------------------------
        self._btn_select_pdf.setObjectName("selectButton")
        self._btn_process.setObjectName("processButton")
        self._btn_review.setObjectName("reviewButton")
        self._btn_export.setObjectName("exportButton")
        # ----------------------------------------------------

        self.set_process_enabled(False)
        self.set_review_enabled(False)
        self.set_export_enabled(False)

    def _create_layout(self):

        layout = QHBoxLayout()

        layout.addWidget(self._btn_select_pdf)
        layout.addWidget(self._btn_process)
        layout.addWidget(self._btn_review)
        layout.addWidget(self._btn_export)
        
        # QSS
        # ----------------------------------------------------
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        # ----------------------------------------------------
        layout.addStretch()

        self.setLayout(layout)

    def _connect_signals(self):

        self._btn_select_pdf.clicked.connect(self.select_pdf.emit)
        self._btn_process.clicked.connect(self.process.emit)
        self._btn_export.clicked.connect(self.export.emit)
        self._btn_review.clicked.connect(self.review.emit)

    # metodos publicos para acceder a la habilitacion de los botones

    def set_process_enabled(self, enabled : bool):

        self._btn_process.setEnabled(enabled)

    def set_export_enabled(self, enabled : bool):

        self._btn_export.setEnabled(enabled)

    def set_review_enabled(self, enabled: bool):
        self._btn_review.setEnabled(enabled)

    


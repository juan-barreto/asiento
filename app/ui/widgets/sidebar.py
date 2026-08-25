from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame

from app.ui.widgets.animated_sidebar_btn import AnimatedSidebarButton


class Sidebar(QWidget):

    navigate = Signal(int)

    def __init__(self):
        super().__init__()

        self.setObjectName("sidebar")

        self._create_widgets()
        self._create_layout()
        self._connect_signals()

    def _create_widgets(self):

        self._title = QLabel("ASIENTO")
        self._title.setObjectName("sidebarTitle")

        self._subtitle = QLabel("Studio®")
        self._subtitle.setObjectName("sidebarSubtitle")

        self._separator = QFrame()
        self._separator.setObjectName("sidebarSeparator")
        self._separator.setFrameShape(QFrame.HLine)

        self._btn_converter = AnimatedSidebarButton(" Conversión")
        self._btn_history = AnimatedSidebarButton(" Historial")
        self._btn_export = AnimatedSidebarButton(" Exportar")
        self._btn_settings = AnimatedSidebarButton(" Configuración")

        self._btn_export.setObjectName("sidebarButton")

        self._version = QLabel("v0.1.1")
        self._version.setObjectName("sidebarVersion")

    def set_export_enabled(self, enabled: bool):
        self._btn_export.setEnabled(enabled)

    def _create_layout(self):

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 22, 16, 18)
        layout.setSpacing(10)

        brand_layout = QVBoxLayout()
        brand_layout.setContentsMargins(0, 0, 0, 0)
        brand_layout.setSpacing(0)

        brand_layout.addWidget(self._title)
        brand_layout.addWidget(self._subtitle)

        layout.addLayout(brand_layout)
        layout.addSpacing(8)
        layout.addWidget(self._separator)

        layout.addSpacing(8)

        layout.addWidget(self._btn_converter)
        layout.addWidget(self._btn_history)
        layout.addWidget(self._btn_export)
        layout.addWidget(self._btn_settings)

        layout.addStretch()

        layout.addWidget(self._version)

        self.setLayout(layout)

    def _connect_signals(self):

        self._btn_converter.clicked.connect(lambda: self.navigate.emit(0))
        self._btn_history.clicked.connect(lambda: self.navigate.emit(2))
        self._btn_export.clicked.connect(lambda: self.navigate.emit(3))
        self._btn_settings.clicked.connect(lambda: self.navigate.emit(4))
        
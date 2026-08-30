from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QProgressBar, QVBoxLayout, QWidget

from app.utils.resource_path import resource_path


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(360, 200)
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.SplashScreen
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(10)

        # Logo
        self.logo = QLabel()
        self.logo.setAlignment(Qt.AlignCenter)

        logo_path = resource_path(
            "resources/icons/asiento.png"
        )

        pixmap = QPixmap(str(logo_path))

        if not pixmap.isNull():
            self.logo.setPixmap(
                pixmap.scaled(
                    100,
                    110,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )

        layout.addWidget(self.logo)

        # Nombre
        self.title = QLabel("ASIENTO")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
            }
        """)

        layout.addWidget(self.title)

        # Estado
        self.status = QLabel("Iniciando aplicación...")
        self.status.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.status)

        # Barra de progreso
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(6)

        layout.addWidget(self.progress)

        # Fondo
        self.setStyleSheet("""
            SplashScreen {
                background: #000000;
                border-radius: 16px;
            }

            QProgressBar {
                border: none;
                background: #e5e7eb;
                border-radius: 3px;
            }

            QProgressBar::chunk {
                background: #2563eb;
                border-radius: 3px;
            }
        """)

    def set_progress(self, value):
        self.progress.setValue(value)

    def set_status(self, text):
        self.status.setText(text)
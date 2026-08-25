from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSplitter,
    QLabel
)

from PySide6.QtCore import Qt

from app.ui.widgets.pdf_viewer_widget import PdfViewerWidget
from app.ui.widgets.file_card import FileCard
from app.ui.widgets.action_bar import ActionBar
from app.ui.widgets.summary_panel import SummaryPanel
from app.ui.widgets.log_panel import LogPanel


class ConverterView(QWidget):

    def __init__(self):
        super().__init__()

        self._create_widgets()
        self._create_layout()

    
    def _create_widgets(self):

        self._title = QLabel("Conversión")
        self._title.setObjectName("conversionTitle")
        
        self._subtitle = QLabel(
            "Procesa tus extractos bancarios."
                )
        self._subtitle.setObjectName("conversionSubtitle")
        
        self._file_card = FileCard()
        self._action_bar = ActionBar()
        self._summary_panel = SummaryPanel()
        self._log_panel = LogPanel()
        self._pdf_viewer = PdfViewerWidget()
        self._right_panel = QWidget()
        self._file_card.setObjectName("fileCard")
        self._action_bar.setObjectName("actionBar")
        self._summary_panel.setObjectName("summaryPanel")
        self._log_panel.setObjectName("logPanel")
        self._pdf_viewer.setObjectName("pdfViewer")
        self._right_panel.setObjectName("rightPanel")

        


    def _create_layout(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(20, 20, 20, 20)
                    
        layout.addWidget(self._title)
        layout.addWidget(self._subtitle)
        layout.setSpacing(14)
        layout.addWidget(self._file_card)

        self._splitter = QSplitter(Qt.Horizontal)

        right_layout = QVBoxLayout()

        right_layout.setContentsMargins(0, 0, 0, 0)

        right_layout.setSpacing(8)

        right_layout.addWidget(self._summary_panel)

        right_layout.addWidget(
            self._log_panel,
            stretch=1
        )

        self._right_panel.setLayout(
            right_layout
        )

        self._splitter.addWidget(
            self._pdf_viewer
        )

        self._splitter.addWidget(
            self._right_panel
        )
        self._splitter.setChildrenCollapsible(False)
        self._splitter.setOpaqueResize(False)

        self._splitter.setStretchFactor(
            0,
            3
        )

        self._splitter.setStretchFactor(
            1,
            2
        )

        layout.addWidget(
            self._splitter,
            stretch=1
        )

        layout.addWidget(
            self._action_bar
        )

        self.setLayout(layout)

        self._splitter.setStyleSheet("background: transparent;")
        self._right_panel.setStyleSheet("background: transparent;")



    # Creacion de FACHADA para reducir acoplamiento

    def set_file_name(self, file_name: str):
        self._file_card.set_file_name(file_name)
    
    def set_bank(self, bank: str):
        self._file_card.set_bank(bank)

    def set_status(self, status: str):
        self._file_card.set_status(status)
    
    def set_process_enabled(self, enabled: bool):
        self._action_bar.set_process_enabled(enabled)
    
    def set_export_enabled(self, enabled: bool):
        self._action_bar.set_export_enabled(enabled)

    def set_review_enabled(self, enabled):
        self._action_bar.set_review_enabled(enabled)
    
    def update_stats(self, stats):
        self._summary_panel.update_stats(stats)
    
    def append_log(self, message: str):
        self._log_panel.append_log(message)

    def clear_log(self):
        self._log_panel.clear()

    def load_pdf(self, pdf_path):
        self._pdf_viewer.load_pdf(pdf_path)

    
    

    

        
from PySide6.QtWidgets import QWidget, QVBoxLayout

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

        self._file_card = FileCard()
        self._action_bar = ActionBar()
        self._summary_panel = SummaryPanel()
        self._log_panel = LogPanel()

    def _create_layout(self):

        layout = QVBoxLayout()

        # QSS
        #------------------------------------------
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        #------------------------------------------
        
        layout.addWidget(self._file_card)
        layout.addWidget(self._action_bar)
        layout.addWidget(self._summary_panel)
        layout.addWidget(self._log_panel)

        self.setLayout(layout)

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
    
    def update_stats(self, stats):
        self._summary_panel.update_stats(stats)
    
    def append_log(self, message: str):
        self._log_panel.append_log(message)

    def clear_log(self):
        self._log_panel.clear()

    
    

    

        
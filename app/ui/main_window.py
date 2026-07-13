from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QStackedWidget
)

from app.ui.widgets.sidebar import Sidebar
from app.ui.views.converter_view import ConverterView
from app.ui.views.history_view import HistoryView
from app.ui.views.settings_view import SettingsView
from app.ui.views.review_view import ReviewView


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self._setup_window()
        self._create_widgets()
        self._create_layout()
        self._connect_signals()

    def _setup_window(self):
        self.setWindowTitle("ASIENTO")
        self.resize(1200, 700)

    def _connect_signals(self):

        self._sidebar.navigate.connect(self._stacked_widget.setCurrentIndex)

    def _create_widgets(self):

        self._central_widget = QWidget()

        self._sidebar = Sidebar()

        self._stacked_widget = QStackedWidget()


        self._converter_view = ConverterView()
        self._review_view = ReviewView()
        self._history_view = HistoryView()
        self._settings_view = SettingsView()

        self._stacked_widget.addWidget(self._converter_view)
        self._stacked_widget.addWidget(self._review_view)
        self._stacked_widget.addWidget(self._history_view)
        self._stacked_widget.addWidget(self._settings_view)

    def _create_layout(self):

        self.setCentralWidget(self._central_widget)

        layout = QHBoxLayout()

        layout.addWidget(self._sidebar)
        layout.addWidget(self._stacked_widget)

        self._central_widget.setLayout(layout)


    def show_converter_view(self):

        self._stacked_widget.setCurrentWidget(self._converter_view)

    def show_review_view(self):

        self._stacked_widget.setCurrentWidget(self._review_view)

    def show_history_view(self):

        self._stacked_widget.setCurrentWidget(self._history_view)

    def show_settings_view(self):

        self._stacked_widget.setCurrentWidget(self._settings_view)
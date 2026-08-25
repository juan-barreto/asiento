from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QStackedWidget
)

from PySide6.QtGui import QIcon
from app.utils.resource_path import resource_path

from app.ui.widgets.sidebar import Sidebar
from app.ui.views.converter_view import ConverterView
from app.ui.views.history_view import HistoryView
from app.ui.views.settings_view import SettingsView
from app.ui.views.review_view import ReviewView
from app.ui.views.export_view import ExportView
from PySide6.QtGui import QIcon
from app.ui.views.templates_view import TemplateEditorView
from app.ui.widgets.background_widget import BackgroundWidget

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        

        self._setup_window()
        self._create_widgets()
        self._create_layout()
        self._connect_signals()

    def _setup_window(self):
        self.setWindowTitle("ASIENTO Studio® ")
        self.resize(1200, 700)
        self.setWindowIcon(
                    QIcon(
                        str(
                            resource_path("app/resources/icons/asiento.ico")
                        )
                    )
                )

    def _connect_signals(self):

        self._sidebar.navigate.connect(self._stacked_widget.setCurrentIndex)

    def _create_widgets(self):

        self._central_widget = BackgroundWidget()  
        self._central_widget.setObjectName("mainContent")

        self._sidebar = Sidebar()

        self._stacked_widget = QStackedWidget()

        self._sidebar = Sidebar()
        self._sidebar.setObjectName("sidebar")

        self._stacked_widget = QStackedWidget()
        self._stacked_widget.setObjectName("stackArea")

        self._converter_view = ConverterView()
        self._converter_view.setObjectName("converterView")

        self._review_view = ReviewView()
        self._review_view.setObjectName("reviewView")

        self._history_view = HistoryView()
        self._history_view.setObjectName("historyView")

        self._settings_view = SettingsView()
        self._settings_view.setObjectName("settingsView")

        self._export_view = ExportView()
        self._export_view.setObjectName("exportView")

        self._template_editor_view = TemplateEditorView()
        self._template_editor_view.setObjectName("templateEditorView")

        self._stacked_widget.addWidget(self._converter_view)
        self._stacked_widget.addWidget(self._review_view)
        self._stacked_widget.addWidget(self._history_view)
        self._stacked_widget.addWidget(self._export_view)
        self._stacked_widget.addWidget(self._settings_view)
        self._stacked_widget.addWidget(self._template_editor_view)

        

        

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

    def show_export_view(self):
    
            self._stacked_widget.setCurrentWidget(self._export_view)

    def show_template_editor_view(self):

        self._stacked_widget.setCurrentWidget(self._template_editor_view)

        
if __name__ == "__main__":

    icon_path = resource_path("app/resources/icons/asiento.ico")

    print(icon_path)
    print(icon_path.exists())
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QListWidget,
    QListWidgetItem
)

from app.models.template import TemplateColumn, TemplateConfig
from app.ui.widgets.template_widget import TemplateColumnWidget


class TemplateEditorView(QWidget):

    save_requested = Signal()
    cancel_requested = Signal()

    def __init__(self):
        super().__init__()

        self.setObjectName("templateEditorView")

        self._create_widgets()
        self._create_layout()
        self._connect_signals()

    def _create_widgets(self):

        self._title = QLabel("Editar plantilla")
        self._title.setObjectName("templateEditorTitle")

        self._subtitle = QLabel(
            "Definí cómo querés organizar los datos del archivo exportado."
        )
        self._subtitle.setObjectName(
            "templateEditorSubtitle"
        )

        
        # Nombre de plantilla
        

        self._name_label = QLabel(
            "Nombre de la plantilla"
        )
        self._name_label.setObjectName(
            "templateFieldLabel"
        )

        self._name_input = QLineEdit()
        self._name_input.setObjectName(
            "templateNameInput"
        )

        self._name_input.setPlaceholderText(
            "Ej. Estudio contable"
        )

        # Columnas

        self._columns_label = QLabel(
            "Columnas del archivo"
        )
        self._columns_label.setObjectName(
            "templateFieldLabel"
        )

        self._columns_list = QListWidget()
        self._columns_list.setObjectName(
            "templateColumnsList"
        )

        # boton columnas

        self._add_column_button = QPushButton(
            "+ Agregar columna"
        )
        self._add_column_button.setObjectName(
            "addTemplateColumnButton"
        )


     

        self._cancel_button = QPushButton(
            "Cancelar"
        )
        self._cancel_button.setObjectName(
            "cancelTemplateButton"
        )

        self._save_button = QPushButton(
            "Guardar plantilla"
        )
        self._save_button.setObjectName(
            "saveTemplateButton"
        )

    def _create_layout(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(
            32,
            28,
            32,
            28
        )

        layout.setSpacing(8)

        layout.addWidget(
            self._title
        )

        layout.addWidget(
            self._subtitle
        )

        layout.addSpacing(20)

        card = QWidget()
        card.setObjectName(
            "templateEditorCard"
        )

        card_layout = QVBoxLayout()

        card_layout.setContentsMargins(
            24,
            24,
            24,
            24
        )

        card_layout.setSpacing(8)


        card_layout.addWidget(
            self._name_label
        )

        card_layout.addWidget(
            self._name_input
        )

        card_layout.addSpacing(18)

    

        card_layout.addWidget(
            self._columns_label
        )

        card_layout.addWidget(
            self._columns_list
        )

        card_layout.addSpacing(8)

        card_layout.addWidget(
            self._add_column_button
        )

        card.setLayout(
            card_layout
        )

        layout.addWidget(
            card
        )

        layout.addStretch()

    

        button_layout = QHBoxLayout()

        button_layout.setSpacing(10)

        button_layout.addStretch()

        button_layout.addWidget(
            self._cancel_button
        )

        button_layout.addWidget(
            self._save_button
        )

        layout.addLayout(
            button_layout
        )

        self.setLayout(
            layout
        )

    def _connect_signals(self):

        self._save_button.clicked.connect(
            self.save_requested.emit
        )

        self._cancel_button.clicked.connect(
            self.cancel_requested.emit
        )

    def load_config(self, config: TemplateConfig):

        self._name_input.setText(config.name)
        self._columns_list.clear()

        for column in config.columns:

            item = QListWidgetItem(self._columns_list)
            widget = TemplateColumnWidget(column)

            self._columns_list.addItem(item)
            self._columns_list.setItemWidget(item, widget)
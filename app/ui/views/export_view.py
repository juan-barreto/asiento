from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QLineEdit,
    QPushButton,
)


class ExportView(QWidget):

    export_requested = Signal()
    cancel_requested = Signal()
    edit_template_requested = Signal()

    def __init__(self):
        super().__init__()

        self.setObjectName("exportView")

        self._create_widgets()
        self._create_layout()
        self._connect_signals()

    def _create_widgets(self):

        # =====================================================
        # HEADER
        # =====================================================

        self._title = QLabel("Exportar")
        self._title.setObjectName("exportTitle")

        self._subtitle = QLabel(
            "Elegí cómo querés generar tu archivo."
        )
        self._subtitle.setObjectName("exportSubtitle")

        # =====================================================
        # TEMPLATE
        # =====================================================

        self._template_label = QLabel("Plantilla")
        self._template_label.setObjectName(
            "exportFieldLabel"
        )

        self._template_combo = QComboBox()
        self._template_combo.setObjectName(
            "exportCombo"
        )

        self._template_combo.addItem(
            "Estándar",
            "default"
        )

        # =====================================================
        # FORMAT
        # =====================================================

        self._format_label = QLabel("Formato")
        self._format_label.setObjectName(
            "exportFieldLabel"
        )

        self._format_combo = QComboBox()
        self._format_combo.setObjectName(
            "exportCombo"
        )

        self._format_combo.addItem(
            "Excel (.xlsx)",
            "xlsx"
        )

        # =====================================================
        # FILE NAME
        # =====================================================

        self._file_name_label = QLabel(
            "Nombre del archivo"
        )
        self._file_name_label.setObjectName(
            "exportFieldLabel"
        )

        self._file_name_input = QLineEdit()
        self._file_name_input.setObjectName(
            "exportFileName"
        )

        self._file_name_input.setPlaceholderText(
            "Nombre del archivo"
        )

        # =====================================================
        # TEMPLATE ACTION
        # =====================================================

        self._edit_button = QPushButton(
            "Editar plantilla"
        )

        self._edit_button.setObjectName(
            "editTemplateButton"
        )

        # =====================================================
        # ACTIONS
        # =====================================================

        self._cancel_button = QPushButton(
            "Cancelar"
        )

        self._cancel_button.setObjectName(
            "cancelExportButton"
        )

        self._export_button = QPushButton(
            "Exportar"
        )

        self._export_button.setObjectName(
            "exportButton"
        )

    def _create_layout(self):

        # =====================================================
        # MAIN LAYOUT
        # =====================================================

        layout = QVBoxLayout()

        layout.setContentsMargins(
            32,
            28,
            32,
            28
        )

        layout.setSpacing(8)

        # =====================================================
        # HEADER
        # =====================================================

        layout.addWidget(self._title)
        layout.addWidget(self._subtitle)

        layout.addSpacing(20)

        # =====================================================
        # EXPORT CARD
        # =====================================================

        card = QWidget()
        card.setObjectName("exportCard")

        card_layout = QVBoxLayout()

        card_layout.setContentsMargins(
            24,
            24,
            24,
            24
        )

        card_layout.setSpacing(8)

        # =====================================================
        # TEMPLATE
        # =====================================================

        card_layout.addWidget(
            self._template_label
        )

        card_layout.addWidget(
            self._template_combo
        )

        card_layout.addSpacing(12)

        # =====================================================
        # FORMAT
        # =====================================================

        card_layout.addWidget(
            self._format_label
        )

        card_layout.addWidget(
            self._format_combo
        )

        card_layout.addSpacing(12)

        # =====================================================
        # FILE NAME
        # =====================================================

        card_layout.addWidget(
            self._file_name_label
        )

        card_layout.addWidget(
            self._file_name_input
        )

        card_layout.addSpacing(16)

        # =====================================================
        # EDIT TEMPLATE
        # =====================================================

        edit_layout = QHBoxLayout()

        edit_layout.addWidget(
            self._edit_button
        )

        edit_layout.addStretch()

        card_layout.addLayout(
            edit_layout
        )

        card.setLayout(card_layout)

        layout.addWidget(card)

        layout.addStretch()

        # =====================================================
        # BOTTOM ACTIONS
        # =====================================================

        button_layout = QHBoxLayout()

        button_layout.setSpacing(10)

        button_layout.addStretch()

        button_layout.addWidget(
            self._cancel_button
        )

        button_layout.addWidget(
            self._export_button
        )

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def _connect_signals(self):

        self._export_button.clicked.connect(
            self.export_requested.emit
        )

        self._cancel_button.clicked.connect(
            self.cancel_requested.emit
        )

        self._edit_button.clicked.connect(
            self.edit_template_requested.emit
        )

    # =========================================================
    # PUBLIC API
    # =========================================================

    def set_file_name(self, file_name):

        self._file_name_input.setText(
            file_name
        )

    def get_file_name(self):

        return self._file_name_input.text().strip()

    def get_selected_template(self):

        return self._template_combo.currentData()

    def get_selected_format(self):

        return self._format_combo.currentData()
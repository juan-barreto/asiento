from PySide6 import QtCore
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QIcon, QPixmap
from app.utils.resource_path import resource_path
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QLineEdit,
    QPushButton,
    QMessageBox,
)
from app.ui.widgets.icon_button import IconButton


class ExportView(QWidget):

    export_requested = Signal()
    cancel_requested = Signal()
    create_template_requested = Signal()
    edit_template_requested = Signal(object)
    template_delete_requested = Signal(int)

    def __init__(self):
        super().__init__()

        self.setObjectName("exportView")

        self._create_widgets()
        self._create_layout()
        self._connect_signals()
        
        self._update_delete_button()

    def _create_widgets(self):


        self._title = QLabel("Exportar")
        self._title.setObjectName("exportTitle")

        self._subtitle = QLabel(
            "Elegí cómo querés generar tu archivo."
        )
        self._subtitle.setObjectName("exportSubtitle")

     

        self._template_label = QLabel("Plantilla")
        self._template_label.setObjectName(
            "exportFieldLabel"
        )

        self._template_combo = QComboBox()
        self._template_combo.setObjectName(
            "exportCombo"
        )





  

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

        self._create_button = QPushButton(
            "+ Crear plantilla"
        )

        self._create_button.setObjectName(
                    "createTemplateButton"
                )

        self._edit_button = QPushButton(
            "Editar plantilla"
        )

        self._edit_button.setObjectName(
            "editTemplateButton"
        )


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

        self._delete_button = IconButton(
        resource_path("app/resources/icons/tacho.png"),
        resource_path("app/resources/icons/tacho_blanco.png")
        )
        self._delete_button.setObjectName(
            "deleteTemplateButton"
        )
        self._delete_button.setFixedSize(36, 36)
        self._delete_button.setIconSize(QtCore.QSize(22, 22))
        self._delete_button.setToolTip("Eliminar plantilla")
        self._delete_button.setCursor(Qt.PointingHandCursor)

    def _create_layout(self):

     
        layout = QVBoxLayout()

        layout.setContentsMargins(
            32,
            28,
            32,
            28
        )

        layout.setSpacing(8)

    
        layout.addWidget(self._title)
        layout.addWidget(self._subtitle)

        layout.addSpacing(12)


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

        card_layout.addWidget(
            self._template_label
        )

        template_layout = QHBoxLayout()

        template_layout.addWidget(
            self._template_combo
        )

        template_layout.addWidget(
            self._delete_button
        )

        card_layout.addLayout(
            template_layout
        )

        card_layout.addSpacing(12)

  

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

  

        button_layout = QHBoxLayout()

        button_layout.setSpacing(10)

        button_layout.addStretch()

        button_layout.addWidget(
            self._cancel_button
        )

        button_layout.addWidget(
            self._create_button
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

        self._create_button.clicked.connect(
            self.create_template_requested.emit
        )

        self._cancel_button.clicked.connect(
            self.cancel_requested.emit
        )

        self._edit_button.clicked.connect(
            self._emit_edit_template
        )

        self._delete_button.clicked.connect(
            self._delete_selected_template
        )

        self._template_combo.currentIndexChanged.connect(
            self._update_delete_button
        )

    def _update_delete_button(self):

        template_id = self._template_combo.currentData()

        self._delete_button.setEnabled(
            isinstance(template_id, int)
        )
       

    def _emit_edit_template(self):
        template_id = self.get_selected_template()
        self.edit_template_requested.emit(template_id)

    def set_file_name(self, file_name):

        self._file_name_input.setText(
            file_name
        )

    def get_file_name(self):

        return self._file_name_input.text().strip()

    def load_templates(self, templates, selected_id=None):

        self._template_combo.clear()

        self._template_combo.addItem(
            "Estándar",
            "default"
        )

        for template in templates:

            self._template_combo.addItem(
                template["config"].name,
                template["id"]
            )

        if selected_id is not None:

            index = self._template_combo.findData(
                selected_id
        )

            if index != -1:
                self._template_combo.setCurrentIndex(index)

                
    def get_selected_template(self):

        return self._template_combo.currentData()

    def get_selected_format(self):

        return self._format_combo.currentData()

    def _delete_selected_template(self):

        template_id = self._template_combo.currentData()

        if not isinstance(template_id, int):
            return

        reply = QMessageBox.question(
            self,
            "Eliminar plantilla",
            "¿Estás seguro de que querés eliminar esta plantilla?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        self.template_delete_requested.emit(
            template_id
        )
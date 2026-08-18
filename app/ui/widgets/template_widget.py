from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QCheckBox,
)



class TemplateColumnWidget(QWidget):
    changed = Signal()
    removed = Signal()

    def __init__(self, column):
        super().__init__()
        self._column = column

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)

        self._drag_label = QLabel("☰")

        self._enabled_checkbox = QCheckBox()
        self._enabled_checkbox.setChecked(getattr(column, "enabled", True))

        self._field_label = QLabel(column.source)

        self._title_input = QLineEdit(column.title)
        self._title_input.setPlaceholderText("Encabezado")

        self._remove_button = QPushButton("✕")
        self._remove_button.setFixedWidth(30)
        self._remove_button.setObjectName("removeColumnButton")

        layout.addWidget(self._drag_label)
        layout.addWidget(self._enabled_checkbox)
        layout.addWidget(self._field_label)
        layout.addWidget(self._title_input)
        layout.addWidget(self._remove_button)

        self._enabled_checkbox.toggled.connect(self._on_changed)
        self._title_input.textChanged.connect(self._on_changed)
        self._remove_button.clicked.connect(self._on_removed)

    def _on_changed(self):
        self._column.enabled = self._enabled_checkbox.isChecked()
        self._column.title = self._title_input.text()
        self.changed.emit()

    def _on_removed(self):
        self.removed.emit()

    def get_column(self):
        return self._column

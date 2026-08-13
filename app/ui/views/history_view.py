from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QHeaderView,
    QAbstractItemView,
    QTableWidgetItem,
    QMenu
)

from PySide6.QtCore import Signal, Qt


class HistoryView(QWidget):

    open_pdf_requested = Signal(int)
    delete_requested = Signal(int)
    modify_requested = Signal(int)

    def __init__(self):
        super().__init__()

        self._create_widgets()
        self._configure_table()
        self._create_layout()
        self._connect_signals()

    def _create_widgets(self):

        self._table = QTableWidget()
        self._table.setObjectName("historyTable")

    def _configure_table(self):

        self._table.setColumnCount(9)

        self._table.setHorizontalHeaderLabels([
            "ID",
            "Procesado",
            "Desde",
            "Hasta",
            "Archivo",
            "Banco",
            "Movimientos",
            "Seguros",
            "Revisar"
        ])

        header = self._table.horizontalHeader()

        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            3,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            4,
            QHeaderView.Stretch
        )

        header.setSectionResizeMode(
            5,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            6,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            7,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            8,
            QHeaderView.ResizeToContents
        )

        self._table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self._table.setSelectionMode(
            QAbstractItemView.SingleSelection
        )

        self._table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self._table.setAlternatingRowColors(True)

        self._table.setSortingEnabled(True)

        # Permite utilizar un menú contextual con click derecho
        self._table.setContextMenuPolicy(
            Qt.CustomContextMenu
        )

    def _create_layout(self):

        layout = QVBoxLayout()

        layout.addWidget(self._table)

        self.setLayout(layout)

    def _connect_signals(self):

        self._table.cellDoubleClicked.connect(
            self._on_double_click
        )

        self._table.customContextMenuRequested.connect(
            self._show_context_menu
        )

    def load_results(self, resultados):

        self._table.setSortingEnabled(False)

        self._table.clearContents()

        self._table.setRowCount(len(resultados))

        for fila, resultado in enumerate(resultados):

            valores = [

                resultado["id"],
                resultado["fecha"],
                resultado["fecha_inicial"],
                resultado["fecha_final"],
                resultado["nombre_archivo"],
                resultado["banco"],
                resultado["movimientos"],
                resultado["seguros"],
                resultado["revisar"]

            ]

            for columna, valor in enumerate(valores):

                item = QTableWidgetItem(str(valor))

                self._table.setItem(
                    fila,
                    columna,
                    item
                )

        self._table.setSortingEnabled(True)

    def _on_double_click(self, row, _):

        item = self._table.item(row, 0)

        if item is None:
            return

        conversion_id = int(item.text())

        self.open_pdf_requested.emit(
            conversion_id
        )

    def _show_context_menu(self, position):

        item = self._table.itemAt(position)

        if item is None:
            return

        row = item.row()

        id_item = self._table.item(row, 0)

        if id_item is None:
            return

        conversion_id = int(id_item.text())

        menu = QMenu(self)

        open_action = menu.addAction(
            "Abrir PDF"
        )

        delete_action = menu.addAction(
            "Eliminar"
        )

        modify_action = menu.addAction(
                    "Editar movimientos"
                )
        action = menu.exec(
            self._table.viewport().mapToGlobal(position)
        )

        if action == open_action:

            self.open_pdf_requested.emit(
                conversion_id
            )

        elif action == delete_action:

            self.delete_requested.emit(
                conversion_id
            )

        elif action == modify_action:

            self.modify_requested.emit(
                conversion_id
            )
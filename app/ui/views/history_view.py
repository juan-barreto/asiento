from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QHeaderView,
    QAbstractItemView,
    QTableWidgetItem
)

from PySide6.QtCore import Signal


class HistoryView(QWidget):

    open_pdf_requested = Signal(int)

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

    def _create_layout(self):

        layout = QVBoxLayout()

        layout.addWidget(self._table)

        self.setLayout(layout)

    def _connect_signals(self):

        self._table.cellDoubleClicked.connect(
        self._on_double_click
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
                resultado["archivo"],
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

    def _on_double_click(self, row, column):

        item = self._table.item(row, 0)

        if item is None:
            return

        conversion_id = int(item.text())

        self.open_pdf_requested.emit(
            conversion_id
        )
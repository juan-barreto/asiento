from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QHeaderView,
    QAbstractItemView
)
from PySide6.QtCore import Qt, Signal

from app.services.movimiento import Movimiento


class ReviewView(QWidget):

    back = Signal()
    save = Signal()

    def __init__(self):
        super().__init__()

        self._create_widgets()
        self._create_layout()
        self._connect_signals()

    def _create_widgets(self):

        self._title = QLabel("Revisión de movimientos")

        self._subtitle = QLabel(
            "Movimientos que requieren revisión manual."
        )

        self._table = QTableWidget()

        self._table.setColumnCount(7)
        
        self._table.setHorizontalHeaderLabels([
            "Fecha",
            "Descripción",
            "Detalle",
            "Crédito",
            "Débito",
            "Saldo",
            "Confianza"
        ])
        self._table.horizontalHeader().setSectionResizeMode(
        QHeaderView.Stretch
        )

        self._table.verticalHeader().setVisible(False)

        self._table.verticalHeader().setDefaultSectionSize(34)

        self._table.setSelectionBehavior(
        QAbstractItemView.SelectRows
        )

        self._table.setSelectionMode(
        QAbstractItemView.SingleSelection
        )

        self._btn_back = QPushButton("Volver")

        self._btn_save = QPushButton("Guardar")

    def _create_layout(self):

        main_layout = QVBoxLayout()

        main_layout.addWidget(self._title)
        main_layout.addWidget(self._subtitle)

        main_layout.addWidget(self._table)

        button_layout = QHBoxLayout()

        button_layout.addStretch()

        button_layout.addWidget(self._btn_back)
        button_layout.addWidget(self._btn_save)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def _connect_signals(self):

        self._btn_back.clicked.connect(self.back.emit)
        self._btn_save.clicked.connect(self.save.emit)


    def load_movements(self, movimientos):

        self._table.setRowCount(len(movimientos))

        for row, movimiento in enumerate(movimientos):

            self._table.setItem(
                row,
                0,
                QTableWidgetItem(movimiento.fecha)
            )


            self._table.setItem(
                row,
                1,
                QTableWidgetItem(movimiento.descripcion)
            )

            self._table.setItem(
                row,
                2,
                QTableWidgetItem(movimiento.detalle)
            )

            credito = QTableWidgetItem(f"{movimiento.credito:,.2f}")
            credito.setFlags(credito.flags() & ~Qt.ItemIsEditable)
            credito.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self._table.setItem(row, 3, credito)

            debito = QTableWidgetItem(f"{movimiento.debito:,.2f}")
            debito.setFlags(debito.flags() & ~Qt.ItemIsEditable)
            debito.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self._table.setItem(row, 4, debito)

            saldo = QTableWidgetItem(f"{movimiento.saldo:,.2f}")
            saldo.setFlags(saldo.flags() & ~Qt.ItemIsEditable)
            saldo.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self._table.setItem(row, 5, saldo)

            confianza = QTableWidgetItem(f"{movimiento.confidence:.2f}")
            confianza.setFlags(confianza.flags() & ~Qt.ItemIsEditable)
            confianza.setTextAlignment(Qt.AlignCenter)
            self._table.setItem(row, 6, confianza)


    def set_review_count(self, total: int):

        self._subtitle.setText(
            f"Se encontraron {total} movimientos para revisar."
        )

    def get_movements(self) -> list[Movimiento]:

        movimientos = []

        for row in range(self._table.rowCount()):

            movimiento = Movimiento(

                fecha=self._table.item(row, 0).text(),

                descripcion=self._table.item(row, 1).text(),

                detalle=self._table.item(row, 2).text(),

                credito=float(self._table.item(row, 3).text()),

                debito=float(self._table.item(row, 4).text()),

                saldo=float(self._table.item(row, 5).text()),

                confidence=float(self._table.item(row, 6).text())

            )

            movimientos.append(movimiento)

        return movimientos
    

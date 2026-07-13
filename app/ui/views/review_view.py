from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout
)


class ReviewView(QWidget):

    def __init__(self):
        super().__init__()

        self._create_widgets()
        self._create_layout()

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

            self._table.setItem(
                row,
                3,
                QTableWidgetItem(str(movimiento.credito))
            )

            self._table.setItem(
                row,
                4,
                QTableWidgetItem(str(movimiento.debito))
            )

            self._table.setItem(
                row,
                5,
                QTableWidgetItem(str(movimiento.saldo))
            )

            self._table.setItem(
                row,
                6,
                QTableWidgetItem(f"{movimiento.confidence:.2f}")
            )

    def set_review_count(self, total: int):

        self._subtitle.setText(
            f"Se encontraron {total} movimientos para revisar."
        )
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QHeaderView,
    QAbstractItemView,
    QMessageBox,
    QMenu
)

from PySide6.QtCore import Qt, Signal

from app.services.movimiento import Movimiento


class ReviewView(QWidget):

    back = Signal()
    save = Signal(list)

    def __init__(self):
        super().__init__()

        self._movimientos_originales = {}
        self._movimientos_dudosos = set()

        self._create_widgets()
        self._create_layout()
        self._connect_signals()

    def _create_widgets(self):

        self._title = QLabel("Revisión de movimientos")

        self._subtitle = QLabel(
            "Movimientos detectados por ASIENTO. "
            "Los movimientos dudosos aparecen resaltados."
        )

        self._table = QTableWidget()
        self._table.setObjectName("reviewTable")
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

        self._table.setContextMenuPolicy(
            Qt.CustomContextMenu
        )

        self._btn_back = QPushButton("Volver")
        self._btn_save = QPushButton("Guardar")
        self._btn_reset = QPushButton("Restaurar todos")

    def _create_layout(self):

        main_layout = QVBoxLayout()

        main_layout.addWidget(self._title)
        main_layout.addWidget(self._subtitle)
        main_layout.addWidget(self._table)

        button_layout = QHBoxLayout()

        button_layout.addWidget(self._btn_reset)
        button_layout.addStretch()
        button_layout.addWidget(self._btn_back)
        button_layout.addWidget(self._btn_save)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def _connect_signals(self):

        self._btn_back.clicked.connect(self.back.emit)
        self._btn_save.clicked.connect(self._on_save)
        self._btn_reset.clicked.connect(self._restore_all)

        self._table.customContextMenuRequested.connect(
            self._show_context_menu
        )

    def load_movements(self, movimientos, dudosos=None):

        dudosos = dudosos or []

        self._movimientos_originales.clear()
        self._movimientos_dudosos.clear()

        for movimiento in dudosos:
            self._movimientos_dudosos.add(movimiento.id)

        self._table.setRowCount(len(movimientos))

        for row, movimiento in enumerate(movimientos):

            self._movimientos_originales[movimiento.id] = (
                movimiento.model_copy(deep=True)
            )

            fecha = QTableWidgetItem(movimiento.fecha)
            fecha.setData(Qt.UserRole, movimiento.id)

            self._table.setItem(row, 0, fecha)

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

            credito = QTableWidgetItem(
                f"{movimiento.credito:,.2f}"
            )
            credito.setTextAlignment(
                Qt.AlignRight | Qt.AlignVCenter
            )
            self._table.setItem(row, 3, credito)

            debito = QTableWidgetItem(
                f"{movimiento.debito:,.2f}"
            )
            debito.setTextAlignment(
                Qt.AlignRight | Qt.AlignVCenter
            )
            self._table.setItem(row, 4, debito)

            saldo = QTableWidgetItem(
                f"{movimiento.saldo:,.2f}"
            )
            saldo.setTextAlignment(
                Qt.AlignRight | Qt.AlignVCenter
            )
            self._table.setItem(row, 5, saldo)

            confianza = QTableWidgetItem(
                f"{movimiento.confidence:.2f}"
            )
            confianza.setFlags(
                confianza.flags() & ~Qt.ItemIsEditable
            )
            confianza.setTextAlignment(Qt.AlignCenter)

            self._table.setItem(row, 6, confianza)

            if movimiento.id in self._movimientos_dudosos:
                self._highlight_row(row)

    def _highlight_row(self, row):

        for column in range(self._table.columnCount()):

            item = self._table.item(row, column)

            if item:
                item.setBackground(Qt.red)
                item.setForeground(Qt.white)

    def set_review_count(self, total: int):

        self._subtitle.setText(
            f"Se encontraron {total} movimientos "
            f"que ASIENTO recomienda revisar."
        )

    def _on_save(self):

        movimientos = self.get_movements()

        if self._has_safe_movements_modified(movimientos):

            if not self._confirm_save():
                return

        self.save.emit(movimientos)

    def _has_safe_movements_modified(self, movimientos):

        for movimiento in movimientos:

            if movimiento.id in self._movimientos_dudosos:
                continue

            original = self._movimientos_originales.get(
                movimiento.id
            )

            if original is None:
                continue

            if self._movement_changed(
                original,
                movimiento
            ):
                return True

        return False

    def _movement_changed(self, original, actual):

        return (
            original.fecha != actual.fecha
            or original.descripcion != actual.descripcion
            or original.detalle != actual.detalle
            or original.debito != actual.debito
            or original.credito != actual.credito
            or original.saldo != actual.saldo
        )

    def _confirm_save(self):

        message_box = QMessageBox(
            QMessageBox.Question,
            "Confirmar modificaciones",
            (
                "Modificaste uno o más movimientos "
                "que ASIENTO había considerado correctos.\n\n"
                "¿Deseás guardar las modificaciones?"
            ),
            parent=self
        )

        button_si = message_box.addButton(
            "Sí",
            QMessageBox.YesRole
        )

        button_no = message_box.addButton(
            "No",
            QMessageBox.NoRole
        )

        message_box.setDefaultButton(button_no)
        message_box.exec()

        return message_box.clickedButton() == button_si

    def _restore_all(self):

        message_box = QMessageBox(
            QMessageBox.Question,
            "Restaurar movimientos",
            (
                "¿Deseás restaurar todos los movimientos "
                "a su estado original?"
            ),
            parent=self
        )

        button_si = message_box.addButton(
            "Sí",
            QMessageBox.YesRole
        )

        button_no = message_box.addButton(
            "No",
            QMessageBox.NoRole
        )

        message_box.setDefaultButton(button_no)
        message_box.exec()

        if message_box.clickedButton() != button_si:
            return

        for row in range(self._table.rowCount()):

            movement_id = self._table.item(
                row, 0
            ).data(Qt.UserRole)

            original = self._movimientos_originales.get(
                movement_id
            )

            if original is None:
                continue

            self._set_row_from_movement(
                row,
                original
            )

    def _restore_row(self, row):

        movement_id = self._table.item(
            row, 0
        ).data(Qt.UserRole)

        original = self._movimientos_originales.get(
            movement_id
        )

        if original is None:
            return

        self._set_row_from_movement(
            row,
            original
        )

    def _set_row_from_movement(self, row, movimiento):

        self._table.item(
            row, 0
        ).setText(movimiento.fecha)

        self._table.item(
            row, 1
        ).setText(movimiento.descripcion)

        self._table.item(
            row, 2
        ).setText(movimiento.detalle)

        self._table.item(
            row, 3
        ).setText(f"{movimiento.credito:,.2f}")

        self._table.item(
            row, 4
        ).setText(f"{movimiento.debito:,.2f}")

        self._table.item(
            row, 5
        ).setText(f"{movimiento.saldo:,.2f}")

        self._table.item(
            row, 6
        ).setText(f"{movimiento.confidence:.2f}")

    def get_movements(self) -> list[Movimiento]:

        movimientos = []

        for row in range(self._table.rowCount()):

            movement_id = self._table.item(
                row, 0
            ).data(Qt.UserRole)

            original = self._movimientos_originales[
                movement_id
            ]

            credito = float(
                self._table.item(
                    row, 3
                ).text().replace(",", "")
            )

            debito = float(
                self._table.item(
                    row, 4
                ).text().replace(",", "")
            )

            saldo = float(
                self._table.item(
                    row, 5
                ).text().replace(",", "")
            )

            movimiento = Movimiento(
                id=movement_id,
                fecha=self._table.item(
                    row, 0
                ).text(),
                descripcion=self._table.item(
                    row, 1
                ).text(),
                detalle=self._table.item(
                    row, 2
                ).text(),
                credito=credito,
                debito=debito,
                saldo=saldo,
                confidence=original.confidence
            )

            movimientos.append(movimiento)

        return movimientos

    def _show_context_menu(self, position):

        item = self._table.itemAt(position)

        if item is None:
            return

        row = item.row()

        menu = QMenu(self)

        restore_action = menu.addAction(
            "Restaurar movimiento"
        )

        action = menu.exec(
            self._table.viewport().mapToGlobal(position)
        )

        if action != restore_action:
            return

        message_box = QMessageBox(
            QMessageBox.Question,
            "Restaurar movimiento",
            (
                "¿Deseás restaurar este movimiento "
                "a sus valores originales?"
            ),
            parent=self
        )

        button_si = message_box.addButton(
            "Sí",
            QMessageBox.YesRole
        )

        button_no = message_box.addButton(
            "No",
            QMessageBox.NoRole
        )

        message_box.setDefaultButton(button_no)
        message_box.exec()

        if message_box.clickedButton() == button_si:
            self._restore_row(row)
from PySide6.QtWidgets import QWidget, QHBoxLayout

from app.ui.widgets.metric_card import MetricCard


class SummaryPanel(QWidget):

    def __init__(self):

        super().__init__()

        self._create_widgets()
        self._create_layout()

    def _create_widgets(self):

        self._movements_card = MetricCard("Movimientos")
        self._insurance_card = MetricCard("Seguros")
        self._review_card = MetricCard("Revisar")

    def _create_layout(self):

        layout = QHBoxLayout()

        layout.addWidget(self._movements_card)
        layout.addWidget(self._insurance_card)
        layout.addWidget(self._review_card)


        self.setLayout(layout)

    # Métodos públicos para obtener el valor de cada sección

    def update_stats(self, stats):

        self._movements_card.set_value(stats.total_movimientos)
        self._insurance_card.set_value(stats.total_seguros)
        self._review_card.set_value(stats.total_revisar)

        
from pathlib import Path

from PySide6.QtCore import QThread
from PySide6.QtWidgets import QFileDialog

from app.exporters.xl_exporter import conversion_excel
from app.ui.main_window import MainWindow
from app.workers.extract_worker import ExtractWorker


class MainController:

    def __init__(self, window: MainWindow):

        self._window = window

        self._selected_pdf = None
        self._resultado = None

        self._thread = None
        self._worker = None

        self._connect_signals()

    
    def _connect_signals(self):

        self._window._converter_view._action_bar.select_pdf.connect(self._select_pdf)

        self._window._converter_view._action_bar.process.connect(self._process_pdf)

        self._window._converter_view._action_bar.export.connect(self._export_excel)

    
    def _select_pdf(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self._window,
            "Seleccionar PDF",
            "",
            "PDF Files (*.pdf)"
        )

        if not file_path:
            return
        
        self._selected_pdf = file_path

        file_name = Path(file_path).name

        self._window._converter_view.set_file_name(file_name)
        self._window._converter_view.set_status("Archivo seleccionado")
        self._window._converter_view.set_process_enabled(True)

    def _process_pdf(self):

        self._window._converter_view.set_status("Procesando...")
        self._window._converter_view.set_process_enabled(False)

        self._create_thread()

    def _export_excel(self):

        if self._resultado is None:
            return
        conversion_excel(self._resultado,
            callback=self._window._converter_view.append_log)

    def _processing_finished(self, resultado):

        self._resultado = resultado

        self._window._converter_view.set_status("Completado")
        self._window._converter_view.set_bank(resultado.banco)

        self._window._converter_view.update_stats(resultado.stats)

        self._window._converter_view.append_log("Proceso finalizado")
        self._window._converter_view.append_log(
            resultado.model_dump_json(indent=2)
        )     
        self._window._converter_view.append_log(str(resultado.stats))
        
        self._window._converter_view.set_export_enabled(True)

        if resultado.revisar:


            self._window._review_view.load_movements(resultado.revisar)

            self._window._review_view.set_review_count(
            len(resultado.revisar)
            )

            self._window.show_review_view()

    def _show_error(self, error: str):

        self._window._converter_view.set_status("Error")

        self._window._converter_view.append_log(error)

        self._window._converter_view.set_process_enabled(True)


    def _create_thread(self):

        self._thread = QThread()

        self._worker = ExtractWorker(self._selected_pdf)

        self._worker.moveToThread(self._thread)

        self._thread.started.connect(self._worker.run)

        self._worker.log.connect(self._window._converter_view.append_log)

        self._worker.finished.connect(self._processing_finished)

        self._worker.error.connect(self._show_error)

        self._worker.finished.connect(self._thread.quit)

        self._thread.finished.connect(self._thread.deleteLater)

        self._worker.finished.connect(self._worker.deleteLater)

        self._thread.start()




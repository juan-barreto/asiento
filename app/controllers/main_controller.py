from pathlib import Path

from PySide6.QtCore import QThread
from PySide6.QtWidgets import (
    QFileDialog,
    QMessageBox,
)

from app.ui.main_window import MainWindow
from app.workers.extract_worker import ExtractWorker
from app.services.database import Database
from app.ui.dialogs.pdf_viewer_dialog import PdfViewerDialog
from app.models.template import (
    TemplateConfig,
    TemplateColumn,
    AVAILABLE_COLUMNS
)
from app.exporters.xl_exporter import conversion_excel


class MainController:

    def __init__(self, window: MainWindow):

        self._window = window
        self._database = Database()

        self._window._sidebar.set_export_enabled(False)

       

        self._selected_pdf_path = None
        self._resultado = None
        self._conversion_id = None
        self._file_name = None

        

      
        self._editing_template_id = None

        

        self._thread = None
        self._worker = None

        

        self._pdf_viewer = None
        self._review_origin = None
        self._template_config = None

       

        self._connect_signals()
        self._load_history()
        self._load_templates()

    # SIGNALS
    

    def _connect_signals(self):

   

        self._window._converter_view._action_bar.select_pdf.connect(
            self._select_pdf
        )

        self._window._converter_view._action_bar.process.connect(
            self._process_pdf
        )

        self._window._converter_view._action_bar.export.connect(
            self._open_export_view
        )

        self._window._converter_view._action_bar.review.connect(
            self._open_review
        )

        

        self._window._export_view.export_requested.connect(
            self._export_conversion
        )

        self._window._export_view.cancel_requested.connect(
            self._cancel_export
        )

        self._window._export_view.edit_template_requested.connect(
            self._open_template_editor
        )

        self._window._export_view.template_delete_requested.connect(
            self._delete_template
        )

        # NUEVO: crear plantilla
        self._window._export_view.create_template_requested.connect(
            self._create_template
        )

      

        self._window._template_editor_view.save_requested.connect(
            self._save_template
        )

        self._window._template_editor_view.cancel_requested.connect(
            self._back_from_template
        )


        self._window._history_view.open_pdf_requested.connect(
            self._open_pdf_from_history
        )

        self._window._history_view.delete_requested.connect(
            self._delete_from_history
        )

        self._window._history_view.modify_requested.connect(
            self._modify_from_history
        )

        self._window._history_view.export_requested.connect(
            self._export_from_history
        )

        
    
        

        self._window._review_view.back.connect(
            self._back_from_review
        )

        self._window._review_view.save.connect(
            self._save_review
        )

        self._window._review_view.open_pdf_requested.connect(
            self._open_pdf_from_review
        )

  
    # TEMPLATES
    

    def _load_templates(self, selected_id = None):

        templates = self._database.get_templates()

        self._window._export_view.load_templates(
            templates,
            selected_id
        )

    def _create_default_template(self):

        if self._resultado is None:
            return None

        columns = [
            TemplateColumn(
                source=key,
                title=AVAILABLE_COLUMNS.get(key, key)
            )
            for key in self._resultado.movimientos[0]
                .model_dump()
                .keys()
            if key in AVAILABLE_COLUMNS
        ]

        return TemplateConfig(
            name="Estándar",
            format="xlsx",
            columns=columns
        )

    def _create_template(self):

        config = self._create_default_template()

        if config is None:
            return

        
        self._editing_template_id = None

        
        config.name = ""

        self._window._template_editor_view.load_config(
            config
        )

        self._window.show_template_editor_view()

    def _open_template_editor(self, template_id):

        self._editing_template_id = template_id

        if not isinstance(template_id, int):
            return

        config = self._database.get_template_by_id(
            template_id
        )

        if config is None:
            return

        # Estamos EDITANDO una existente
        self._editing_template_id = template_id

        self._window._template_editor_view.load_config(
            config
        )

        self._window.show_template_editor_view()

    def _save_template(self):

        config = self._window._template_editor_view.get_config()
        self._template_config = config

        template_id = self._editing_template_id
        nombre_nuevo = config.name.strip().lower()

    
        existing_templates = self._database.get_templates()
        for tpl in existing_templates:
            nombre_existente = tpl["config"].name.strip().lower()
            if nombre_existente == nombre_nuevo:
                if template_id is None or tpl["id"] != template_id:
                    QMessageBox.warning(
                        self._window,
                        "Nombre duplicado",
                        "Ya existe una plantilla con ese nombre."
                    )
                    return


        if template_id == "default" or template_id is None:

            new_id = self._database.save_new_template(config)

            self._load_templates(
                selected_id=new_id
            )

        else:

            self._database.update_template(
                template_id,
                config
            )

            self._load_templates(
                selected_id=template_id
            )

        self._window.show_export_view()

    def _delete_template(self, template_id: int):

        filas = self._database.delete_template(
            template_id
        ) or 0

        if filas == 0:
            return

        self._load_templates(template_id)

# EXPORTACION

    def _open_export_view(self):

        if self._resultado is None:
            return

        self._load_templates()

        self._window._export_view.set_file_name(
            self._file_name
        )

        self._window.show_export_view()

    def _export_conversion(self):

        if self._resultado is None:
            return

        file_name = (
            self._window._export_view
            .get_file_name()
        )

        if not file_name:
            QMessageBox.warning(
                self._window,
                "Nombre requerido",
                "Ingresá un nombre para el archivo."
            )
            return

        selected_format = (
            self._window._export_view
            .get_selected_format()
        )

        selected_template = (
            self._window._export_view
            .get_selected_template()
        )

        # Por ahora la lógica de exportación queda
        # separada de la creación/edición de plantillas.

        ruta, _ = QFileDialog.getSaveFileName(
            self._window,
            "Guardar archivo",
            f"{file_name}.{selected_format}",
            "Excel (*.xlsx)"
        )

        if not ruta:
            return

        config = self._database.get_template_by_id(
            selected_template
        )

        conversion_excel(
            self._resultado,
            ruta,
            config,
            callback=(
                self._window
                ._converter_view
                .append_log
            )
        )

    def _cancel_export(self):

        self._window.show_converter_view()

        self._window._sidebar.set_export_enabled(
            False
        )


    def _back_from_template(self):

        self._editing_template_id = None

        self._window.show_export_view()

    # REVIEW VIEW

    def _open_review(self):

        if self._resultado is None:
            return

        self._review_origin = "converter"

        self._window._review_view.load_movements(
            self._resultado.movimientos,
            self._resultado.revisar
        )

        self._window._review_view.set_review_count(
            len(self._resultado.revisar)
        )

        self._window.show_review_view()

    # SELECCIONAR PDF

    def _select_pdf(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self._window,
            "Seleccionar PDF",
            "",
            "PDF Files (*.pdf)"
        )

        if not file_path:
            return

        self._selected_pdf_path = file_path
        self._file_name = Path(file_path).name

        self._window._converter_view.set_file_name(
            self._file_name
        )

        self._window._converter_view.set_status(
            "Archivo seleccionado"
        )

        self._window._converter_view.set_process_enabled(
            True
        )
# BOTON PROCESAR

    def _process_pdf(self):

        self._window._converter_view.set_status(
            "Procesando..."
        )

        self._window._converter_view.set_process_enabled(
            False
        )

        self._create_thread()

   # PROCESAMIENTO

    def _processing_finished(self, resultado):

        conversion_id = self._database.save_result(
            resultado,
            self._file_name,
            self._selected_pdf_path
        )

        self._activate_conversion(
            conversion_id,
            resultado,
            self._selected_pdf_path,
            self._file_name
        )

        self._load_history()

        self._window._converter_view.set_status(
            "Completado"
        )

        self._window._converter_view.set_bank(
            resultado.banco
        )

        self._window._converter_view.update_stats(
            resultado.stats
        )

        self._window._converter_view.load_pdf(
            self._selected_pdf_path
        )

        self._window._converter_view.append_log(
            "Proceso finalizado"
        )

        self._window._converter_view.append_log(
            resultado.model_dump_json(
                indent=2
            )
        )

        self._window._converter_view.append_log(
            str(resultado.stats)
        )

        self._window._converter_view.set_export_enabled(
            True
        )

        self._window._converter_view.set_review_enabled(
            True
        )

        self._window._sidebar.set_export_enabled(
            True
        )

        if resultado.revisar:

            self._review_origin = "converter"

            self._open_review()

    def _show_error(self, error: str):

        self._window._converter_view.set_status(
            "Error"
        )

        self._window._converter_view.append_log(
            error
        )

        self._window._converter_view.set_process_enabled(
            True
        )

    # THREAD

    def _create_thread(self):

        self._thread = QThread()

        self._worker = ExtractWorker(
            self._selected_pdf_path
        )

        self._worker.moveToThread(
            self._thread
        )

        self._thread.started.connect(
            self._worker.run
        )

        self._worker.log.connect(
            self._window._converter_view.append_log
        )

        self._worker.finished.connect(
            self._processing_finished
        )

        self._worker.error.connect(
            self._show_error
        )

        self._worker.finished.connect(
            self._thread.quit
        )

        self._thread.finished.connect(
            self._thread.deleteLater
        )

        self._worker.finished.connect(
            self._worker.deleteLater
        )

        self._thread.start()

   # GUARDADO DEL REVIEW

    def _back_from_review(self):

        if self._review_origin == "history":

            self._window.show_history_view()

        else:

            self._window.show_converter_view()

    def _save_review(self, movimientos_editados):

        cantidad = len(
            self._resultado.revisar
        )

        self._resultado.movimientos = (
            movimientos_editados
        )

        self._resultado.seguros = (
            movimientos_editados
        )

        self._resultado.revisar = []

        self._resultado.stats.total_seguros = (
            len(self._resultado.seguros)
        )

        self._resultado.stats.total_revisar = (
            len(self._resultado.revisar)
        )

        self._database.update_result(
            self._conversion_id,
            self._resultado
        )

        if self._review_origin == "history":

            self._sync_converter_with_active_conversion()

            self._window.show_history_view()

        else:

            self._window._converter_view.update_stats(
                self._resultado.stats
            )

            self._window._converter_view.append_log(
                f"Se corrigieron manualmente "
                f"{cantidad} movimientos."
            )

            self._window._converter_view.append_log(
                "Movimientos revisados, guardados."
            )

            self._window._converter_view.set_status(
                "Listo para exportar"
            )

            self._window.show_converter_view()

        self._load_history()

    # HISTORIAL

    def _load_history(self):

        resultados = self._database.get_results()

        self._window._history_view.load_results(
            resultados
        )

    def _open_pdf_from_history(self, conversion_id):

        pdf_path = self._database.get_pdf_path(
            conversion_id
        )

        self._pdf_viewer = PdfViewerDialog(
            self._window
        )

        self._pdf_viewer.load_pdf(
            pdf_path
        )

        self._pdf_viewer.show()

    def _modify_from_history(self, conversion_id):

        resultado_json = (
            self._database.get_result_json(
                conversion_id
            )
        )

        if not resultado_json:
            return

        pdf_path = (
            self._database.get_pdf_path(
                conversion_id
            )
        )

        from app.services.movimiento import ResultadoPipeline

        resultado = (
            ResultadoPipeline.model_validate_json(
                resultado_json
            )
        )

        self._activate_conversion(
            conversion_id,
            resultado,
            pdf_path,
            Path(pdf_path).name
        )

        self._review_origin = "history"

        self._window._review_view.load_movements(
            resultado.movimientos,
            resultado.revisar
        )

        self._window._review_view.set_review_count(
            len(resultado.revisar)
        )

        self._window.show_review_view()

    def _export_from_history(self, conversion_id: int):
        
        resultado_json = self._database.get_result_json(conversion_id)
        if not resultado_json:
            return

        pdf_path = self._database.get_pdf_path(conversion_id)

        from app.services.movimiento import ResultadoPipeline
        resultado = ResultadoPipeline.model_validate_json(resultado_json)

        
        self._activate_conversion(
            conversion_id,
            resultado,
            pdf_path,
            Path(pdf_path).name
        )

        
        self._open_export_view()


    def _delete_from_history(self, conversion_id):

        message_box = QMessageBox(
            self._window
        )

        message_box.setWindowTitle(
            "Eliminar conversión"
        )

        message_box.setText(
            "¿Estás seguro de que querés "
            "eliminar esta conversión?"
        )

        yes_button = message_box.addButton(
            "Sí",
            QMessageBox.YesRole
        )

        no_button = message_box.addButton(
            "No",
            QMessageBox.NoRole
        )

        message_box.setDefaultButton(
            no_button
        )

        message_box.exec()

        if message_box.clickedButton() != yes_button:
            return

        filas = self._database.delete_result(
            conversion_id
        )

        if filas == 0:
            return

        self._load_history()

    def _open_pdf_from_review(self):

        self._open_pdf_from_history(
            self._conversion_id
        )

    # CONVERSION ACTIVA
    

    def _sync_converter_with_active_conversion(self):

        self._window._converter_view.set_file_name(
            self._file_name
        )

        self._window._converter_view.set_bank(
            self._resultado.banco
        )

        self._window._converter_view.set_status(
            "Listo para exportar"
        )

        self._window._converter_view.update_stats(
            self._resultado.stats
        )

        self._window._converter_view.load_pdf(
            self._selected_pdf_path
        )

        self._window._converter_view.set_export_enabled(
            True
        )

        self._window._converter_view.set_review_enabled(
            True
        )

    def _activate_conversion(
        self,
        conversion_id,
        resultado,
        pdf_path,
        file_name
    ):

        self._conversion_id = conversion_id
        self._resultado = resultado
        self._selected_pdf_path = pdf_path
        self._file_name = file_name
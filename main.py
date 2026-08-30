import sys
from PySide6.QtWidgets import QApplication 
from PySide6.QtGui import QIcon
from app.utils.resource_path import resource_path
from app.ui.widgets.splash_screen import SplashScreen

from pathlib import Path

from app.ui.main_window import MainWindow
from app.controllers.main_controller import MainController

# QApplication es el nucleo de mi app en Qt, maneja el loop de eventos (clicks, teclado ,etc
def main():
    app = QApplication(sys.argv)

    app.setWindowIcon(
        QIcon(
            str(
                resource_path("resources/icons/asiento.ico")
            )
        )
    )

    splash = SplashScreen()
    splash.show()

    app.processEvents()

    splash.set_status("Cargando interfaz...")
    splash.set_progress(30)
    app.processEvents()

    qss_path = resource_path("resources/qss/style.qss")

    with open(qss_path, "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())

    splash.set_status("Inicializando ASIENTO...")
    splash.set_progress(60)
    app.processEvents()

    window = MainWindow()

    splash.set_status("Preparando aplicación...")
    splash.set_progress(85)
    app.processEvents()

    controller = MainController(window)

    splash.set_progress(100)
    app.processEvents()

    window.show()

    splash.close()

    sys.exit(app.exec())




if __name__ == "__main__":

   main()
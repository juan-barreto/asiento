import sys
from PySide6.QtWidgets import QApplication 
from PySide6.QtGui import QIcon
from app.utils.resource_path import resource_path

from pathlib import Path

from app.ui.main_window import MainWindow
from app.controllers.main_controller import MainController

# QApplication es el nucleo de mi app en Qt, maneja el loop de eventos (clicks, teclado ,etc
def main():
   app = QApplication(sys.argv)
   app.setWindowIcon(
    QIcon(
        str(
            resource_path("app/resources/icons/asiento.ico")
        )
    )
      )

   qss_path = resource_path("app/resources/qss/style.qss")

   
      
   window = MainWindow()

   controller = MainController(window)

   with open(qss_path, "r", encoding="utf-8") as f:
         app.setStyleSheet(f.read())

   window.show()

   # Este es el evento en prueba donde mantiene la app activa esperando los eventos, sino esta esto la ventana se abriria y cerraria instantaneamente 
   sys.exit(app.exec())




if __name__ == "__main__":

   main()
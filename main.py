import sys
from PySide6.QtWidgets import QApplication 

from pathlib import Path

from app.ui.main_window import MainWindow
from app.controllers.main_controller import MainController

# QApplication es el nucleo de mi app en Qt, maneja el loop de eventos (clicks, teclado ,etc
def main():
   app = QApplication(sys.argv)

   qss_path = Path("app/resources/qss/style.qss")

   with open(qss_path, "r", encoding="utf-8") as f:
      app.setStyleSheet(f.read())
      
   window = MainWindow()

   controller = MainController(window)

   window.show()

   # Este es el evento en prueba donde mantiene la app activa esperando los eventos, sino esta esto la ventana se abriria y cerraria instantaneamente 
   sys.exit(app.exec())




if __name__ == "__main__":

   main()
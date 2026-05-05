# main.py
import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # Instanciar y mostrar la ventana principal
    window = MainWindow()
    window.show()
    
    # Ejecutar el ciclo de eventos de la aplicación
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
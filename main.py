from gui import OscilloscopeGUI
from PyQt6.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = OscilloscopeGUI()
    
    window.show()
    

    sys.exit(app.exec())

    








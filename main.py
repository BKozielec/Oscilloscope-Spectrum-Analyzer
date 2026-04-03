from gui import OscilloscopeGUI
from PyQt6.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    # 1. Tworzysz obiekt aplikacji (zarządca zdarzeń systemowych)
    app = QApplication(sys.argv)
    
    # 2. Tworzysz instancję swojego okna
    window = OscilloscopeGUI()
    
    # 3. Wyświetlasz okno (domyślnie są ukryte)
    window.show()
    
    # 4. Uruchamiasz pętlę i czekasz na zamknięcie (X)
    sys.exit(app.exec())

    








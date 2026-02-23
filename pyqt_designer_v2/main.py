import sys
import os

# Ensure backend can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from PyQt6.QtWidgets import QApplication, QMainWindow
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    from PyQt6.QtWebChannel import QWebChannel
    from PyQt6.QtCore import QUrl
    from PyQt6.QtGui import QColor, QPalette
    PYQT_VERSION = 6
except ImportError:
    from PyQt5.QtWidgets import QApplication, QMainWindow
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    from PyQt5.QtWebChannel import QWebChannel
    from PyQt5.QtCore import QUrl
    from PyQt5.QtGui import QColor, QPalette
    PYQT_VERSION = 5

from backend.bridge import DesignerBridge
from backend.server import run_server_in_thread

class MainWindow(QMainWindow):
    def __init__(self, port):
        super().__init__()
        self.setWindowTitle("PyQt Designer Pro V2")
        self.resize(1600, 900)

        self.browser = QWebEngineView()
        self.channel = QWebChannel()
        self.bridge = DesignerBridge()
        self.channel.registerObject('pyBridge', self.bridge)
        self.browser.page().setWebChannel(self.channel)

        self.setCentralWidget(self.browser)

        # Load local server URL
        # We serve the 'frontend' directory
        url = f"http://127.0.0.1:{port}/index.html"
        self.browser.setUrl(QUrl(url))

def main():
    app = QApplication(sys.argv)

    # Fusion Style & Dark Palette for the Host Window
    app.setStyle("Fusion")
    palette = app.palette()
    dark_gray = QColor(30, 30, 30)
    palette.setColor(QPalette.ColorRole.Window, dark_gray)
    palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
    app.setPalette(palette)

    # Start Server
    PORT = 8999
    # Root dir should be the frontend folder
    # Assuming main.py is in root (pyqt_designer_v2/), frontend is ./frontend
    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend')
    run_server_in_thread(PORT, root_dir)

    window = MainWindow(PORT)
    window.show()

    if PYQT_VERSION == 6:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()

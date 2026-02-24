import sys
import os

try:
    from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QWidget, QFrame, QStatusBar
    from PyQt6.QtCore import Qt, QRect
    from PyQt6 import uic
except ImportError:
    try:
        from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QWidget, QFrame, QStatusBar
        from PyQt5.QtCore import Qt, QRect
        from PyQt5 import uic
    except ImportError:
        print("Error: PyQt6 or PyQt5 is required.")
        sys.exit(1)

class AutoScaler(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)

        # Check Qt version
        self.is_qt6 = hasattr(QFrame, 'Shape')

        # Configure Frame
        if self.is_qt6:
            self.setFrameShape(QFrame.Shape.NoFrame)
            sb_off = Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        else:
            self.setFrameShape(QFrame.NoFrame)
            sb_off = Qt.ScrollBarAlwaysOff

        self.setVerticalScrollBarPolicy(sb_off)
        self.setHorizontalScrollBarPolicy(sb_off)
        self.setStyleSheet("background: transparent; border: 0px;")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.scene():
            if self.is_qt6:
                mode = Qt.AspectRatioMode.KeepAspectRatio
            else:
                mode = Qt.KeepAspectRatio
            self.fitInView(self.sceneRect(), mode)

class ScaleAwareLoader(QMainWindow):
    def __init__(self, ui_file):
        super().__init__()

        # Load UI
        try:
            temp_window = uic.loadUi(ui_file)
        except Exception as e:
            print(f"Error loading UI file: {e}")
            return

        # Extract metadata
        self.setWindowTitle(temp_window.windowTitle())
        self.resize(temp_window.size())

        # Find the container widget created by our generator ("design_container")
        container = temp_window.findChild(QWidget, "design_container")

        if not container:
            print("Warning: 'design_container' not found. Scaling logic may not work as intended.")
            # Try to use central widget directly
            if isinstance(temp_window, QMainWindow):
                container = temp_window.centralWidget()
            else:
                container = temp_window

        if container:
            # We need to detach container from temp_window
            container.setParent(None)

            # Create Scene matching original size
            w, h = container.width(), container.height()
            self.scene = QGraphicsScene(0, 0, w, h)
            self.scene.addWidget(container)

            # Setup View
            self.view = AutoScaler(self.scene)
            self.setCentralWidget(self.view)

            # Copy stylesheet
            self.setStyleSheet(temp_window.styleSheet())

            # Copy Status Bar if exists
            if isinstance(temp_window, QMainWindow) and temp_window.statusBar():
                self.setStatusBar(QStatusBar(self))
        else:
            print("Error: Could not find content to display.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python ui_loader.py <path_to_ui_file>")
        sys.exit(1)

    ui_path = sys.argv[1]
    if not os.path.exists(ui_path):
        print(f"Error: File not found: {ui_path}")
        sys.exit(1)

    app = QApplication(sys.argv)
    window = ScaleAwareLoader(ui_path)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

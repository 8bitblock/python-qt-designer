try:
    from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal
    from PyQt6.QtWidgets import QFileDialog
    PYQT_VERSION = 6
except ImportError:
    from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
    from PyQt5.QtWidgets import QFileDialog
    PYQT_VERSION = 5

import json
from .generator_ui import UIGenerator
from .generator_py import PythonGenerator

class DesignerBridge(QObject):
    ui_imported = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtSlot(str)
    def save_ui_file(self, data_json):
        data = json.loads(data_json)
        # Parse data
        elements = data.get('elements', [])
        meta = data.get('meta', {})
        canvas_size = meta.get('canvasSize', {'w':800, 'h':600})
        window_title = meta.get('windowTitle', 'MainWindow')
        theme = meta.get('theme', {})
        pyqt_version = meta.get('pyqtVersion', 6)
        export_theme = meta.get('exportTheme', True)

        # Generate XML
        gen = UIGenerator(elements, canvas_size, window_title, theme, pyqt_version, export_theme)
        xml_content = gen.generate()

        if PYQT_VERSION == 6:
            file_path, _ = QFileDialog.getSaveFileName(
                None, "Save PyQt UI File", "design.ui", "UI Files (*.ui);;All Files (*)"
            )
        else:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(
                None, "Save PyQt UI File", "design.ui", "UI Files (*.ui);;All Files (*)", options=options
            )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(xml_content)
                print(f"Saved UI to: {file_path}")
            except Exception as e:
                print(f"Error saving UI: {e}")

    @pyqtSlot(str)
    def save_python_file(self, data_json):
        data = json.loads(data_json)
        # Parse data
        elements = data.get('elements', [])
        connections = data.get('connections', [])
        meta = data.get('meta', {})
        canvas_size = meta.get('canvasSize', {'w':800, 'h':600})
        window_title = meta.get('windowTitle', 'MainWindow')
        theme = meta.get('theme', {})
        pyqt_version = meta.get('pyqtVersion', 6)
        export_theme = meta.get('exportTheme', True)

        # Generate Python
        gen = PythonGenerator(elements, canvas_size, window_title, theme, connections, pyqt_version, export_theme)
        py_content = gen.generate()

        if PYQT_VERSION == 6:
            file_path, _ = QFileDialog.getSaveFileName(
                None, "Save Python File", "ui_main.py", "Python Files (*.py);;All Files (*)"
            )
        else:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(
                None, "Save Python File", "ui_main.py", "Python Files (*.py);;All Files (*)", options=options
            )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(py_content)
                print(f"Saved Python to: {file_path}")
            except Exception as e:
                print(f"Error saving Python: {e}")

    @pyqtSlot()
    def import_ui_file(self):
        if PYQT_VERSION == 6:
            file_path, _ = QFileDialog.getOpenFileName(
                None, "Open PyQt UI File", "", "UI Files (*.ui);;All Files (*)"
            )
        else:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getOpenFileName(
                None, "Open PyQt UI File", "", "UI Files (*.ui);;All Files (*)", options=options
            )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.ui_imported.emit(content)
            except Exception as e:
                print(f"Error loading: {e}")

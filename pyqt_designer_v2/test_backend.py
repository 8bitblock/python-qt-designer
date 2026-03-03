import sys
import os
import json

# Add path
sys.path.append(os.getcwd())

from pyqt_designer_v2.backend.generator_ui import UIGenerator
from pyqt_designer_v2.backend.generator_py import PythonGenerator

def test_backend_generation():
    # Mock Data
    elements = [
        {
            "id": "btn1", "type": "QPushButton", "name": "pushbutton_1", "x": 100, "y": 100, "w": 100, "h": 30,
            "text": "Button", "bg": "", "color": "", "value": 123 # Invalid property for Button
        },
        {
            "id": "lbl1", "type": "QLabel", "name": "label_1", "x": 100, "y": 150, "w": 100, "h": 30,
            "text": "Label", "bg": "", "color": ""
        },
        {
            "id": "bar1", "type": "QProgressBar", "name": "progress_1", "x": 100, "y": 200, "w": 200, "h": 22,
            "value": 50, "hAlign": "center", "vAlign": "center", "text": "Should not exist" # Invalid property for ProgressBar
        },
        {
            "id": "img1", "type": "QImage", "name": "image_1", "x": 10, "y": 10, "w": 50, "h": 50
        }
    ]

    connections = [
        {
            "senderId": "btn1",
            "signal": "clicked()",
            "receiverId": "lbl1",
            "slot": "clear()"
        }
    ]

    canvas_size = {"w": 800, "h": 600}
    window_title = "Test Window"
    theme_data = {
        "ide": {"text": "#ffffff"},
        "canvas": "#1e1e1e",
        "borderRadius": "6px",
        "fontFamily": '"Segoe UI", sans-serif',
        "widget": {
            "defaultBg": "#404040",
            "btnBg": "#3a3a3a",
            "btnBorder": "1px solid #555",
            "btnColor": "#ffffff",
            "inputBg": "#303030",
            "inputBorder": "1px solid #555",
            "comboBg": "#303030",
            "comboBorder": "1px solid #555",
            "groupBorder": "1px solid #555"
        }
    }

    # Test UI Generation
    print("Testing UI Generation...")
    ui_gen = UIGenerator(elements, canvas_size, window_title, theme_data, connections)
    xml_out = ui_gen.generate()

    # Check for canvas style (Now part of Global QSS)
    # Looking for QMainWindow block in QSS
    assert 'QMainWindow {' in xml_out, "Global QMainWindow stylesheet block missing in XML"
    assert 'background-color: #1e1e1e;' in xml_out, "Global canvas background missing in XML QSS"

    # Check for Modern Styling
    assert 'border-radius: 6px;' in xml_out, "Modern border-radius missing in XML QSS"

    # Check for inline widget styles (Should NOT exist for default widgets anymore)
    assert '<widget class="QPushButton" name="pushbutton_1">' in xml_out, "Button missing in XML"

    # We verify that the button definition does NOT contain an inline styleSheet property
    # This is a bit rough with simple string search, but if we search for the specific old style string it shouldn't be there
    # Old style was: background-color:#3a3a3a...
    # New global style has spaces: background-color: #3a3a3a;
    # Let's check that we don't see a local styleSheet property tag immediately following the button declaration
    # A safer check: ensure the global style is present, which we did above.

    # Check Label autoFillBackground
    assert '<property name="autoFillBackground"><bool>true</bool></property>' in xml_out, "Label autoFillBackground missing in XML"

    # Check Connection
    assert '<sender>pushbutton_1</sender>' in xml_out, "Connection sender missing in XML"
    assert '<receiver>label_1</receiver>' in xml_out, "Connection receiver missing in XML"
    assert '<signal>clicked()</signal>' in xml_out, "Connection signal missing in XML"

    # Check QImage mapping
    assert '<widget class="QLabel" name="image_1">' in xml_out, "QImage should be mapped to QLabel in XML"

    # Check Validation
    assert 'Should not exist' not in xml_out, "Invalid text property generated for ProgressBar in XML"
    assert '<number>123</number>' not in xml_out, "Invalid value property generated for Button in XML"

    print("UI XML Generation Passed")

    # Test Python Generation
    print("Testing Python Generation...")
    py_gen = PythonGenerator(elements, canvas_size, window_title, theme_data, connections)
    py_out = py_gen.generate()

    assert 'MainWindow.setStyleSheet' in py_out, "Global Stylesheet setting missing in Python"

    # Check for Global QSS content in Python
    assert 'QMainWindow {' in py_out, "Global QMainWindow stylesheet block missing in Python"
    assert 'border-radius: 6px;' in py_out, "Modern border-radius missing in Python QSS"

    # Check for widget init
    assert 'self.pushbutton_1 = QPushButton(self.container)' in py_out, "Button init missing in Python"

    # Check absence of inline style for default button
    # The string 'self.pushbutton_1.setStyleSheet' should NOT appear because no user overrides were provided in mock data
    if 'self.pushbutton_1.setStyleSheet' in py_out:
        raise AssertionError("Inline stylesheet found on standard button in Python (should be global)")

    # Check Label autoFillBackground
    assert 'self.label_1.setAutoFillBackground(True)' in py_out, "Label autoFillBackground missing in Python"

    # Check Connection
    assert 'self.pushbutton_1.clicked.connect(self.label_1.clear)' in py_out, "Connection missing in Python"

    # Check QImage mapping
    assert 'self.image_1 = QLabel(self.container)' in py_out, "QImage should be mapped to QLabel in Python"

    # Check Validation
    assert 'Should not exist' not in py_out, "Invalid text property generated for ProgressBar in Python"
    assert '.setValue(123)' not in py_out, "Invalid value property generated for Button in Python"

    print("Python Code Generation Passed")

if __name__ == "__main__":
    test_backend_generation()

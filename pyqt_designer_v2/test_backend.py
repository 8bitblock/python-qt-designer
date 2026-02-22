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
            "text": "Button", "bg": "", "color": ""
        },
        {
            "id": "lbl1", "type": "QLabel", "name": "label_1", "x": 100, "y": 150, "w": 100, "h": 30,
            "text": "Label", "bg": "", "color": ""
        },
        {
            "id": "bar1", "type": "QProgressBar", "name": "progress_1", "x": 100, "y": 200, "w": 200, "h": 22,
            "value": 50, "hAlign": "center", "vAlign": "center"
        }
    ]
    canvas_size = {"w": 800, "h": 600}
    window_title = "Test Window"
    theme_data = {
        "ide": {"text": "#ffffff"},
        "canvas": "#1e1e1e",
        "widget": {
            "defaultBg": "#404040",
            "btnBg": "#3a3a3a",
            "btnBorder": "#555",
            "btnColor": "#ffffff",
            "inputBg": "#303030",
            "inputBorder": "#555",
            "comboBg": "#303030",
            "comboBorder": "#555",
            "groupBorder": "#555"
        }
    }

    # Test UI Generation
    ui_gen = UIGenerator(elements, canvas_size, window_title, theme_data)
    xml_out = ui_gen.generate()

    # Check for canvas style
    assert 'background-color:#1e1e1e;color:#ffffff;' in xml_out, "Global canvas stylesheet missing in XML"

    # Check for inline widget styles
    assert '<widget class="QPushButton" name="pushbutton_1">' in xml_out, "Button missing in XML"
    # Button style (approximate check)
    assert 'background-color:#3a3a3a' in xml_out, "Button inline background missing in XML"

    # Check Label autoFillBackground
    assert '<property name="autoFillBackground"><bool>true</bool></property>' in xml_out, "Label autoFillBackground missing in XML"

    print("UI XML Generation Passed")

    # Test Python Generation
    py_gen = PythonGenerator(elements, canvas_size, window_title, theme_data)
    py_out = py_gen.generate()

    assert 'self.centralwidget.setStyleSheet' in py_out, "Stylesheet setting missing in Python"

    # Check for inline widget styles in Python
    assert 'self.pushbutton_1 = QPushButton(self.centralwidget)' in py_out, "Button init missing in Python"
    assert 'self.pushbutton_1.setStyleSheet("background-color:#3a3a3a' in py_out, "Button inline stylesheet missing in Python"

    # Check Label autoFillBackground
    assert 'self.label_1.setAutoFillBackground(True)' in py_out, "Label autoFillBackground missing in Python"

    print("Python Code Generation Passed")

if __name__ == "__main__":
    test_backend_generation()

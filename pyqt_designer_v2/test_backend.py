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
        }
    ]
    canvas_size = {"w": 800, "h": 600}
    window_title = "Test Window"
    theme_data = {
        "ide": {"text": "#ffffff"},
        "canvas": "#1e1e1e",
        "widget": {
            "defaultBg": "#404040",
            "btnBorder": "#555",
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

    assert 'background-color:#404040' in xml_out, "Global stylesheet defaultBg missing in XML"
    assert 'QWidget{color:#ffffff;}' in xml_out, "Global stylesheet text color missing in XML"
    assert '<widget class="QPushButton" name="pushbutton_1">' in xml_out, "Button missing in XML"

    print("UI XML Generation Passed")

    # Test Python Generation
    py_gen = PythonGenerator(elements, canvas_size, window_title, theme_data)
    py_out = py_gen.generate()

    assert 'self.centralwidget.setStyleSheet' in py_out, "Stylesheet setting missing in Python"
    assert 'background-color:#404040' in py_out, "Global stylesheet defaultBg missing in Python"
    assert 'self.pushbutton_1 = QPushButton(self.centralwidget)' in py_out, "Button init missing in Python"

    print("Python Code Generation Passed")

if __name__ == "__main__":
    test_backend_generation()

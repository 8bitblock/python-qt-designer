import sys
import os

# Add the parent directory to sys.path to allow importing from pyqt_designer_v2
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from pyqt_designer_v2.backend.generator_py import PythonGenerator
from pyqt_designer_v2.backend.generator_ui import UIGenerator

def test_generators():
    elements = [{'id': '1', 'name': 'btn', 'type': 'QPushButton', 'x': 0, 'y': 0, 'w': 100, 'h': 30, 'text': 'Click Me'}]
    canvas_size = {'w': 800, 'h': 600}
    window_title = 'Test Window'
    theme_data = {
        'widget': {'btnBg': '#ff0000'},
        'ide': {'text': '#ffffff'},
        'canvas': '#000000',
        'borderRadius': '8px',
        'fontFamily': 'Arial'
    }

    print("Testing PythonGenerator...")
    py_gen = PythonGenerator(elements, canvas_size, window_title, theme_data)
    py_ss = py_gen.generate_stylesheet()
    assert 'background-color: #ff0000;' in py_ss
    assert 'color: #ffffff;' in py_ss
    assert 'border-radius: 8px;' in py_ss
    assert 'font-family: Arial;' in py_ss
    print("PythonGenerator stylesheet test passed.")

    py_output = py_gen.generate()
    assert 'MainWindow.setStyleSheet' in py_output
    assert 'self.btn = QPushButton(self.container)' in py_output
    print("PythonGenerator generate test passed.")

    print("\nTesting UIGenerator...")
    ui_gen = UIGenerator(elements, canvas_size, window_title, theme_data)
    ui_ss = ui_gen.generate_stylesheet()
    assert 'background-color: #ff0000;' in ui_ss
    assert 'color: #ffffff;' in ui_ss
    print("UIGenerator stylesheet test passed.")

    ui_output = ui_gen.generate()
    assert '<property name="styleSheet">' in ui_output
    assert '<widget class="QPushButton" name="btn">' in ui_output
    print("UIGenerator generate test passed.")

if __name__ == "__main__":
    try:
        test_generators()
        print("\nAll tests passed successfully!")
    except Exception as e:
        print(f"\nTests failed: {e}")
        sys.exit(1)

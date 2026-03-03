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

def test_build_hierarchy_edge_cases():
    elements = [
        # 0: Non-overlapping root element
        {'id': '1', 'name': 'btn1', 'type': 'QPushButton', 'x': 10, 'y': 10, 'w': 50, 'h': 30},

        # 1: Large container (root)
        {'id': '2', 'name': 'groupbox1', 'type': 'QGroupBox', 'x': 100, 'y': 100, 'w': 400, 'h': 400},

        # 2: Single-level nested element (inside groupbox1)
        {'id': '3', 'name': 'btn2', 'type': 'QPushButton', 'x': 110, 'y': 110, 'w': 50, 'h': 30},

        # 3: Mid-size container (inside groupbox1)
        {'id': '4', 'name': 'frame1', 'type': 'QFrame', 'x': 200, 'y': 200, 'w': 200, 'h': 200},

        # 4: Deeply nested element (inside frame1)
        {'id': '5', 'name': 'btn3', 'type': 'QPushButton', 'x': 210, 'y': 210, 'w': 50, 'h': 30},

        # 5: Partial overlap (partially inside groupbox1, should remain root)
        {'id': '6', 'name': 'btn4', 'type': 'QPushButton', 'x': 90, 'y': 90, 'w': 50, 'h': 30},

        # 6: Non-container widget acting as fake parent
        {'id': '7', 'name': 'label1', 'type': 'QLabel', 'x': 600, 'y': 600, 'w': 100, 'h': 100},

        # 7: Element completely inside non-container widget (should remain root)
        {'id': '8', 'name': 'btn5', 'type': 'QPushButton', 'x': 610, 'y': 610, 'w': 50, 'h': 30}
    ]
    canvas_size = {'w': 800, 'h': 800}
    window_title = 'Hierarchy Test'
    theme_data = {}

    ui_gen = UIGenerator(elements, canvas_size, window_title, theme_data)
    roots = ui_gen.build_hierarchy()

    # We should have exactly 4 roots: btn1, groupbox1, btn4 (partial overlap), label1, btn5 (inside label1)
    # Wait, actually btn1, groupbox1, btn4, label1, btn5
    assert len(roots) == 5, f"Expected 5 roots, but got {len(roots)}"

    root_ids = [r['id'] for r in roots]
    assert '1' in root_ids # btn1
    assert '2' in root_ids # groupbox1
    assert '6' in root_ids # btn4 (partial overlap)
    assert '7' in root_ids # label1
    assert '8' in root_ids # btn5 (inside label1, non-container)

    # Check groupbox1 children
    groupbox1 = next(r for r in roots if r['id'] == '2')
    # Should have btn2 and frame1
    assert len(groupbox1['children']) == 2
    gb_child_ids = [c['id'] for c in groupbox1['children']]
    assert '3' in gb_child_ids # btn2
    assert '4' in gb_child_ids # frame1

    # Check frame1 children (deep nesting)
    frame1 = next(c for c in groupbox1['children'] if c['id'] == '4')
    # Should have btn3
    assert len(frame1['children']) == 1
    assert frame1['children'][0]['id'] == '5' # btn3

    print("test_build_hierarchy_edge_cases passed successfully!")

if __name__ == "__main__":
    try:
        test_generators()
        print("\nAll tests passed successfully!")
    except Exception as e:
        print(f"\nTests failed: {e}")
        sys.exit(1)

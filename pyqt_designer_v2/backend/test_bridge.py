import json
import pytest
from unittest.mock import patch, mock_open, MagicMock

from pyqt_designer_v2.backend.bridge import DesignerBridge

# ====================
# Tests for save_ui_file
# ====================

def test_save_ui_file_success():
    data = {
        'elements': [],
        'connections': [],
        'meta': {}
    }
    data_json = json.dumps(data)

    bridge_instance = DesignerBridge()

    with patch('pyqt_designer_v2.backend.bridge.QFileDialog.getSaveFileName') as mock_get_save_file_name, \
         patch('builtins.open', mock_open()) as mocked_file, \
         patch('builtins.print') as mock_print:

        mock_get_save_file_name.return_value = ('/fake/path/design.ui', 'UI Files (*.ui)')

        bridge_instance.save_ui_file(data_json)

        mock_get_save_file_name.assert_called_once()
        mocked_file.assert_called_once_with('/fake/path/design.ui', 'w', encoding='utf-8')
        mocked_file().write.assert_called_once()
        mock_print.assert_called_once_with("Saved UI to: /fake/path/design.ui")

def test_save_ui_file_cancel():
    data = {}
    data_json = json.dumps(data)

    bridge_instance = DesignerBridge()

    with patch('pyqt_designer_v2.backend.bridge.QFileDialog.getSaveFileName') as mock_get_save_file_name, \
         patch('builtins.open', mock_open()) as mocked_file, \
         patch('builtins.print') as mock_print:

        mock_get_save_file_name.return_value = ('', '')

        bridge_instance.save_ui_file(data_json)

        mock_get_save_file_name.assert_called_once()
        mocked_file.assert_not_called()
        mock_print.assert_not_called()

def test_save_ui_file_exception():
    data = {}
    data_json = json.dumps(data)

    bridge_instance = DesignerBridge()

    with patch('pyqt_designer_v2.backend.bridge.QFileDialog.getSaveFileName') as mock_get_save_file_name, \
         patch('builtins.open', mock_open()) as mocked_file, \
         patch('builtins.print') as mock_print:

        mock_get_save_file_name.return_value = ('/fake/path/design.ui', 'UI Files (*.ui)')
        mocked_file.side_effect = PermissionError("Permission denied")

        bridge_instance.save_ui_file(data_json)

        mock_get_save_file_name.assert_called_once()
        mocked_file.assert_called_once_with('/fake/path/design.ui', 'w', encoding='utf-8')
        mock_print.assert_called_once_with("Error saving UI: Permission denied")


# ====================
# Tests for save_python_file
# ====================

def test_save_python_file_success():
    data = {
        'elements': [],
        'connections': [],
        'meta': {}
    }
    data_json = json.dumps(data)

    bridge_instance = DesignerBridge()

    with patch('pyqt_designer_v2.backend.bridge.QFileDialog.getSaveFileName') as mock_get_save_file_name, \
         patch('builtins.open', mock_open()) as mocked_file, \
         patch('builtins.print') as mock_print:

        mock_get_save_file_name.return_value = ('/fake/path/ui_main.py', 'Python Files (*.py)')

        bridge_instance.save_python_file(data_json)

        mock_get_save_file_name.assert_called_once()
        mocked_file.assert_called_once_with('/fake/path/ui_main.py', 'w', encoding='utf-8')
        mocked_file().write.assert_called_once()
        mock_print.assert_called_once_with("Saved Python to: /fake/path/ui_main.py")

def test_save_python_file_cancel():
    data = {}
    data_json = json.dumps(data)

    bridge_instance = DesignerBridge()

    with patch('pyqt_designer_v2.backend.bridge.QFileDialog.getSaveFileName') as mock_get_save_file_name, \
         patch('builtins.open', mock_open()) as mocked_file, \
         patch('builtins.print') as mock_print:

        mock_get_save_file_name.return_value = ('', '')

        bridge_instance.save_python_file(data_json)

        mock_get_save_file_name.assert_called_once()
        mocked_file.assert_not_called()
        mock_print.assert_not_called()

def test_save_python_file_exception():
    data = {}
    data_json = json.dumps(data)

    bridge_instance = DesignerBridge()

    with patch('pyqt_designer_v2.backend.bridge.QFileDialog.getSaveFileName') as mock_get_save_file_name, \
         patch('builtins.open', mock_open()) as mocked_file, \
         patch('builtins.print') as mock_print:

        mock_get_save_file_name.return_value = ('/fake/path/ui_main.py', 'Python Files (*.py)')
        mocked_file.side_effect = PermissionError("Permission denied")

        bridge_instance.save_python_file(data_json)

        mock_get_save_file_name.assert_called_once()
        mocked_file.assert_called_once_with('/fake/path/ui_main.py', 'w', encoding='utf-8')
        mock_print.assert_called_once_with("Error saving Python: Permission denied")

# ====================
# Tests for import_ui_file
# ====================

def test_import_ui_file_success():
    bridge_instance = DesignerBridge()
    # We need to mock ui_imported.emit
    bridge_instance.ui_imported = MagicMock()

    fake_parsed_data = {"elements": [{"id": "1", "type": "QPushButton"}]}

    with patch('pyqt_designer_v2.backend.bridge.QFileDialog.getOpenFileName') as mock_get_open_file_name, \
         patch('builtins.open', mock_open(read_data='<ui><widget class="QPushButton" name="btn"/></ui>')) as mocked_file, \
         patch('pyqt_designer_v2.backend.bridge.UIParser.parse', return_value=fake_parsed_data) as mock_parse, \
         patch('builtins.print') as mock_print:

        mock_get_open_file_name.return_value = ('/fake/path/import.ui', 'UI Files (*.ui)')

        bridge_instance.import_ui_file()

        mock_get_open_file_name.assert_called_once()
        mocked_file.assert_called_once_with('/fake/path/import.ui', 'r', encoding='utf-8')
        mock_parse.assert_called_once_with('<ui><widget class="QPushButton" name="btn"/></ui>')

        # Verify the emit was called with the json serialized data
        bridge_instance.ui_imported.emit.assert_called_once()
        emitted_val = bridge_instance.ui_imported.emit.call_args[0][0]
        assert json.loads(emitted_val) == fake_parsed_data

def test_import_ui_file_cancel():
    bridge_instance = DesignerBridge()
    bridge_instance.ui_imported = MagicMock()

    with patch('pyqt_designer_v2.backend.bridge.QFileDialog.getOpenFileName') as mock_get_open_file_name, \
         patch('builtins.open', mock_open()) as mocked_file, \
         patch('builtins.print') as mock_print:

        mock_get_open_file_name.return_value = ('', '')

        bridge_instance.import_ui_file()

        mock_get_open_file_name.assert_called_once()
        mocked_file.assert_not_called()
        bridge_instance.ui_imported.emit.assert_not_called()

def test_import_ui_file_parse_fail():
    bridge_instance = DesignerBridge()
    bridge_instance.ui_imported = MagicMock()

    with patch('pyqt_designer_v2.backend.bridge.QFileDialog.getOpenFileName') as mock_get_open_file_name, \
         patch('builtins.open', mock_open(read_data='invalid xml')) as mocked_file, \
         patch('pyqt_designer_v2.backend.bridge.UIParser.parse', return_value=None) as mock_parse, \
         patch('builtins.print') as mock_print:

        mock_get_open_file_name.return_value = ('/fake/path/import.ui', 'UI Files (*.ui)')

        bridge_instance.import_ui_file()

        mock_get_open_file_name.assert_called_once()
        mocked_file.assert_called_once_with('/fake/path/import.ui', 'r', encoding='utf-8')
        mock_parse.assert_called_once_with('invalid xml')
        bridge_instance.ui_imported.emit.assert_not_called()
        mock_print.assert_called_once_with("Failed to parse UI file")

def test_import_ui_file_exception():
    bridge_instance = DesignerBridge()
    bridge_instance.ui_imported = MagicMock()

    with patch('pyqt_designer_v2.backend.bridge.QFileDialog.getOpenFileName') as mock_get_open_file_name, \
         patch('builtins.open', mock_open()) as mocked_file, \
         patch('builtins.print') as mock_print:

        mock_get_open_file_name.return_value = ('/fake/path/import.ui', 'UI Files (*.ui)')
        mocked_file.side_effect = FileNotFoundError("File not found")

        bridge_instance.import_ui_file()

        mock_get_open_file_name.assert_called_once()
        mocked_file.assert_called_once_with('/fake/path/import.ui', 'r', encoding='utf-8')
        bridge_instance.ui_imported.emit.assert_not_called()
        mock_print.assert_called_once_with("Error loading: File not found")

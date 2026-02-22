# PyQt Designer Pro V2

This is a rewritten version of the PyQt Designer application, now featuring a modular architecture with separate frontend and backend components.

## Features

- **High Contrast UI**: Widgets are now clearly visible against the dark background, thanks to global stylesheet generation.
- **Drag and Drop**: Create UIs easily by dragging widgets onto the canvas.
- **Code Generation**: Generates both `.ui` XML files and Python code.
- **Modular Structure**: Easier to maintain and extend.

## Requirements

- Python 3.6+
- Internet connection (required for loading React and Tailwind from CDNs).
- `PyQt5` and `PyQtWebEngine` are required.

## Installation

1.  Install dependencies:
    ```bash
    pip install PyQt5 PyQtWebEngine
    ```

## How to Run

1.  Run the application from the root directory:
    ```bash
    python pyqt_designer_v2/main.py
    ```

## Development

- **Backend**: Located in `pyqt_designer_v2/backend/`. Handles code generation and file I/O.
- **Frontend**: Located in `pyqt_designer_v2/frontend/`. React-based UI designer.
- **Tests**: Run `python pyqt_designer_v2/test_backend.py` to test the code generators.

## Limitations

- **Import Functionality**: Currently not fully implemented in this version. Use drag-and-drop to create new designs.
- **Offline Use**: Requires an internet connection to load frontend libraries.

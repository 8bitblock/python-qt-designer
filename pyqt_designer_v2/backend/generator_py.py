import json

class PythonGenerator:
    def __init__(self, elements, canvas_size, window_title, theme_data, connections=None, pyqt_version=6, include_theme=True):
        self.elements = elements
        self.canvas_size = canvas_size
        self.window_title = window_title
        self.theme = theme_data
        self.connections = connections or []
        self.pyqt_version = pyqt_version
        self.include_theme = include_theme
        self.id_map = {e['id']: e['name'] for e in elements}

    def generate_stylesheet(self):
        """Generates a global QSS stylesheet based on the theme."""
        if not self.include_theme or not self.theme:
            return ""

        tw = self.theme.get('widget', {})
        ide = self.theme.get('ide', {})
        canvas_bg = self.theme.get('canvas', '#f0f0f0')
        text_color = ide.get('text', '#000000')

        radius = self.theme.get('borderRadius', '4px')
        font_family = self.theme.get('fontFamily', '"Segoe UI", sans-serif')

        # Base Styles
        qss = f"""
        QMainWindow {{
            background-color: {canvas_bg};
            color: {text_color};
        }}
        QWidget {{
            font-family: {font_family};
            font-size: 10pt;
        }}
        """

        # Common Disabled Styles (Theme Aware)
        disabled_bg = ide.get('bg3', tw.get('btnBgDisabled', canvas_bg)) # A darker/dimmer surface color
        disabled_border = ide.get('border', '1px solid #d0d0d0') # The subtle border for inputs/frames in the theme
        if not disabled_border.startswith('1px'): disabled_border = f'1px solid {disabled_border}'
        disabled_color = ide.get('text3', '#888888') # The dim/placeholder text color

        # Buttons
        btn_bg = tw.get('btnBg', '#e0e0e0')
        btn_border = tw.get('btnBorder', '1px solid #999')
        btn_color = tw.get('btnColor', '#000')
        btn_hover = tw.get('btnHoverBg', '#eeeeee')
        btn_pressed = tw.get('btnPressedBg', '#cccccc')

        qss += f"""
        QPushButton, QToolButton {{
            background-color: {btn_bg};
            border: {btn_border};
            color: {btn_color};
            border-radius: {radius};
            padding: 6px 12px;
        }}
        QPushButton:hover, QToolButton:hover {{
            background-color: {btn_hover};
        }}
        QPushButton:pressed, QToolButton:pressed {{
            background-color: {btn_pressed};
        }}
        QPushButton:disabled, QToolButton:disabled {{
            background-color: {disabled_bg};
            border: {disabled_border};
            color: {disabled_color};
        }}
        """

        # Flat Buttons (Using the native :flat pseudo-state for dynamic updates)
        qss += f"""
        QPushButton:flat {{
            background-color: transparent;
            border: none;
        }}
        QPushButton:flat:hover {{
            background-color: rgba(128, 128, 128, 0.1);
        }}
        QPushButton:flat:pressed {{
            background-color: rgba(128, 128, 128, 0.2);
        }}
        QPushButton:flat:disabled {{
            background-color: transparent;
            color: {disabled_color};
        }}
        """

        # Command Link Button (Card Style)
        cmd_btn_bg = tw.get('cmdBtnBg', btn_bg)
        cmd_btn_hover = tw.get('cmdBtnHoverBg', btn_hover)

        qss += f"""
        QCommandLinkButton {{
            background-color: {cmd_btn_bg};
            border: {btn_border};
            color: {btn_color};
            border-radius: {radius};
            padding: 8px;
            text-align: left;
        }}
        QCommandLinkButton:hover {{
            background-color: {cmd_btn_hover};
        }}
        QCommandLinkButton:disabled {{
            background-color: {disabled_bg};
            border: {disabled_border};
            color: {disabled_color};
        }}
        """

        # Inputs
        input_bg = tw.get('inputBg', '#fff')
        input_border = tw.get('inputBorder', '1px solid #ccc')
        input_color = tw.get('inputColor', '#000')
        input_focus = tw.get('inputFocusBorder', '1px solid blue')

        qss += f"""
        QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QTimeEdit, QDateTimeEdit {{
            background-color: {input_bg};
            border: {input_border};
            color: {input_color};
            border-radius: {radius};
            padding: 4px;
        }}
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus {{
            border: {input_focus};
        }}
        QLineEdit:disabled, QTextEdit:disabled, QPlainTextEdit:disabled, QSpinBox:disabled, QDoubleSpinBox:disabled, QDateEdit:disabled, QTimeEdit:disabled, QDateTimeEdit:disabled {{
            background-color: {disabled_bg};
            color: {disabled_color};
            border: {disabled_border};
        }}
        """

        # ComboBox
        combo_bg = tw.get('comboBg', '#fff')
        combo_border = tw.get('comboBorder', '1px solid #ccc')
        combo_color = tw.get('comboColor', '#000')

        qss += f"""
        QComboBox, QFontComboBox {{
            background-color: {combo_bg};
            border: {combo_border};
            color: {combo_color};
            border-radius: {radius};
            padding: 4px;
        }}
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left-width: 0px;
            border-top-right-radius: {radius};
            border-bottom-right-radius: {radius};
        }}
        QComboBox:disabled {{
            background-color: {disabled_bg};
            color: {disabled_color};
            border: {disabled_border};
        }}
        """

        # Labels & Checks
        label_bg = tw.get('labelBg', 'transparent')
        label_color = tw.get('labelColor', text_color)
        check_color = tw.get('checkColor', text_color)

        qss += f"""
        QLabel {{
            background-color: {label_bg};
            color: {label_color};
            border-radius: {radius};
            padding: 2px;
        }}
        QCheckBox, QRadioButton {{
            color: {check_color};
            spacing: 5px;
        }}
        QCheckBox::indicator, QRadioButton::indicator {{
            width: 16px;
            height: 16px;
        }}
        """

        # GroupBox
        group_border = tw.get('groupBorder', '1px solid #ccc')
        group_color = tw.get('groupColor', text_color)

        qss += f"""
        QGroupBox {{
            border: {group_border};
            border-radius: {radius};
            margin-top: 1.5em;
            color: {group_color};
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 5px;
            left: 10px;
        }}
        """

        # Lists/Trees/Tables
        list_bg = tw.get('listBg', '#fff')
        list_color = tw.get('listColor', '#000')
        list_border = tw.get('listBorder', '1px solid #ccc')
        list_sel_bg = tw.get('listSelBg', 'blue')
        list_sel_color = tw.get('listSelColor', '#fff')
        table_header_bg = tw.get('tableHeaderBg', '#eee')

        qss += f"""
        QListWidget, QTreeWidget, QTableWidget {{
            background-color: {list_bg};
            color: {list_color};
            border: {list_border};
            border-radius: {radius};
            outline: 0;
        }}
        QListWidget::item:selected, QTreeWidget::item:selected, QTableWidget::item:selected {{
            background-color: {list_sel_bg};
            color: {list_sel_color};
        }}
        QHeaderView::section {{
            background-color: {table_header_bg};
            color: {list_color};
            padding: 4px;
            border: 0px;
            border-bottom: 1px solid #ccc;
        }}
        """

        # Tabs
        tab_border = tw.get('tabBorder', '1px solid #ccc')
        tab_active_bg = tw.get('tabActiveBg', '#fff')
        tab_bar_bg = tw.get('tabBarBg', '#eee')
        tab_color = tw.get('tabColor', '#000')

        qss += f"""
        QTabWidget::pane {{
            border: {tab_border};
            border-radius: {radius};
            background-color: {tab_active_bg};
        }}
        QTabBar::tab {{
            background-color: {tab_bar_bg};
            color: {tab_color};
            padding: 6px 12px;
            border-top-left-radius: {radius};
            border-top-right-radius: {radius};
            margin-right: 2px;
        }}
        QTabBar::tab:selected {{
            background-color: {tab_active_bg};
            border-bottom-color: {tab_active_bg};
        }}
        """

        # Scrollbars (Modern Touch)
        sb_bg = tw.get('scrollBg', '#f0f0f0')
        sb_handle = tw.get('scrollHandle', '#ccc')
        sb_hover = tw.get('scrollHandleHover', '#bbb')

        qss += f"""
        QScrollBar:vertical {{
            border: none;
            background: {sb_bg};
            width: 10px;
            margin: 0px;
            border-radius: 5px;
        }}
        QScrollBar::handle:vertical {{
            background: {sb_handle};
            min-height: 20px;
            border-radius: 5px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {sb_hover};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        QScrollBar:horizontal {{
            border: none;
            background: {sb_bg};
            height: 10px;
            margin: 0px;
            border-radius: 5px;
        }}
        QScrollBar::handle:horizontal {{
            background: {sb_handle};
            min-width: 20px;
            border-radius: 5px;
        }}
        QScrollBar::handle:horizontal:hover {{
            background: {sb_hover};
        }}
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
        """

        return qss

    def get_user_style_overrides(self, el):
        """Returns ONLY the user-defined style overrides."""
        user_style = el.get('styleSheet', '')

        # Additional User Props overrides
        if el.get('bg'): user_style += f"background-color:{el['bg']};"
        if el.get('color'): user_style += f"color:{el['color']};"
        if el.get('fontSize'): user_style += f"font-size:{el['fontSize']}pt;"
        if el.get('fontFamily'): user_style += f"font-family:'{el['fontFamily']}';"
        if el.get('fontWeight') == 'bold': user_style += "font-weight:bold;"
        if el.get('fontItalic'): user_style += "font-style:italic;"

        return user_style

    def generate(self):
        lines = []
        lines.append("# Auto-generated by PyQt Designer Pro")

        if self.pyqt_version == 5:
            lines.append("from PyQt5.QtWidgets import *")
            lines.append("from PyQt5.QtCore import *")
            lines.append("from PyQt5.QtGui import *\n")
        else:
            lines.append("from PyQt6.QtWidgets import *")
            lines.append("from PyQt6.QtCore import *")
            lines.append("from PyQt6.QtGui import *\n")

        # AutoScaler Class
        lines.append("class AutoScaler(QGraphicsView):")
        lines.append("    def __init__(self, scene, parent=None):")
        lines.append("        super().__init__(scene, parent)")
        if self.pyqt_version == 5:
            lines.append("        self.setFrameShape(QFrame.NoFrame)")
        else:
            lines.append("        self.setFrameShape(QFrame.Shape.NoFrame)")
        lines.append("        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff if hasattr(Qt, 'ScrollBarPolicy') else Qt.ScrollBarAlwaysOff)")
        lines.append("        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff if hasattr(Qt, 'ScrollBarPolicy') else Qt.ScrollBarAlwaysOff)")
        lines.append("        self.setStyleSheet('background: transparent;')")

        lines.append("    def resizeEvent(self, event):")
        lines.append("        super().resizeEvent(event)")
        if self.pyqt_version == 5:
            lines.append("        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)")
        else:
            lines.append("        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)")
        lines.append("")

        lines.append("class Ui_MainWindow:")
        lines.append("    def setupUi(self, MainWindow):")
        lines.append('        MainWindow.setObjectName("MainWindow")')
        lines.append(f"        MainWindow.resize({int(self.canvas_size['w'])}, {int(self.canvas_size['h'])})")
        lines.append(f'        MainWindow.setWindowTitle("{self.window_title}")')

        # Inject Global Stylesheet
        if self.include_theme:
            global_style = self.generate_stylesheet()
            # Escape newlines for python string
            global_style_py = global_style.replace('\n', '')
            lines.append(f'        MainWindow.setStyleSheet("""{global_style}""")')

        # Setup Scene and Container
        lines.append(f"        self.scene = QGraphicsScene(0, 0, {int(self.canvas_size['w'])}, {int(self.canvas_size['h'])})")
        lines.append("        self.container = QWidget()")
        lines.append(f"        self.container.setGeometry(0, 0, {int(self.canvas_size['w'])}, {int(self.canvas_size['h'])})")
        lines.append('        self.container.setObjectName("container")')

        HAS_TEXT = {'QPushButton','QToolButton','QLabel','QLineEdit','QTextEdit','QPlainTextEdit','QCheckBox','QRadioButton','QImage','QCommandLinkButton'}
        HAS_TITLE = {'QGroupBox'}
        HAS_WINDOWTITLE = {'QDockWidget'}
        HAS_ALIGN = {'QLabel','QLineEdit','QImage','QProgressBar'}
        HAS_PLACEHOLDER = {'QLineEdit','QTextEdit','QPlainTextEdit'}
        HAS_READONLY = {'QLineEdit','QTextEdit','QPlainTextEdit','QSpinBox','QDoubleSpinBox','QDateEdit','QTimeEdit','QDateTimeEdit'}
        HAS_FLAT = {'QPushButton','QGroupBox'}
        HAS_CHECKABLE = {'QPushButton','QToolButton','QGroupBox','QCheckBox','QRadioButton'}
        HAS_CHECKED = {'QPushButton','QToolButton','QCheckBox','QRadioButton','QGroupBox'}
        HAS_AUTOFILL = {'QLabel', 'QCheckBox', 'QRadioButton'}

        for el in self.elements:
            cls = el['type']
            py_class = cls
            if cls in ['VLine', 'HLine']:
                py_class = 'QFrame'
            elif cls == 'QImage':
                py_class = 'QLabel'

            # Parent is self.container instead of self.centralwidget
            lines.append(f"        self.{el['name']} = {py_class}(self.container)")
            lines.append(f'        self.{el["name"]}.setObjectName("{el["name"]}")')
            lines.append(f"        self.{el['name']}.setGeometry(QRect({int(el['x'])}, {int(el['y'])}, {int(el['w'])}, {int(el['h'])}))")

            # Inline Stylesheet Logic (User Overrides Only)
            user_style = self.get_user_style_overrides(el)
            if user_style:
                lines.append(f'        self.{el["name"]}.setStyleSheet("{user_style}")')

            # AutoFillBackground (Optional but good backup for Labels)
            if cls in HAS_AUTOFILL and self.include_theme and self.theme.get('widget', {}).get('defaultBg'):
                lines.append(f'        self.{el["name"]}.setAutoFillBackground(True)')

            # Text
            text = el.get('text', '').replace('"', '\\"').replace('\n', '\\n')
            if text:
                if cls in HAS_TEXT:
                    lines.append(f'        self.{el["name"]}.setText("{text}")')
                if cls in HAS_TITLE:
                    lines.append(f'        self.{el["name"]}.setTitle("{text}")')
                if cls in HAS_WINDOWTITLE:
                    lines.append(f'        self.{el["name"]}.setWindowTitle("{text}")')

            if el.get('description') and cls == 'QCommandLinkButton':
                lines.append(f'        self.{el["name"]}.setDescription("{el["description"].replace("\"", "\\\"").replace(chr(10), "\\n")}")')

            # Common
            if el.get('tooltip'): lines.append(f'        self.{el["name"]}.setToolTip("{el["tooltip"].replace("\"", "\\\"").replace(chr(10), "\\n")}")')
            if el.get('statusTip'): lines.append(f'        self.{el["name"]}.setStatusTip("{el["statusTip"].replace("\"", "\\\"").replace(chr(10), "\\n")}")')
            if 'enabled' in el and not el['enabled']: lines.append(f'        self.{el["name"]}.setEnabled(False)')
            if 'visible' in el and not el['visible']: lines.append(f'        self.{el["name"]}.setVisible(False)')

            if el.get('placeholderText') and cls in HAS_PLACEHOLDER:
                lines.append(f'        self.{el["name"]}.setPlaceholderText("{el["placeholderText"].replace("\"", "\\\"")}")')
            if el.get('readOnly') and cls in HAS_READONLY: lines.append(f'        self.{el["name"]}.setReadOnly(True)')
            if el.get('flat') and cls in HAS_FLAT: lines.append(f'        self.{el["name"]}.setFlat(True)')
            if el.get('checkable') and cls in HAS_CHECKABLE: lines.append(f'        self.{el["name"]}.setCheckable(True)')
            if el.get('checked') and cls in HAS_CHECKED: lines.append(f'        self.{el["name"]}.setChecked(True)')

            if cls == 'QComboBox' and el.get('items'):
                safe_items = [str(x) for x in el['items']]
                lines.append(f'        self.{el["name"]}.addItems({json.dumps(safe_items)})')

            if cls == 'VLine':
                if self.pyqt_version == 5:
                    lines.append(f'        self.{el["name"]}.setFrameShape(QFrame.VLine)')
                    lines.append(f'        self.{el["name"]}.setFrameShadow(QFrame.Sunken)')
                else:
                    lines.append(f'        self.{el["name"]}.setFrameShape(QFrame.Shape.VLine)')
                    lines.append(f'        self.{el["name"]}.setFrameShadow(QFrame.Shadow.Sunken)')

            if cls == 'HLine':
                if self.pyqt_version == 5:
                    lines.append(f'        self.{el["name"]}.setFrameShape(QFrame.HLine)')
                    lines.append(f'        self.{el["name"]}.setFrameShadow(QFrame.Sunken)')
                else:
                    lines.append(f'        self.{el["name"]}.setFrameShape(QFrame.Shape.HLine)')
                    lines.append(f'        self.{el["name"]}.setFrameShadow(QFrame.Shadow.Sunken)')

            if 'value' in el and cls in {'QProgressBar', 'QSlider', 'QSpinBox', 'QDoubleSpinBox'}:
                lines.append(f'        self.{el["name"]}.setValue({el["value"]})')
            if 'value' in el and cls == 'QLCDNumber':
                lines.append(f'        self.{el["name"]}.display({el["value"]})')
            if 'minimum' in el and cls in {'QProgressBar', 'QSlider', 'QSpinBox', 'QDoubleSpinBox'}:
                lines.append(f'        self.{el["name"]}.setMinimum({el["minimum"]})')
            if 'maximum' in el and cls in {'QProgressBar', 'QSlider', 'QSpinBox', 'QDoubleSpinBox'}:
                lines.append(f'        self.{el["name"]}.setMaximum({el["maximum"]})')

            if cls == 'QTabWidget' and el.get('tabs'):
                for i, t in enumerate(el['tabs']):
                    lines.append(f'        self.tab_{el["name"]}_{i} = QWidget()')
                    lines.append(f'        self.{el["name"]}.addTab(self.tab_{el["name"]}_{i}, "{t.replace("\"", "\\\"")}")')

            if cls in HAS_ALIGN:
                h, v = el.get('hAlign'), el.get('vAlign')
                parts = []
                if self.pyqt_version == 5:
                    if h == 'left': parts.append('Qt.AlignLeft')
                    elif h == 'right': parts.append('Qt.AlignRight')
                    elif h == 'justify': parts.append('Qt.AlignJustify')
                    elif h == 'center': parts.append('Qt.AlignHCenter')
                    if v == 'top': parts.append('Qt.AlignTop')
                    elif v == 'bottom': parts.append('Qt.AlignBottom')
                    elif v == 'center': parts.append('Qt.AlignVCenter')
                else:
                    if h == 'left': parts.append('Qt.AlignmentFlag.AlignLeft')
                    elif h == 'right': parts.append('Qt.AlignmentFlag.AlignRight')
                    elif h == 'justify': parts.append('Qt.AlignmentFlag.AlignJustify')
                    elif h == 'center': parts.append('Qt.AlignmentFlag.AlignHCenter')
                    if v == 'top': parts.append('Qt.AlignmentFlag.AlignTop')
                    elif v == 'bottom': parts.append('Qt.AlignmentFlag.AlignBottom')
                    elif v == 'center': parts.append('Qt.AlignmentFlag.AlignVCenter')
                if parts:
                    lines.append(f'        self.{el["name"]}.setAlignment({" | ".join(parts)})')

            lines.append("")

        # Add container to scene, set view as central
        lines.append("        self.scene.addWidget(self.container)")
        lines.append("        self.view = AutoScaler(self.scene)")
        lines.append('        self.view.setObjectName("view")')
        lines.append("        MainWindow.setCentralWidget(self.view)")

        lines.append("        self.statusbar = QStatusBar(MainWindow)")
        lines.append("        MainWindow.setStatusBar(self.statusbar)")

        if self.connections:
            lines.append("")
            for c in self.connections:
                sig = c['signal'].split('(')[0]
                slt = c['slot'].split('(')[0]
                sender = self.id_map.get(c['senderId'])
                receiver = 'MainWindow' if c['receiverId'] == 'MainWindow' else self.id_map.get(c['receiverId'])

                if sender and receiver:
                    if receiver == 'MainWindow':
                        lines.append(f"        self.{sender}.{sig}.connect(MainWindow.{slt})")
                    else:
                        lines.append(f"        self.{sender}.{sig}.connect(self.{receiver}.{slt})")

        lines.append("\nif __name__ == \"__main__\":")
        lines.append("    import sys")
        lines.append("    app = QApplication(sys.argv)")
        lines.append("    window = QMainWindow()")
        lines.append("    ui = Ui_MainWindow()")
        lines.append("    ui.setupUi(window)")
        lines.append("    window.show()")
        if self.pyqt_version == 5:
            lines.append("    sys.exit(app.exec_())")
        else:
            lines.append("    sys.exit(app.exec())")

        return "\n".join(lines)

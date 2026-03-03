class BaseGenerator:
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

        # Buttons
        btn_bg = tw.get('btnBg', '#e0e0e0')
        btn_border = tw.get('btnBorder', '1px solid #999')
        btn_color = tw.get('btnColor', '#000')
        btn_hover = tw.get('btnHoverBg', '#eeeeee')
        btn_pressed = tw.get('btnPressedBg', '#cccccc')
        btn_disabled = tw.get('btnBgDisabled', canvas_bg)

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
            background-color: {btn_disabled};
            border: 1px solid #d0d0d0;
            color: #888888;
        }}
        """

        # Flat Buttons
        qss += f"""
        QPushButton[flat="true"] {{
            background-color: transparent;
            border: none;
        }}
        QPushButton[flat="true"]:hover {{
            background-color: rgba(0, 0, 0, 0.05);
        }}
        QPushButton[flat="true"]:pressed {{
            background-color: rgba(0, 0, 0, 0.1);
        }}
        QPushButton[flat="true"]:disabled {{
            background-color: transparent;
            color: #888888;
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
            background-color: {btn_disabled};
            border: 1px solid #d0d0d0;
            color: #888888;
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
            background-color: #f5f5f5;
            color: #888888;
            border: 1px solid #d0d0d0;
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
            background-color: #f5f5f5;
            color: #888888;
            border: 1px solid #d0d0d0;
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

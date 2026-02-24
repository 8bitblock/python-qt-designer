import json

def esc_xml(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

class UIGenerator:
    def __init__(self, elements, canvas_size, window_title, theme_data, connections=None, pyqt_version=6, include_theme=True):
        self.elements = elements
        self.canvas_size = canvas_size
        self.window_title = window_title
        self.theme = theme_data
        self.connections = connections or []
        self.pyqt_version = pyqt_version
        self.include_theme = include_theme
        self.id_map = {e['id']: e['name'] for e in elements}

    def _gen_connections(self):
        if not self.connections:
            return ""

        xml = ' <connections>\n'
        for c in self.connections:
            sender = self.id_map.get(c['senderId'])
            receiver = 'MainWindow' if c['receiverId'] == 'MainWindow' else self.id_map.get(c['receiverId'])

            if sender and receiver:
                xml += '  <connection>\n'
                xml += f'   <sender>{sender}</sender>\n'
                xml += f'   <signal>{c["signal"]}</signal>\n'
                xml += f'   <receiver>{receiver}</receiver>\n'
                xml += f'   <slot>{c["slot"]}</slot>\n'
                xml += '  </connection>\n'

        xml += ' </connections>\n'
        return xml

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
        qss += f"""
        QPushButton, QToolButton {{
            background-color: {tw.get('btnBg', '#e0e0e0')};
            border: {tw.get('btnBorder', '1px solid #999')};
            color: {tw.get('btnColor', '#000')};
            border-radius: {radius};
            padding: 6px 12px;
        }}
        QPushButton:hover, QToolButton:hover {{
            background-color: {tw.get('btnHoverBg', '#eeeeee')};
        }}
        QPushButton:pressed, QToolButton:pressed {{
            background-color: {tw.get('btnPressedBg', '#cccccc')};
        }}
        """

        # Command Link Button (Card Style)
        qss += f"""
        QCommandLinkButton {{
            background-color: {tw.get('cmdBtnBg', tw.get('btnBg'))};
            border: {tw.get('btnBorder', '1px solid #999')};
            color: {tw.get('btnColor', '#000')};
            border-radius: {radius};
            padding: 8px;
            text-align: left;
        }}
        QCommandLinkButton:hover {{
            background-color: {tw.get('cmdBtnHoverBg', tw.get('btnHoverBg'))};
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
        """

        # ComboBox
        qss += f"""
        QComboBox, QFontComboBox {{
            background-color: {tw.get('comboBg', '#fff')};
            border: {tw.get('comboBorder', '1px solid #ccc')};
            color: {tw.get('comboColor', '#000')};
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
        """

        # Labels & Checks
        qss += f"""
        QLabel {{
            background-color: {tw.get('labelBg', 'transparent')};
            color: {tw.get('labelColor', text_color)};
            border-radius: {radius};
            padding: 2px;
        }}
        QCheckBox, QRadioButton {{
            color: {tw.get('checkColor', text_color)};
            spacing: 5px;
        }}
        QCheckBox::indicator, QRadioButton::indicator {{
            width: 16px;
            height: 16px;
        }}
        """

        # GroupBox
        qss += f"""
        QGroupBox {{
            border: {tw.get('groupBorder', '1px solid #ccc')};
            border-radius: {radius};
            margin-top: 1.5em;
            color: {tw.get('groupColor', text_color)};
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
            background-color: {tw.get('tableHeaderBg', '#eee')};
            color: {list_color};
            padding: 4px;
            border: 0px;
            border-bottom: 1px solid #ccc;
        }}
        """

        # Tabs
        qss += f"""
        QTabWidget::pane {{
            border: {tw.get('tabBorder', '1px solid #ccc')};
            border-radius: {radius};
            background-color: {tw.get('tabActiveBg', '#fff')};
        }}
        QTabBar::tab {{
            background-color: {tw.get('tabBarBg', '#eee')};
            color: {tw.get('tabColor', '#000')};
            padding: 6px 12px;
            border-top-left-radius: {radius};
            border-top-right-radius: {radius};
            margin-right: 2px;
        }}
        QTabBar::tab:selected {{
            background-color: {tw.get('tabActiveBg', '#fff')};
            border-bottom-color: {tw.get('tabActiveBg', '#fff')};
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

    def build_hierarchy(self):
        nodes = []
        for i, e in enumerate(self.elements):
            n = e.copy()
            n['_original_idx'] = i
            n['children'] = []
            nodes.append(n)

        roots = []
        # Sort by area (width * height) ascending
        sorted_nodes = sorted(nodes, key=lambda x: x['w'] * x['h'])

        container_types = {'QGroupBox', 'QTabWidget', 'QFrame', 'QScrollArea', 'QStackedWidget', 'QToolBox', 'QDockWidget'}

        for node in sorted_nodes:
            best_parent = None
            min_area = float('inf')

            for potential_parent in nodes:
                if node['id'] == potential_parent['id']:
                    continue
                if potential_parent['type'] not in container_types:
                    continue

                # Check containment
                if (node['x'] >= potential_parent['x'] and
                    node['y'] >= potential_parent['y'] and
                    node['x'] + node['w'] <= potential_parent['x'] + potential_parent['w'] and
                    node['y'] + node['h'] <= potential_parent['y'] + potential_parent['h']):

                    area = potential_parent['w'] * potential_parent['h']
                    if area < min_area:
                        min_area = area
                        best_parent = potential_parent

            if best_parent:
                best_parent['children'].append(node)
            else:
                roots.append(node)

        # Re-sort roots and children by original index (Z-order)
        roots.sort(key=lambda x: x['_original_idx'])

        def sort_children(n):
            if n['children']:
                n['children'].sort(key=lambda x: x['_original_idx'])
                for c in n['children']:
                    sort_children(c)

        for r in roots:
            sort_children(r)

        return roots

    def _prop(self, name, type_, val, indent):
        if type_ == 'string':
            return f'{indent}<property name="{name}"><string>{esc_xml(val)}</string></property>\n'
        elif type_ == 'bool':
            v = 'true' if val else 'false'
            return f'{indent}<property name="{name}"><bool>{v}</bool></property>\n'
        elif type_ == 'number':
            return f'{indent}<property name="{name}"><number>{val}</number></property>\n'
        elif type_ == 'enum':
            return f'{indent}<property name="{name}"><enum>{val}</enum></property>\n'
        elif type_ == 'set':
            return f'{indent}<property name="{name}"><set>{val}</set></property>\n'
        return ''

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

    def _gen_widget(self, el, rx, ry, indent='    '):
        # Mappings
        xml_cls = el['type']
        if xml_cls == 'VLine' or xml_cls == 'HLine':
            xml_cls = 'Line'
        elif xml_cls == 'QImage':
            xml_cls = 'QLabel'

        # Whitelists
        HAS_TEXT = {'QPushButton','QToolButton','QLabel','QLineEdit','QTextEdit','QPlainTextEdit','QCheckBox','QRadioButton','QGroupBox','QImage','QCommandLinkButton','QDockWidget'}
        HAS_ALIGN = {'QLabel','QLineEdit','QImage','QProgressBar'}
        HAS_PLACEHOLDER = {'QLineEdit','QTextEdit','QPlainTextEdit'}
        HAS_READONLY = {'QLineEdit','QTextEdit','QPlainTextEdit','QSpinBox','QDoubleSpinBox','QDateEdit','QTimeEdit','QDateTimeEdit'}
        HAS_FLAT = {'QPushButton','QGroupBox'}
        HAS_CHECKABLE = {'QPushButton','QToolButton','QGroupBox','QCheckBox','QRadioButton'}
        HAS_CHECKED = {'QPushButton','QToolButton','QCheckBox','QRadioButton','QGroupBox'}
        HAS_AUTOFILL = {'QLabel', 'QCheckBox', 'QRadioButton'}

        props = ''

        # Geometry
        props += f'{indent}<property name="geometry"><rect><x>{int(rx)}</x><y>{int(ry)}</y><width>{int(el["w"])}</width><height>{int(el["h"])}</height></rect></property>\n'

        # Identity
        if el.get('objectName'):
            pass # We use el['name'] in widget tag

        # AutoFillBackground for labels if themed
        if el['type'] in HAS_AUTOFILL and self.include_theme and self.theme.get('widget', {}).get('defaultBg'):
            props += self._prop('autoFillBackground', 'bool', True, indent)

        # Text
        if el.get('text') and el['type'] in HAS_TEXT:
            prop_name = 'text'
            if el['type'] == 'QGroupBox': prop_name = 'title'
            if el['type'] == 'QDockWidget': prop_name = 'windowTitle'
            props += self._prop(prop_name, 'string', el['text'], indent)

        if el.get('description') and el['type'] == 'QCommandLinkButton':
            props += self._prop('description', 'string', el['description'], indent)

        # Common
        if el.get('tooltip'): props += self._prop('toolTip', 'string', el['tooltip'], indent)
        if el.get('statusTip'): props += self._prop('statusTip', 'string', el['statusTip'], indent)
        if 'enabled' in el and not el['enabled']: props += self._prop('enabled', 'bool', False, indent)
        if 'visible' in el and not el['visible']: props += self._prop('visible', 'bool', False, indent)

        # Properties
        if el.get('readOnly') and el['type'] in HAS_READONLY: props += self._prop('readOnly', 'bool', True, indent)
        if el.get('placeholderText') and el['type'] in HAS_PLACEHOLDER: props += self._prop('placeholderText', 'string', el['placeholderText'], indent)
        if el.get('flat') and el['type'] in HAS_FLAT: props += self._prop('flat', 'bool', True, indent)
        if el.get('checkable') and el['type'] in HAS_CHECKABLE: props += self._prop('checkable', 'bool', True, indent)
        if el.get('checked') and el['type'] in HAS_CHECKED: props += self._prop('checked', 'bool', True, indent)

        # Values
        if 'value' in el and el['type'] in {'QProgressBar', 'QSlider', 'QSpinBox', 'QDoubleSpinBox', 'QLCDNumber'}:
            props += self._prop('value', 'number', el['value'], indent)
        if 'minimum' in el and el['type'] in {'QProgressBar', 'QSlider', 'QSpinBox', 'QDoubleSpinBox'}:
            props += self._prop('minimum', 'number', el['minimum'], indent)
        if 'maximum' in el and el['type'] in {'QProgressBar', 'QSlider', 'QSpinBox', 'QDoubleSpinBox'}:
            props += self._prop('maximum', 'number', el['maximum'], indent)

        # Style (User Override Only)
        user_style = self.get_user_style_overrides(el)
        if user_style:
            props += self._prop('styleSheet', 'string', user_style, indent)

        # Alignment
        if el['type'] in HAS_ALIGN:
            als = []
            h, v = el.get('hAlign'), el.get('vAlign')
            if h == 'left': als.append('Qt::AlignLeft')
            elif h == 'right': als.append('Qt::AlignRight')
            elif h == 'justify': als.append('Qt::AlignJustify')
            elif h == 'center': als.append('Qt::AlignHCenter')

            if v == 'top': als.append('Qt::AlignTop')
            elif v == 'bottom': als.append('Qt::AlignBottom')
            elif v == 'center': als.append('Qt::AlignVCenter')

            if als:
                props += self._prop('alignment', 'set', '|'.join(als), indent)

        # Extra
        extra = ''
        if el['type'] == 'VLine': extra += self._prop('orientation', 'enum', 'Qt::Vertical', indent)
        if el['type'] == 'HLine': extra += self._prop('orientation', 'enum', 'Qt::Horizontal', indent)

        if el['type'] == 'QComboBox':
            for item in el.get('items', []):
                extra += f'{indent}<item><property name="text"><string>{esc_xml(item)}</string></property></item>\n'

        if el['type'] == 'QTabWidget':
            for i, tab in enumerate(el.get('tabs', [])):
                extra += f'{indent}<widget class="QWidget" name="tab_{el["name"]}_{i}"><attribute name="title"><string>{esc_xml(tab)}</string></attribute></widget>\n'

        # Recursive Children
        child_xml = ''
        if 'children' in el:
            for child in el['children']:
                child_xml += self._gen_widget(child, child['x'] - el['x'], child['y'] - el['y'], indent + '  ')

        return f'{indent}<widget class="{xml_cls}" name="{el["name"]}">\n{props}{extra}{child_xml}{indent}</widget>\n'

    def generate(self):
        roots = self.build_hierarchy()
        wxml = ''
        for el in roots:
            wxml += self._gen_widget(el, el['x'], el['y'], '    ')

        # Global Style Injection
        style_prop = ""
        if self.include_theme:
            global_style = self.generate_stylesheet()
            if global_style:
                style_prop = f'<property name="styleSheet"><string>{esc_xml(global_style)}</string></property>'

        # We need to wrap the user content in a fixed-size container widget,
        # which is then placed inside the QGraphicsView.
        # However, standard .ui files are strict about hierarchy.
        # We'll set the central widget to be a QGraphicsView.
        # But QGraphicsView in .ui doesn't easily allow adding a "scene" or "container" internally via XML.
        # The standard way is: centralwidget -> QGraphicsView.
        # The "content" must be loaded separately or added via code.
        # BUT, to make the .ui useful on its own, we usually want the widgets visible.
        # If we put them in a QGraphicsView, they won't show up unless we use a scene.

        # A workaround for the "ScaleAwareLoader" plan:
        # We generate the XML *exactly* as before (centralwidget -> widgets),
        # BUT we wrap them all in a single QWidget container named "design_container".
        # Then the Loader script will:
        # 1. Load the UI.
        # 2. Take "design_container" out.
        # 3. Create a QGraphicsView/Scene.
        # 4. Put "design_container" into the scene.
        # 5. Set QGraphicsView as central widget.

        # This keeps the .ui file viewable in standard Designer (mostly) and makes the loader logic simple.

        return f"""<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry"><rect><x>0</x><y>0</y><width>{int(self.canvas_size['w'])}</width><height>{int(self.canvas_size['h'])}</height></rect></property>
  <property name="windowTitle"><string>{esc_xml(self.window_title)}</string></property>
  <widget class="QWidget" name="centralwidget">
   {style_prop}
   <widget class="QWidget" name="design_container">
    <property name="geometry"><rect><x>0</x><y>0</y><width>{int(self.canvas_size['w'])}</width><height>{int(self.canvas_size['h'])}</height></rect></property>
{wxml}   </widget>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
{self._gen_connections()}</ui>"""

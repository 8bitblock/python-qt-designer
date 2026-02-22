import json

def esc_xml(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

class UIGenerator:
    def __init__(self, elements, canvas_size, window_title, theme_data, pyqt_version=6, include_theme=True):
        self.elements = elements
        self.canvas_size = canvas_size
        self.window_title = window_title
        self.theme = theme_data
        self.pyqt_version = pyqt_version
        self.include_theme = include_theme

    def get_global_style(self):
        if not self.include_theme or not self.theme:
            return ""

        def_bg = self.theme.get('widget', {}).get('defaultBg', '')
        txt = self.theme.get('ide', {}).get('text', '#000000')
        btn_border = self.theme.get('widget', {}).get('btnBorder', '#555')
        input_bg = self.theme.get('widget', {}).get('inputBg', def_bg)
        input_border = self.theme.get('widget', {}).get('inputBorder', '#555')
        combo_bg = self.theme.get('widget', {}).get('comboBg', def_bg)
        combo_border = self.theme.get('widget', {}).get('comboBorder', '#555')
        group_border = self.theme.get('widget', {}).get('groupBorder', '#555')

        css = f"QWidget{{color:{txt};}}"

        if def_bg:
            css += f"""
            QPushButton, QToolButton, QCommandLinkButton{{background-color:{def_bg};border:1px solid {btn_border};border-radius:4px;padding:4px;}}
            QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QTimeEdit, QDateTimeEdit{{background-color:{input_bg};border:1px solid {input_border};border-radius:3px;}}
            QComboBox, QFontComboBox{{background-color:{combo_bg};border:1px solid {combo_border};border-radius:3px;}}
            QLabel, QCheckBox, QRadioButton{{background-color:{def_bg};padding:2px;border-radius:2px;}}
            QGroupBox{{border:1px solid {group_border};border-radius:4px;margin-top:1.5em;}}
            QGroupBox::title{{subcontrol-origin:margin;subcontrol-position:top left;padding:0 3px;}}
            """
        return css.replace('\n', ' ').strip()

    def build_hierarchy(self):
        nodes = [e.copy() for e in self.elements]
        for n in nodes:
            n['children'] = []

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

    def _gen_widget(self, el, rx, ry, indent='    '):
        # Mappings
        xml_cls = el['type']
        if xml_cls == 'VLine' or xml_cls == 'HLine':
            xml_cls = 'Line'

        # Whitelists
        HAS_TEXT = {'QPushButton','QToolButton','QLabel','QLineEdit','QTextEdit','QPlainTextEdit','QCheckBox','QRadioButton','QGroupBox','QImage','QCommandLinkButton','QDockWidget'}
        HAS_ALIGN = {'QLabel','QLineEdit','QImage','QProgressBar'}
        HAS_PLACEHOLDER = {'QLineEdit','QTextEdit','QPlainTextEdit'}
        HAS_READONLY = {'QLineEdit','QTextEdit','QPlainTextEdit','QSpinBox','QDoubleSpinBox','QDateEdit','QTimeEdit','QDateTimeEdit'}
        HAS_FLAT = {'QPushButton','QGroupBox'}
        HAS_CHECKABLE = {'QPushButton','QToolButton','QGroupBox','QCheckBox','QRadioButton'}
        HAS_CHECKED = {'QPushButton','QToolButton','QCheckBox','QRadioButton','QGroupBox'}

        props = ''

        # Geometry
        props += f'{indent}<property name="geometry"><rect><x>{int(rx)}</x><y>{int(ry)}</y><width>{int(el["w"])}</width><height>{int(el["h"])}</height></rect></property>\n'

        # Identity
        if el.get('objectName'): # Usually handled by name attribute in widget tag, but strictly speaking XML uses name attr
            pass # We use el['name'] in widget tag

        # Text
        if el.get('text') and el['type'] in HAS_TEXT and el['type'] != 'QComboBox':
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

        # Style
        # Local StyleSheet (User override)
        ss = el.get('styleSheet', '')
        # If we are NOT exporting global theme, we might want to inject local colors if user set them explicitly
        # But our frontend sets specific props like 'bg', 'color'.
        # If include_theme is False, we should probably ONLY output manually set styleSheet,
        # or maybe we should still output local overrides?
        # User said "not a universal style sheet".
        # I will assume local overrides (bg, color props) are INTENTIONAL styling by user, so I keep them.

        if el.get('bg'): ss += f"background-color:{el['bg']};"
        if el.get('color'): ss += f"color:{el['color']};"
        if el.get('fontSize'): ss += f"font-size:{el['fontSize']}pt;"
        if el.get('fontFamily'): ss += f"font-family:'{el['fontFamily']}';"
        if el.get('fontWeight') == 'bold': ss += "font-weight:bold;"
        if el.get('fontItalic'): ss += "font-style:italic;"

        if ss:
            props += self._prop('styleSheet', 'string', ss, indent)

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
            wxml += self._gen_widget(el, el['x'], el['y'], '   ')

        # Global Style
        main_style = ""
        if self.include_theme:
            canvas_bg = self.theme.get('canvas', '#f0f0f0') if self.theme else '#f0f0f0'
            global_css = self.get_global_style()
            main_style = f"background-color:{canvas_bg};" + global_css

        style_prop = ""
        if main_style:
            style_prop = f'<property name="styleSheet"><string>{esc_xml(main_style)}</string></property>'

        return f"""<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry"><rect><x>0</x><y>0</y><width>{int(self.canvas_size['w'])}</width><height>{int(self.canvas_size['h'])}</height></rect></property>
  <property name="windowTitle"><string>{esc_xml(self.window_title)}</string></property>
  <widget class="QWidget" name="centralwidget">
   {style_prop}
{wxml}  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
</ui>"""

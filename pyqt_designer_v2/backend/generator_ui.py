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

    def get_widget_style(self, cls):
        """Returns the specific style for a widget class based on the theme."""
        if not self.include_theme or not self.theme:
            return ""

        tw = self.theme.get('widget', {})
        styles = []

        if cls in ['QPushButton', 'QToolButton', 'QCommandLinkButton']:
            bg = tw.get('btnBg') or tw.get('defaultBg')
            border = tw.get('btnBorder')
            color = tw.get('btnColor')
            if bg: styles.append(f"background-color:{bg}")
            if border: styles.append(f"border:1px solid {border}")
            if color: styles.append(f"color:{color}")
            styles.append("border-radius:4px;padding:4px")

        elif cls in ['QLineEdit', 'QTextEdit', 'QPlainTextEdit', 'QSpinBox', 'QDoubleSpinBox', 'QDateEdit', 'QTimeEdit', 'QDateTimeEdit']:
            bg = tw.get('inputBg') or tw.get('defaultBg')
            border = tw.get('inputBorder')
            color = tw.get('inputColor')
            if bg: styles.append(f"background-color:{bg}")
            if border: styles.append(f"border:1px solid {border}")
            if color: styles.append(f"color:{color}")
            styles.append("border-radius:3px")

        elif cls in ['QComboBox', 'QFontComboBox']:
            bg = tw.get('comboBg') or tw.get('defaultBg')
            border = tw.get('comboBorder')
            color = tw.get('comboColor')
            if bg: styles.append(f"background-color:{bg}")
            if border: styles.append(f"border:1px solid {border}")
            if color: styles.append(f"color:{color}")
            styles.append("border-radius:3px")

        elif cls in ['QLabel', 'QCheckBox', 'QRadioButton']:
            bg = tw.get('defaultBg')
            color = tw.get('labelColor')
            if cls in ['QCheckBox', 'QRadioButton']: color = tw.get('checkColor')

            if bg: styles.append(f"background-color:{bg}")
            if color: styles.append(f"color:{color}")
            styles.append("padding:2px;border-radius:2px")

        elif cls == 'QGroupBox':
            border = tw.get('groupBorder')
            color = tw.get('groupColor')
            if border: styles.append(f"border:1px solid {border}")
            if color: styles.append(f"color:{color}")
            styles.append("border-radius:4px;margin-top:1.5em")

        elif cls in ['QListWidget', 'QTreeWidget', 'QTableWidget']:
             bg = tw.get('listBg')
             color = tw.get('listColor')
             border = tw.get('listBorder')
             if bg: styles.append(f"background-color:{bg}")
             if color: styles.append(f"color:{color}")
             if border: styles.append(f"border:1px solid {border}")

        return ";".join(styles)

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

        # Style (Inline + User Override)
        theme_style = self.get_widget_style(el['type'])
        user_style = el.get('styleSheet', '')

        # Additional User Props overrides (bg, color)
        if el.get('bg'): user_style += f"background-color:{el['bg']};"
        if el.get('color'): user_style += f"color:{el['color']};"
        if el.get('fontSize'): user_style += f"font-size:{el['fontSize']}pt;"
        if el.get('fontFamily'): user_style += f"font-family:'{el['fontFamily']}';"
        if el.get('fontWeight') == 'bold': user_style += "font-weight:bold;"
        if el.get('fontItalic'): user_style += "font-style:italic;"

        final_style = theme_style
        if user_style:
            final_style = final_style + ";" + user_style if final_style else user_style

        if el['type'] in ['QPushButton', 'QToolButton', 'QCommandLinkButton'] and self.include_theme:
            pressed_bg = self.theme.get('widget', {}).get('btnPressedBg')
            if pressed_bg:
                pressed_style = f"{el['type']}:pressed{{background:{pressed_bg};border-style:inset;padding:5px 3px 3px 5px}}"
                if final_style:
                    final_style = f"{final_style};{pressed_style}"
                else:
                    final_style = pressed_style

        if final_style:
            props += self._prop('styleSheet', 'string', final_style, indent)

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

        # Global Style (Only Canvas BG)
        main_style = ""
        if self.include_theme:
            canvas_bg = self.theme.get('canvas', '#f0f0f0') if self.theme else '#f0f0f0'
            txt = self.theme.get('ide', {}).get('text', '#000000') if self.theme else '#000000'
            main_style = f"background-color:{canvas_bg};color:{txt};"

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

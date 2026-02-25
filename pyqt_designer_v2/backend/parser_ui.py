import xml.etree.ElementTree as ET
import json
import uuid

class UIParser:
    def __init__(self):
        self.elements = []
        self.meta = {}
        self.canvas_size = {'w': 800, 'h': 600}
        self.window_title = "MainWindow"

    def parse(self, xml_content):
        # Reset state
        self.elements = []
        self.meta = {}

        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError as e:
            print(f"XML Parse Error: {e}")
            return None

        # Determine Root Widget
        # Standard .ui has <ui version="4.0"> <class>...</class> <widget class="..." name="..."> ... </widget> </ui>
        # Sometimes the root is just <widget> if it's a snippet? No, standard is <ui>.

        main_widget = None
        for child in root:
            if child.tag == "widget":
                main_widget = child
                break

        if main_widget is None:
            # Maybe root IS the widget (non-standard but possible)
            if root.tag == "widget":
                main_widget = root
            else:
                return None

        # Window Properties
        self.window_title = self._get_prop_val(main_widget, "windowTitle") or "MainWindow"
        rect = self._get_rect(main_widget)
        if rect:
            self.canvas_size = {'w': rect['w'], 'h': rect['h']}

        # Determine where to start parsing children (CentralWidget or Direct)
        start_node = main_widget
        start_x = 0
        start_y = 0

        # If it's QMainWindow, we look for centralwidget
        is_mainwindow = main_widget.get("class") == "QMainWindow"
        if is_mainwindow:
            central = None
            for child in main_widget:
                if child.tag == "widget" and child.get("name") == "centralwidget":
                    central = child
                    break

            if central is not None:
                start_node = central
                # centralwidget usually has geometry 0,0 relative to window content area
                # We treat its top-left as 0,0 for our canvas.
            else:
                # Fallback
                pass

        # Check for 'design_container' wrapper (workaround for AutoScaler)
        # If found, we must unwrap it to avoid nested containers on re-import
        container = None
        for child in start_node:
            if child.tag == "widget" and child.get("name") == "design_container":
                container = child
                break

        if container is not None:
            start_node = container

        # Parse children
        # Note: We do NOT add the main window / central widget itself to the elements list,
        # as it represents the canvas container.
        self._parse_children(start_node, 0, 0)

        return {
            "elements": self.elements,
            "meta": {
                "canvasSize": self.canvas_size,
                "windowTitle": self.window_title,
                "theme": {},
                "pyqtVersion": 6,
                "exportTheme": True
            }
        }

    def _parse_children(self, parent_node, current_abs_x, current_abs_y):
        for child in parent_node:
            if child.tag == "widget":
                self._process_widget(child, current_abs_x, current_abs_y)
            elif child.tag == "layout":
                self._process_layout(child, current_abs_x, current_abs_y)

    def _process_layout(self, layout_node, parent_abs_x, parent_abs_y):
        # Layouts don't have geometry in the same way.
        # We simulate a "flow" layout for import purposes if geometry is missing.
        offset_y = 0

        for item in layout_node:
            if item.tag == "item":
                # Check for widget
                widget = item.find("widget")
                if widget is not None:
                    # Place it
                    self._process_widget(widget, parent_abs_x, parent_abs_y + offset_y, from_layout=True)
                    offset_y += 40 # Spacing

                # Check for nested layout
                layout = item.find("layout")
                if layout is not None:
                    self._process_layout(layout, parent_abs_x + 20, parent_abs_y + offset_y)
                    offset_y += 40

    def _process_widget(self, node, parent_abs_x, parent_abs_y, from_layout=False):
        w_class = node.get("class")
        w_name = node.get("name")

        if from_layout:
            # Use passed coordinates
            x, y, w, h = 0, 0, 100, 30
            # Try to get size hint from property if available (rare in XML directly)
            final_x = parent_abs_x
            final_y = parent_abs_y
        else:
            rect = self._get_rect(node)
            if not rect:
                rect = {'x': 0, 'y': 0, 'w': 100, 'h': 30}

            x, y, w, h = rect['x'], rect['y'], rect['w'], rect['h']
            final_x = parent_abs_x + x
            final_y = parent_abs_y + y

        el = {
            "id": str(uuid.uuid4()),
            "name": w_name,
            "type": self._map_class(w_class, node),
            "x": final_x,
            "y": final_y,
            "w": w,
            "h": h
        }

        # Properties
        self._extract_props(node, el)

        self.elements.append(el)

        # Recurse
        self._parse_children(node, final_x, final_y)

    def _map_class(self, w_class, node):
        if w_class == "Line":
            # Check orientation
            orient = self._get_prop_val(node, "orientation")
            return "VLine" if orient == "Qt::Vertical" else "HLine"
        return w_class

    def _extract_props(self, node, el):
        # Text
        text = self._get_prop_val(node, "text")
        if not text and el["type"] == "QGroupBox":
            text = self._get_prop_val(node, "title")
        if text: el["text"] = text

        # Checkable
        if self._get_prop_val(node, "checkable") == "true": el["checkable"] = True
        if self._get_prop_val(node, "checked") == "true": el["checked"] = True

        # Stylesheet
        ss = self._get_prop_val(node, "styleSheet")
        if ss: el["styleSheet"] = ss

        # Tooltip
        tt = self._get_prop_val(node, "toolTip")
        if tt: el["tooltip"] = tt

        # Value
        val = self._get_prop_val(node, "value")
        if val:
            try: el["value"] = float(val)
            except: pass

    def _get_rect(self, node):
        for prop in node.findall("property"):
            if prop.get("name") == "geometry":
                rect = prop.find("rect")
                if rect is not None:
                    return {
                        'x': int(rect.find("x").text),
                        'y': int(rect.find("y").text),
                        'w': int(rect.find("width").text),
                        'h': int(rect.find("height").text)
                    }
        return None

    def _get_prop_val(self, node, name):
        for prop in node.findall("property"):
            if prop.get("name") == name:
                for tag in ['string', 'bool', 'number', 'enum', 'set', 'cstring']:
                    val = prop.find(tag)
                    if val is not None:
                        return val.text
        return None

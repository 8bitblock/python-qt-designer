// Namespace
window.Designer = window.Designer || {};

window.Designer.FONT_FAMILIES = ['Segoe UI','Arial','Helvetica Neue','Times New Roman','Courier New','Verdana','Georgia','Trebuchet MS','Tahoma','Palatino','Lucida Console','Consolas','Roboto','Open Sans','monospace','sans-serif','serif'];

window.Designer.THEMES = {
    midnight: {
        name: 'Midnight',
        swatch: '#1e1e1e',
        ide: {
            bg: '#1e1e1e', bg2: '#252526', bg3: '#37373d', bg4: '#454545',
            border: '#333333', border2: '#404040',
            text: '#ffffff', text2: '#cccccc', text3: '#909090',
            accent: '#007acc', accent2: '#005a9e', 'accent-glow': 'rgba(0,122,204,0.15)',
            red: '#f48771', green: '#89d185', yellow: '#cca700', purple: '#c586c0'
        },
        canvas: '#1e1e1e',
        widget: {
            defaultBg: '#2d3d4d',
            btnBg: 'linear-gradient(180deg,#3a3a3a,#303030)', btnBorder: '#555555', btnColor: '#ffffff',
            inputBg: '#303030', inputBorder: '#555555', inputColor: '#ffffff',
            comboBg: '#303030', comboBorder: '#555555', comboColor: '#ffffff',
            checkColor: '#ffffff', groupBorder: '#555555', groupColor: '#ffffff',
            frameBorder: '#555555',
            progressBg: '#252526', progressBorder: '#555555', progressFill: 'linear-gradient(90deg,#007acc,#0098ff)',
            sliderTrack: '#444444', sliderThumb: '#007acc', sliderThumbBorder: '#fff',
            spinBg: '#303030', spinBorder: '#555555', spinColor: '#ffffff',
            lcdBg: '#000000', lcdColor: '#00ff00',
            listBg: '#252526', listBorder: '#555555', listColor: '#ffffff', listSelBg: '#004c75', listSelColor: '#ffffff', listItemBorder: '#3e3e3e',
            treeBg: '#252526', treeBorder: '#555555', treeColor: '#ffffff',
            tableBg: '#252526', tableBorder: '#555555', tableColor: '#ffffff', tableHeaderBg: '#3e3e3e',
            tabBarBg: '#252526', tabActiveBg: '#1e1e1e', tabBorder: '#555555', tabColor: '#ffffff',
            calBg: '#252526', calBorder: '#555555', calColor: '#ffffff', calHeaderBg: '#3e3e3e', calCellColor: '#ffffff',
            dateBg: '#303030', dateBorder: '#555555', dateColor: '#ffffff',
            scrollBg: '#3e3e3e',
            dialBg: 'conic-gradient(from 220deg,#007acc 0%,#007acc 45%,#333333 45%,#333333 100%)', dialBorder: '#555555',
            labelColor: '#ffffff'
        }
    },
    snow: {
        name: 'Snow',
        swatch: '#ffffff',
        ide: {
            bg: '#f3f3f3', bg2: '#ffffff', bg3: '#e8e8e8', bg4: '#d0d0d0',
            border: '#e0e0e0', border2: '#c0c0c0',
            text: '#202020', text2: '#444444', text3: '#666666',
            accent: '#0078d4', accent2: '#0067b8', 'accent-glow': 'rgba(0,120,212,0.1)',
            red: '#d13438', green: '#107c10', yellow: '#ffb900', purple: '#881798'
        },
        canvas: '#ffffff',
        widget: {
            defaultBg: '#e5e5e5',
            btnBg: 'linear-gradient(180deg,#f0f0f0,#e0e0e0)', btnBorder: '#bbbbbb', btnColor: '#000000',
            inputBg: '#f5f5f5', inputBorder: '#bbbbbb', inputColor: '#000000',
            comboBg: '#f5f5f5', comboBorder: '#bbbbbb', comboColor: '#000000',
            checkColor: '#000000', groupBorder: '#bbbbbb', groupColor: '#000000',
            frameBorder: '#bbbbbb',
            progressBg: '#e6e6e6', progressBorder: '#bbbbbb', progressFill: 'linear-gradient(90deg,#0078d4,#00bcf2)',
            sliderTrack: '#d0d0d0', sliderThumb: '#ffffff', sliderThumbBorder: '#0078d4',
            spinBg: '#f5f5f5', spinBorder: '#bbbbbb', spinColor: '#000000',
            lcdBg: '#000000', lcdColor: '#00ff00',
            listBg: '#ffffff', listBorder: '#bbbbbb', listColor: '#000000', listSelBg: '#cde6f7', listSelColor: '#000000', listItemBorder: '#f0f0f0',
            treeBg: '#ffffff', treeBorder: '#bbbbbb', treeColor: '#000000',
            tableBg: '#ffffff', tableBorder: '#bbbbbb', tableColor: '#000000', tableHeaderBg: '#f0f0f0',
            tabBarBg: '#f0f0f0', tabActiveBg: '#ffffff', tabBorder: '#bbbbbb', tabColor: '#000000',
            calBg: '#ffffff', calBorder: '#bbbbbb', calColor: '#000000', calHeaderBg: '#f0f0f0', calCellColor: '#000000',
            dateBg: '#f5f5f5', dateBorder: '#bbbbbb', dateColor: '#000000',
            scrollBg: '#f0f0f0',
            dialBg: 'conic-gradient(from 220deg,#0078d4 0%,#0078d4 45%,#e0e0e0 45%,#e0e0e0 100%)', dialBorder: '#cccccc',
            labelColor: '#000000'
        }
    },
    classic: {
        name: 'Classic',
        swatch: '#c0c0c0',
        ide: {
            bg: '#d4d0c8', bg2: '#ece9d8', bg3: '#f7f6f2', bg4: '#aaa',
            border: '#888', border2: '#666',
            text: '#000', text2: '#333', text3: '#555',
            accent: '#000080', accent2: '#1020a0', 'accent-glow': 'rgba(0,0,128,0.1)',
            red: '#c00', green: '#080', yellow: '#aa0', purple: '#808'
        },
        canvas: '#d4d0c8',
        widget: {
            defaultBg: '#ffffff',
            btnBg: 'linear-gradient(180deg,#fff,#ece9d8)', btnBorder: '#777', btnColor: '#000',
            inputBg: '#fff', inputBorder: '#777', inputColor: '#000',
            comboBg: '#fff', comboBorder: '#777', comboColor: '#000',
            checkColor: '#000', groupBorder: '#777', groupColor: '#000',
            frameBorder: '#777',
            progressBg: '#fff', progressBorder: '#777', progressFill: 'linear-gradient(90deg,#000080,#0000ff)',
            sliderTrack: '#999', sliderThumb: '#ece9d8', sliderThumbBorder: '#444',
            spinBg: '#fff', spinBorder: '#777', spinColor: '#000',
            lcdBg: '#000', lcdColor: '#0f0',
            listBg: '#fff', listBorder: '#777', listColor: '#000', listSelBg: '#000080', listSelColor: '#fff', listItemBorder: '#eee',
            treeBg: '#fff', treeBorder: '#777', treeColor: '#000',
            tableBg: '#fff', tableBorder: '#777', tableColor: '#000', tableHeaderBg: '#ece9d8',
            tabBarBg: '#ece9d8', tabActiveBg: '#d4d0c8', tabBorder: '#777', tabColor: '#000',
            calBg: '#fff', calBorder: '#777', calColor: '#000', calHeaderBg: '#ece9d8', calCellColor: '#000',
            dateBg: '#fff', dateBorder: '#777', dateColor: '#000',
            scrollBg: '#ece9d8',
            dialBg: 'conic-gradient(from 220deg,#000080 0%,#000080 45%,#ccc 45%,#ccc 100%)', dialBorder: '#777',
            labelColor: '#000'
        }
    },
    hacker: {
        name: 'Hacker',
        swatch: '#001100',
        ide: {
            bg: '#000a00', bg2: '#001a00', bg3: '#002200', bg4: '#003300',
            border: '#003300', border2: '#004400',
            text: '#00ff00', text2: '#00cc00', text3: '#009900',
            accent: '#00ff00', accent2: '#00cc00', 'accent-glow': 'rgba(0,255,0,0.1)',
            red: '#ff3333', green: '#00ff00', yellow: '#ffff00', purple: '#cc00ff'
        },
        canvas: '#000800',
        widget: {
            defaultBg: '#002800',
            btnBg: 'linear-gradient(180deg,#003a00,#002800)', btnBorder: '#00cc00', btnColor: '#00ff00',
            inputBg: '#001800', inputBorder: '#00bb00', inputColor: '#00ff00',
            comboBg: '#001800', comboBorder: '#00bb00', comboColor: '#00ff00',
            checkColor: '#00ff00', groupBorder: '#00bb00', groupColor: '#00ff00',
            frameBorder: '#00bb00',
            progressBg: '#001800', progressBorder: '#00bb00', progressFill: 'linear-gradient(90deg,#005500,#00ff00)',
            sliderTrack: '#004400', sliderThumb: '#00ff00', sliderThumbBorder: '#000',
            spinBg: '#001800', spinBorder: '#00bb00', spinColor: '#00ff00',
            lcdBg: '#000500', lcdColor: '#00ff00',
            listBg: '#001800', listBorder: '#00bb00', listColor: '#00ff00', listSelBg: '#006600', listSelColor: '#00ff00', listItemBorder: '#003300',
            treeBg: '#001800', treeBorder: '#00bb00', treeColor: '#00ff00',
            tableBg: '#001800', tableBorder: '#00bb00', tableColor: '#00ff00', tableHeaderBg: '#003300',
            tabBarBg: '#003300', tabActiveBg: '#001800', tabBorder: '#00bb00', tabColor: '#00ff00',
            calBg: '#001800', calBorder: '#00bb00', calColor: '#00ff00', calHeaderBg: '#003300', calCellColor: '#00cc00',
            dateBg: '#001800', dateBorder: '#00bb00', dateColor: '#00ff00',
            scrollBg: '#004400',
            dialBg: 'conic-gradient(from 220deg,#00ff00 0%,#00ff00 45%,#004400 45%,#004400 100%)', dialBorder: '#00bb00',
            labelColor: '#00ff00'
        }
    }
};

window.Designer.CATEGORIES = {
    Buttons: { icon: 'mouse-pointer-2', items: ['QPushButton', 'QToolButton', 'QRadioButton', 'QCheckBox', 'QCommandLinkButton'] },
    Input: { icon: 'text-cursor', items: ['QLineEdit', 'QTextEdit', 'QPlainTextEdit', 'QSpinBox', 'QDoubleSpinBox', 'QKeySequenceEdit', 'QComboBox', 'QFontComboBox', 'QDateEdit', 'QTimeEdit', 'QDateTimeEdit'] },
    Display: { icon: 'monitor', items: ['QLabel', 'QProgressBar', 'QLCDNumber', 'QCalendarWidget', 'QImage'] },
    Controls: { icon: 'sliders-horizontal', items: ['QSlider', 'QDial', 'QScrollBar'] },
    Containers: { icon: 'box', items: ['QGroupBox', 'QTabWidget', 'QFrame', 'QScrollArea', 'QStackedWidget', 'QToolBox', 'QDockWidget'] },
    Views: { icon: 'table', items: ['QListWidget', 'QTreeWidget', 'QTableWidget'] },
    Separators: { icon: 'minus', items: ['HLine', 'VLine'] }
};

window.Designer.WIDGETS = {
    QPushButton: { label: 'Push Button', icon: 'mouse-pointer-2', dw: 100, dh: 30, cat: 'Buttons' },
    QCommandLinkButton: { label: 'Command Link', icon: 'arrow-right-circle', dw: 180, dh: 45, cat: 'Buttons' },
    QToolButton: { label: 'Tool Button', icon: 'square', dw: 32, dh: 32, cat: 'Buttons' },
    QLabel: { label: 'Label', icon: 'type', dw: 80, dh: 22, cat: 'Display' },
    QLineEdit: { label: 'Line Edit', icon: 'text-cursor-input', dw: 150, dh: 26, cat: 'Input' },
    QTextEdit: { label: 'Text Edit', icon: 'file-text', dw: 200, dh: 120, cat: 'Input' },
    QPlainTextEdit: { label: 'Plain Text', icon: 'align-left', dw: 200, dh: 120, cat: 'Input' },
    QKeySequenceEdit: { label: 'Key Seq', icon: 'keyboard', dw: 140, dh: 26, cat: 'Input' },
    QGroupBox: { label: 'Group Box', icon: 'box', dw: 240, dh: 160, cat: 'Containers', container: true },
    QTabWidget: { label: 'Tab Widget', icon: 'panel-top', dw: 320, dh: 220, cat: 'Containers', container: true },
    QFrame: { label: 'Frame', icon: 'layout', dw: 200, dh: 150, cat: 'Containers', container: true },
    QScrollArea: { label: 'Scroll Area', icon: 'scroll', dw: 200, dh: 150, cat: 'Containers', container: true },
    QStackedWidget: { label: 'Stacked', icon: 'layers', dw: 200, dh: 150, cat: 'Containers', container: true },
    QToolBox: { label: 'Tool Box', icon: 'briefcase', dw: 200, dh: 200, cat: 'Containers', container: true },
    QDockWidget: { label: 'Dock Widget', icon: 'panel-right-open', dw: 250, dh: 180, cat: 'Containers', container: true },
    QCheckBox: { label: 'Check Box', icon: 'check-square', dw: 110, dh: 22, cat: 'Buttons' },
    QRadioButton: { label: 'Radio Button', icon: 'circle-dot', dw: 110, dh: 22, cat: 'Buttons' },
    QComboBox: { label: 'Combo Box', icon: 'chevron-down', dw: 130, dh: 26, cat: 'Input' },
    QFontComboBox: { label: 'Font Combo', icon: 'type', dw: 160, dh: 26, cat: 'Input' },
    QProgressBar: { label: 'Progress Bar', icon: 'loader', dw: 200, dh: 22, cat: 'Display' },
    QSlider: { label: 'Slider', icon: 'sliders-horizontal', dw: 160, dh: 22, cat: 'Controls' },
    QScrollBar: { label: 'Scroll Bar', icon: 'grip-vertical', dw: 16, dh: 120, cat: 'Controls' },
    QSpinBox: { label: 'Spin Box', icon: 'hash', dw: 80, dh: 26, cat: 'Input' },
    QDoubleSpinBox: { label: 'Double Spin', icon: 'hash', dw: 90, dh: 26, cat: 'Input' },
    QLCDNumber: { label: 'LCD Number', icon: 'monitor', dw: 80, dh: 34, cat: 'Display' },
    QDial: { label: 'Dial', icon: 'disc', dw: 64, dh: 64, cat: 'Controls' },
    QCalendarWidget: { label: 'Calendar', icon: 'calendar', dw: 280, dh: 200, cat: 'Display' },
    QListWidget: { label: 'List Widget', icon: 'list', dw: 160, dh: 150, cat: 'Views' },
    QTreeWidget: { label: 'Tree Widget', icon: 'git-branch', dw: 160, dh: 150, cat: 'Views' },
    QTableWidget: { label: 'Table Widget', icon: 'table', dw: 240, dh: 150, cat: 'Views' },
    QDateEdit: { label: 'Date Edit', icon: 'calendar', dw: 110, dh: 26, cat: 'Input' },
    QTimeEdit: { label: 'Time Edit', icon: 'clock', dw: 90, dh: 26, cat: 'Input' },
    QDateTimeEdit: { label: 'DateTime', icon: 'calendar-clock', dw: 160, dh: 26, cat: 'Input' },
    QImage: { label: 'Image', icon: 'image', dw: 100, dh: 100, cat: 'Display', xmlClass: 'QLabel' },
    VLine: { label: 'V-Line', icon: 'grip-vertical', dw: 3, dh: 100, cat: 'Separators', xmlClass: 'Line' },
    HLine: { label: 'H-Line', icon: 'grip-horizontal', dw: 100, dh: 3, cat: 'Separators', xmlClass: 'Line' }
};

window.Designer.CURSORS = ["ArrowCursor", "UpArrowCursor", "CrossCursor", "WaitCursor", "IBeamCursor", "SizeVerCursor", "SizeHorCursor", "SizeBDiagCursor", "SizeFDiagCursor", "SizeAllCursor", "BlankCursor", "SplitVCursor", "SplitHCursor", "PointingHandCursor", "ForbiddenCursor", "OpenHandCursor", "ClosedHandCursor", "WhatsThisCursor"];
window.Designer.SIZE_POLICIES = ["Fixed", "Minimum", "Maximum", "Preferred", "Expanding", "MinimumExpanding", "Ignored"];

window.Designer.COMMON_SIGNALS = {
    QAbstractButton: ['clicked()', 'pressed()', 'released()', 'toggled(bool)'],
    QLineEdit: ['textChanged(QString)', 'textEdited(QString)', 'returnPressed()', 'editingFinished()'],
    QComboBox: ['currentIndexChanged(int)', 'currentTextChanged(QString)'],
    QSpinBox: ['valueChanged(int)'],
    QDoubleSpinBox: ['valueChanged(double)'],
    QSlider: ['valueChanged(int)', 'sliderMoved(int)'],
    QListWidget: ['currentRowChanged(int)', 'currentTextChanged(QString)', 'itemClicked(QListWidgetItem*)'],
    QTreeWidget: ['currentItemChanged(QTreeWidgetItem*,QTreeWidgetItem*)', 'itemClicked(QTreeWidgetItem*,int)'],
    QTableWidget: ['cellClicked(int,int)', 'cellChanged(int,int)'],
    QCalendarWidget: ['selectionChanged()', 'activated(QDate)'],
    QDateEdit: ['dateChanged(QDate)'],
    QTimeEdit: ['timeChanged(QTime)'],
    QDateTimeEdit: ['dateTimeChanged(QDateTime)'],
    QKeySequenceEdit: ['keySequenceChanged(QKeySequence)', 'editingFinished()'],
    QDockWidget: ['featuresChanged(QDockWidget::DockWidgetFeatures)', 'topLevelChanged(bool)', 'visibilityChanged(bool)']
};

window.Designer.COMMON_SLOTS = {
    QWidget: ['show()', 'hide()', 'close()', 'update()', 'setDisabled(bool)', 'setEnabled(bool)', 'setVisible(bool)'],
    QLineEdit: ['clear()', 'selectAll()', 'copy()', 'paste()'],
    QTextEdit: ['clear()', 'copy()', 'paste()', 'selectAll()'],
    QAbstractButton: ['click()', 'animateClick()', 'toggle()', 'setChecked(bool)'],
    QComboBox: ['clear()'],
    QProgressBar: ['reset()', 'setValue(int)'],
    QKeySequenceEdit: ['clear()', 'setKeySequence(QKeySequence)']
};

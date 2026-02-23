window.Designer = window.Designer || {};

window.Designer.snap = (v, grid) => Math.round(v / grid) * grid;
window.Designer.clamp = (v, min, max) => Math.max(min, Math.min(max, v));
window.Designer.uid = () => `w${Date.now().toString(36)}${Math.random().toString(36).slice(2, 6)}`;

window.Designer.defaultEl = (type, x, y, idx, gridSize, W) => {
    const c = W[type];
    if (!c) return null;
    return {
        id: window.Designer.uid(),
        type,
        name: `${(c.xmlClass || type).replace('Q', '').toLowerCase()}_${idx}`,
        x: window.Designer.snap(x, gridSize),
        y: window.Designer.snap(y, gridSize),
        w: c.dw,
        h: c.dh,
        zIndex: idx,
        locked: false,
        text: type.includes('Button') ? 'Button' : type.includes('Label') ? 'Label' : type === 'QGroupBox' ? 'Group' : '',
        bg: '',
        color: '',
        fontSize: 0,
        fontWeight: 'normal',
        fontItalic: false,
        fontFamily: '',
        enabled: true,
        visible: true,
        tooltip: '',
        statusTip: '',
        items: type === 'QComboBox' ? ['Item 1', 'Item 2', 'Item 3'] : [],
        description: type === 'QCommandLinkButton' ? 'Description...' : '',
        pixmap: '',
        cursor: 'ArrowCursor',
        placeholderText: '',
        readOnly: false,
        flat: false,
        checkable: false,
        checked: false,
        tabs: type === 'QTabWidget' ? ['Tab 1', 'Tab 2'] : [],
        pages: type === 'QStackedWidget' ? ['Page 1', 'Page 2'] : type === 'QToolBox' ? ['Section 1', 'Section 2'] : [],
        hAlign: 'center',
        vAlign: 'center',
        minW: 0,
        minH: 0,
        maxW: 16777215,
        maxH: 16777215,
        sizeH: 'Preferred',
        sizeV: 'Preferred',
        value: type === 'QProgressBar' ? 45 : type === 'QSlider' ? 50 : type === 'QSpinBox' || type === 'QDoubleSpinBox' ? 0 : type === 'QLCDNumber' ? 42 : 0,
        minimum: 0,
        maximum: type === 'QProgressBar' || type === 'QSlider' ? 100 : type === 'QSpinBox' ? 99 : type === 'QDoubleSpinBox' ? 99.99 : 0,
        orientation: type === 'QScrollBar' ? 'vertical' : 'horizontal',
        rows: type === 'QTableWidget' ? 3 : 0,
        columns: type === 'QTableWidget' ? 3 : 0,
        columnHeaders: type === 'QTableWidget' ? ['Col 1', 'Col 2', 'Col 3'] : [],
        echoMode: 'Normal',
        inputMask: '',
        styleSheet: '',
        children: [] // For nesting
    };
};

window.Designer.getSignals = (type, commonSignals) => {
    let sigs = [];
    if (type === 'QPushButton' || type === 'QToolButton' || type === 'QCheckBox' || type === 'QRadioButton' || type === 'QCommandLinkButton') sigs.push(...commonSignals.QAbstractButton);
    else if (commonSignals[type]) sigs.push(...commonSignals[type]);
    return sigs;
};

window.Designer.getSlots = (type, commonSlots) => {
    let slots = [...commonSlots.QWidget];
    if (type === 'QPushButton' || type === 'QToolButton' || type === 'QCheckBox' || type === 'QRadioButton' || type === 'QCommandLinkButton') slots.push(...commonSlots.QAbstractButton);
    else if (commonSlots[type]) slots.push(...commonSlots[type]);
    return slots;
};

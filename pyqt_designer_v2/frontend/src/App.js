window.Designer = window.Designer || {};

const { useState, useEffect, useRef, useCallback } = React;

window.Designer.App = () => {
    const THEMES = window.Designer.THEMES;
    const WIDGETS = window.Designer.WIDGETS;
    const defaultEl = window.Designer.defaultEl;
    const Canvas = window.Designer.Canvas;
    const Sidebar = window.Designer.Sidebar;
    const PropertiesPanel = window.Designer.PropertiesPanel;

    const [elements, setElements] = useState([]);
    const [selectedIds, setSelectedIds] = useState([]);
    const [activeTheme, setActiveTheme] = useState('midnight');
    const [canvasSize, setCanvasSize] = useState({ w: 800, h: 600 });
    const [windowTitle, setWindowTitle] = useState('MainWindow');
    const [leftPanel, setLeftPanel] = useState('widgets');
    const [rightPanel, setRightPanel] = useState('props');
    const [previewMode, setPreviewMode] = useState(false);
    const [snapEnabled, setSnapEnabled] = useState(true);
    const [gridSize, setGridSize] = useState(20);
    const [zoom, setZoom] = useState(1);
    const [widgetSearch, setWidgetSearch] = useState('');
    const [connections, setConnections] = useState([]);

    // New Settings State
    const [pyqtVersion, setPyqtVersion] = useState(6);
    const [exportTheme, setExportTheme] = useState(true);

    const theme = THEMES[activeTheme];
    const primaryEl = elements.find(e => e.id === selectedIds[0]);
    const bridge = window.qt?.webChannelTransport ? window.pyBridge : null;

    useEffect(() => {
        const r = document.documentElement;
        r.style.setProperty('--canvas-bg', theme.canvas);
        Object.entries(theme.ide).forEach(([k, v]) => r.style.setProperty('--' + k, v));
    }, [activeTheme]);

    useEffect(() => {
        if (window.qt) {
            new QWebChannel(qt.webChannelTransport, (ch) => {
                window.pyBridge = ch.objects.pyBridge;
                window.pyBridge.ui_imported.connect((xml) => {
                    console.log("Import not fully implemented in frontend v2 yet");
                });
            });
        }
    }, []);

    const handleAddWidget = (type, x, y) => {
        const n = elements.length + 1;
        const el = defaultEl(type, x, y, n, snapEnabled ? gridSize : 1, WIDGETS);
        if (el) {
            setElements([...elements, el]);
            setSelectedIds([el.id]);
        }
    };

    const handleUpdate = (newElements, commit = true) => {
        setElements(newElements);
    };

    const handlePropChange = (key, val) => {
        setElements(elements.map(el => selectedIds.includes(el.id) ? { ...el, [key]: val } : el));
    };

    const handleCanvasChange = (key, val) => {
        if (key === 'windowTitle') setWindowTitle(val);
        if (key === 'canvasSize') setCanvasSize(val);
    };

    const handleSaveUI = () => {
        if (!window.pyBridge) return alert("Not connected to Python backend");
        const data = {
            elements,
            connections,
            meta: {
                canvasSize,
                windowTitle,
                theme: THEMES[activeTheme],
                pyqtVersion,
                exportTheme
            }
        };
        window.pyBridge.save_ui_file(JSON.stringify(data));
    };

    const handleSavePy = () => {
        if (!window.pyBridge) return alert("Not connected to Python backend");
        const data = {
            elements,
            connections,
            meta: {
                canvasSize,
                windowTitle,
                theme: THEMES[activeTheme],
                pyqtVersion,
                exportTheme
            }
        };
        window.pyBridge.save_python_file(JSON.stringify(data));
    };

    return (
        <div className="flex h-screen w-screen flex-col overflow-hidden select-none">
            <div className="h-12 shrink-0 flex items-center justify-between px-3 border-b" style={{ background: 'var(--bg2)', borderColor: 'var(--border)' }}>
                <div className="flex items-center gap-2">
                    <div className="flex items-center gap-2 mr-3">
                        <div className="w-7 h-7 rounded-md flex items-center justify-center text-white font-bold text-xs" style={{ background: 'var(--accent)' }}>Qt</div>
                        <span className="text-xs font-bold" style={{ color: 'var(--text2)' }}>Designer Pro V2</span>
                    </div>
                    <div className="toolbar-sep" />
                    <button onClick={handleSaveUI} className="toolbar-btn" title="Save .ui"><i data-lucide="save"></i></button>
                    <button onClick={handleSavePy} className="toolbar-btn" title="Export .py"><i data-lucide="file-code"></i></button>
                    <div className="toolbar-sep" />
                    <button onClick={() => setSnapEnabled(!snapEnabled)} className={`toolbar-btn ${snapEnabled ? 'active' : ''}`}><i data-lucide="grid-3x3"></i></button>
                    <button onClick={() => setPreviewMode(!previewMode)} className={`toolbar-btn ${previewMode ? 'active' : ''}`} style={{ color: previewMode ? 'var(--green)' : 'var(--text3)' }}><i data-lucide="play"></i></button>
                </div>
                {/* Global Settings Indicator */}
                <div className="text-[10px] text-zinc-500 font-mono">
                    PyQt{pyqtVersion} | {exportTheme ? 'Theme Export' : 'No Theme'}
                </div>
            </div>

            <div className="flex flex-1 overflow-hidden">
                <Sidebar
                    activeTab={leftPanel}
                    onTabChange={setLeftPanel}
                    widgetSearch={widgetSearch}
                    setWidgetSearch={setWidgetSearch}
                    elements={elements}
                    selectedIds={selectedIds}
                    onSelect={(id, multi) => setSelectedIds(multi ? [...selectedIds, id] : [id])}
                />

                <Canvas
                    elements={elements}
                    selectedIds={selectedIds}
                    canvasSize={canvasSize}
                    canvasBg={theme.canvas}
                    zoom={zoom}
                    theme={theme}
                    previewMode={previewMode}
                    snapEnabled={snapEnabled}
                    gridSize={gridSize}
                    onAddWidget={handleAddWidget}
                    onSelect={(id, shift, raw) => {
                        if (raw) setSelectedIds(id);
                        else if (id === null) setSelectedIds([]);
                        else setSelectedIds(shift ? (selectedIds.includes(id) ? selectedIds : [...selectedIds, id]) : [id]);
                    }}
                    onUpdate={handleUpdate}
                    onContextMenu={(e, id) => {
                        setSelectedIds([id]);
                    }}
                />

                <PropertiesPanel
                    activeTab={rightPanel}
                    onTabChange={setRightPanel}
                    element={primaryEl}
                    onChange={handlePropChange}
                    canvasProps={{ windowTitle, canvasSize }}
                    onCanvasChange={handleCanvasChange}
                    themes={THEMES}
                    activeTheme={activeTheme}
                    onThemeChange={setActiveTheme}
                    connections={connections}
                    pyqtVersion={pyqtVersion}
                    onPyqtVersionChange={setPyqtVersion}
                    exportTheme={exportTheme}
                    onExportThemeChange={setExportTheme}
                />
            </div>
        </div>
    );
};

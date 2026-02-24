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
    const [clipboard, setClipboard] = useState([]);

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
                window.pyBridge.ui_imported.connect((jsonStr) => {
                    try {
                        const data = JSON.parse(jsonStr);
                        if (data.elements) setElements(data.elements);
                        if (data.meta) {
                            if (data.meta.canvasSize) setCanvasSize(data.meta.canvasSize);
                            if (data.meta.windowTitle) setWindowTitle(data.meta.windowTitle);
                        }
                        setSelectedIds([]);
                        setConnections([]);
                    } catch (e) {
                        console.error("Failed to parse imported UI JSON", e);
                    }
                });
            });
        }
    }, []);

    useEffect(() => {
        const handleKeyDown = (e) => {
            if (document.activeElement && (document.activeElement.tagName === 'INPUT' || document.activeElement.tagName === 'TEXTAREA')) return;

            if (['Delete', 'Backspace'].includes(e.key)) {
                if (selectedIds.length > 0) {
                    setElements(prev => prev.filter(el => !selectedIds.includes(el.id)));
                    setSelectedIds([]);
                }
            }
            if ((e.ctrlKey || e.metaKey) && e.key === 'c') {
                e.preventDefault();
                if (selectedIds.length > 0) {
                    setClipboard(elements.filter(el => selectedIds.includes(el.id)));
                }
            }
            if ((e.ctrlKey || e.metaKey) && e.key === 'v') {
                e.preventDefault();
                if (clipboard.length > 0) {
                    const newEls = clipboard.map(el => ({
                        ...el,
                        id: window.Designer.uid(),
                        x: el.x + 20,
                        y: el.y + 20,
                        name: el.name + '_copy'
                    }));
                    setElements(prev => [...prev, ...newEls]);
                    setSelectedIds(newEls.map(el => el.id));
                }
            }
        };
        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [selectedIds, clipboard, elements]);

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

    const handleImportUI = () => {
        if (!window.pyBridge) return alert("Not connected to Python backend");
        window.pyBridge.import_ui_file();
    };

    const handleAddConnection = (conn) => {
        setConnections([...connections, conn]);
    };

    const handleDeleteConnection = (conn) => {
        setConnections(connections.filter(c => c !== conn));
    };

    const handleDuplicate = (ids) => {
        const toDup = elements.filter(el => ids.includes(el.id));
        if (toDup.length === 0) return;

        const newEls = toDup.map(el => ({
            ...el,
            id: window.Designer.uid(),
            x: el.x + 20,
            y: el.y + 20,
            name: el.name + '_copy'
        }));
        setElements(prev => [...prev, ...newEls]);
        setSelectedIds(newEls.map(el => el.id));
    };

    const handleDelete = (ids) => {
        setElements(prev => prev.filter(el => !ids.includes(el.id)));
        setSelectedIds([]);
    };

    const handleMoveElement = (id, direction) => {
        const idx = elements.findIndex(e => e.id === id);
        if (idx === -1) return;
        const newEls = [...elements];
        const el = newEls[idx];
        newEls.splice(idx, 1);

        if (direction === 'front') {
            newEls.push(el);
        } else if (direction === 'back') {
            newEls.unshift(el);
        } else if (direction === 'forward') {
            const newIdx = Math.min(idx + 1, newEls.length);
            newEls.splice(newIdx, 0, el);
        } else if (direction === 'backward') {
            const newIdx = Math.max(idx - 1, 0);
            newEls.splice(newIdx, 0, el);
        }
        setElements(newEls);
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
                    <button onClick={handleImportUI} className="toolbar-btn flex gap-2" title="Import .ui">
                        <i data-lucide="folder-open"></i>
                        <span className="text-[10px] font-bold">Import UI</span>
                    </button>
                    <button onClick={handleSaveUI} className="toolbar-btn flex gap-2" title="Save .ui">
                        <i data-lucide="save"></i>
                        <span className="text-[10px] font-bold">Save UI</span>
                    </button>
                    <button onClick={handleSavePy} className="toolbar-btn flex gap-2" title="Export .py">
                        <i data-lucide="file-code"></i>
                        <span className="text-[10px] font-bold">Export Python</span>
                    </button>
                    <div className="toolbar-sep" />
                    <button onClick={() => setSnapEnabled(!snapEnabled)} className={`toolbar-btn flex gap-2 ${snapEnabled ? 'active' : ''}`}>
                        <i data-lucide="grid-3x3"></i>
                        <span className="text-[10px] font-bold">Snap</span>
                    </button>
                    <button onClick={() => setPreviewMode(!previewMode)} className={`toolbar-btn flex gap-2 ${previewMode ? 'active' : ''}`} style={{ color: previewMode ? 'var(--green)' : 'var(--text3)' }}>
                        <i data-lucide="play"></i>
                        <span className="text-[10px] font-bold">Preview</span>
                    </button>
                </div>
                {/* Global Settings Indicator */}
                <div className="text-[10px] text-[var(--text3)] font-mono">
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
                    onMoveElement={handleMoveElement}
                    onDuplicate={handleDuplicate}
                    onDelete={handleDelete}
                />

                <PropertiesPanel
                    activeTab={rightPanel}
                    onTabChange={setRightPanel}
                    element={primaryEl}
                    elements={elements}
                    onChange={handlePropChange}
                    canvasProps={{ windowTitle, canvasSize }}
                    onCanvasChange={handleCanvasChange}
                    themes={THEMES}
                    activeTheme={activeTheme}
                    onThemeChange={setActiveTheme}
                    connections={connections}
                    onAddConnection={handleAddConnection}
                    onDeleteConnection={handleDeleteConnection}
                    pyqtVersion={pyqtVersion}
                    onPyqtVersionChange={setPyqtVersion}
                    exportTheme={exportTheme}
                    onExportThemeChange={setExportTheme}
                    onMoveElement={handleMoveElement}
                />
            </div>
        </div>
    );
};

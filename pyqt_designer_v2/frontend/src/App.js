window.Designer = window.Designer || {};

const { useState, useEffect, useRef, useCallback, useMemo } = React;

const Ico = ({ name, size = 16 }) => {
    const r = useRef(null);
    useEffect(() => {
        if (window.lucide && r.current) {
            r.current.textContent = '';
            const i = document.createElement('i');
            i.dataset.lucide = name;
            r.current.appendChild(i);
            window.lucide.createIcons({ attrs: { width: size, height: size }, nameAttr: 'data-lucide', root: r.current });
        }
    }, [name, size]);
    return <span ref={r} className="inline-flex items-center justify-center pointer-events-none" />;
};

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
    const [hoverId, setHoverId] = useState(null);

    // Undo/Redo State
    const [history, setHistory] = useState([]);
    const [future, setFuture] = useState([]);

    // New Settings State
    const [pyqtVersion, setPyqtVersion] = useState(6);
    const [exportTheme, setExportTheme] = useState(true);

    const theme = THEMES[activeTheme];
    const primaryEl = useMemo(() => elements.find(e => e.id === selectedIds[0]), [elements, selectedIds[0]]);
    const bridge = window.qt?.webChannelTransport ? window.pyBridge : null;

    const saveHistory = () => {
        setHistory(prev => [...prev, elements]);
        setFuture([]);
    };

    const handleUndo = () => {
        if (history.length === 0) return;
        const prev = history[history.length - 1];
        setFuture(f => [elements, ...f]);
        setHistory(h => h.slice(0, -1));
        setElements(prev);
    };

    const handleRedo = () => {
        if (future.length === 0) return;
        const next = future[0];
        setHistory(h => [...h, elements]);
        setFuture(f => f.slice(1));
        setElements(next);
    };

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
                    saveHistory();
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
                    saveHistory();
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
            if ((e.ctrlKey || e.metaKey) && e.key === 'z') {
                e.preventDefault();
                handleUndo();
            }
            if ((e.ctrlKey || e.metaKey) && (e.key === 'y' || (e.shiftKey && e.key === 'z'))) {
                e.preventDefault();
                handleRedo();
            }

            // Keyboard Nudging
            if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.key)) {
                if (selectedIds.length > 0) {
                    e.preventDefault();
                    saveHistory();
                    const step = e.shiftKey ? 10 : 1;
                    const dx = e.key === 'ArrowLeft' ? -step : (e.key === 'ArrowRight' ? step : 0);
                    const dy = e.key === 'ArrowUp' ? -step : (e.key === 'ArrowDown' ? step : 0);

                    setElements(prev => {
                        // Find any groups in selection
                        const selectedGroups = prev.filter(el => selectedIds.includes(el.id) && el.type === 'QGroupBox');
                        const groupIds = selectedGroups.map(g => g.id);

                        return prev.map(el => {
                            // Move if selected OR if it belongs to a selected group
                            if (selectedIds.includes(el.id) || (el.groupId && groupIds.includes(el.groupId))) {
                                return { ...el, x: el.x + dx, y: el.y + dy };
                            }
                            return el;
                        });
                    });
                }
            }
        };
        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [selectedIds, clipboard, elements, history, future]);

    const handleAddWidget = (type, x, y) => {
        saveHistory();
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

    // Logical Grouping
    const handleGroup = () => {
        if (selectedIds.length < 2) return;
        saveHistory();

        const selectedEls = elements.filter(el => selectedIds.includes(el.id));
        const minX = Math.min(...selectedEls.map(e => e.x));
        const minY = Math.min(...selectedEls.map(e => e.y));
        const maxX = Math.max(...selectedEls.map(e => e.x + e.w));
        const maxY = Math.max(...selectedEls.map(e => e.y + e.h));

        const padding = 10;
        const groupEl = {
            id: window.Designer.uid(),
            type: 'QGroupBox',
            name: 'groupBox_' + Date.now().toString().slice(-4),
            x: minX - padding,
            y: minY - padding - 10,
            w: (maxX - minX) + (padding * 2),
            h: (maxY - minY) + (padding * 2) + 10,
            text: 'Group',
            cat: 'Containers'
        };

        const newElements = elements.map(el => {
            if (selectedIds.includes(el.id)) {
                return { ...el, groupId: groupEl.id };
            }
            return el;
        });

        // Add group at the beginning so it's behind everything
        setElements([groupEl, ...newElements]);
        setSelectedIds([groupEl.id]);
    };

    const handleUngroup = () => {
        if (selectedIds.length === 0) return;
        saveHistory();

        const groupsToUngroup = elements.filter(el => selectedIds.includes(el.id) && el.type === 'QGroupBox');
        const groupIds = groupsToUngroup.map(g => g.id);

        // Also support "ungrouping" a child (detaching it)
        const childIds = elements.filter(el => selectedIds.includes(el.id) && el.groupId).map(el => el.id);

        if (groupIds.length === 0 && childIds.length === 0) return;

        // If removing groups, delete them. If just detaching children, remove their groupId.
        let newElements = elements;

        if (groupIds.length > 0) {
            newElements = newElements.filter(el => !groupIds.includes(el.id)).map(el => {
                if (el.groupId && groupIds.includes(el.groupId)) {
                    const { groupId, ...rest } = el;
                    return rest;
                }
                return el;
            });
        }

        if (childIds.length > 0) {
            newElements = newElements.map(el => {
                if (childIds.includes(el.id)) {
                    const { groupId, ...rest } = el;
                    return rest;
                }
                return el;
            });
        }

        setElements(newElements);
        // If we deleted groups, clear selection. If we detached children, keep selection.
        if (groupIds.length > 0) setSelectedIds([]);
    };

    const handlePropChange = (key, val) => {
        saveHistory();
        setElements(elements.map(el => selectedIds.includes(el.id) ? { ...el, [key]: val } : el));
    };

    const handleNameChange = (id, newName) => {
        saveHistory();
        setElements(elements.map(el => el.id === id ? { ...el, name: newName } : el));
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

        saveHistory();
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
        saveHistory();
        setElements(prev => prev.filter(el => !ids.includes(el.id)));
        setSelectedIds([]);
    };

    const handleMoveElement = (id, direction) => {
        saveHistory();
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

    const handleAlign = (mode) => {
        if (selectedIds.length < 2) return;
        saveHistory();

        const selectedEls = elements.filter(el => selectedIds.includes(el.id));
        let val;

        if (mode === 'left') val = Math.min(...selectedEls.map(e => e.x));
        else if (mode === 'right') val = Math.max(...selectedEls.map(e => e.x + e.w));
        else if (mode === 'top') val = Math.min(...selectedEls.map(e => e.y));
        else if (mode === 'bottom') val = Math.max(...selectedEls.map(e => e.y + e.h));
        else if (mode === 'center') {
            const minX = Math.min(...selectedEls.map(e => e.x));
            const maxX = Math.max(...selectedEls.map(e => e.x + e.w));
            val = minX + (maxX - minX) / 2;
        }
        else if (mode === 'middle') {
            const minY = Math.min(...selectedEls.map(e => e.y));
            const maxY = Math.max(...selectedEls.map(e => e.y + e.h));
            val = minY + (maxY - minY) / 2;
        }

        setElements(elements.map(el => {
            if (!selectedIds.includes(el.id)) return el;
            if (mode === 'left') return { ...el, x: val };
            if (mode === 'right') return { ...el, x: val - el.w };
            if (mode === 'top') return { ...el, y: val };
            if (mode === 'bottom') return { ...el, y: val - el.h };
            if (mode === 'center') return { ...el, x: val - el.w / 2 };
            if (mode === 'middle') return { ...el, y: val - el.h / 2 };
            return el;
        }));
    };

    const handleDistribute = (mode) => {
        if (selectedIds.length < 3) return;
        saveHistory();

        const selectedEls = elements.filter(el => selectedIds.includes(el.id));
        const newMap = new Map();

        if (mode === 'horizontal') {
            const sorted = [...selectedEls].sort((a, b) => a.x - b.x);
            const first = sorted[0];
            const last = sorted[sorted.length - 1];
            const totalSpan = (last.x + last.w) - first.x;
            const sumW = sorted.reduce((acc, el) => acc + el.w, 0);
            const gap = (totalSpan - sumW) / (sorted.length - 1);

            let curr = first.x;
            sorted.forEach(el => {
                newMap.set(el.id, curr);
                curr += el.w + gap;
            });

            setElements(elements.map(el => {
                if (newMap.has(el.id)) return { ...el, x: newMap.get(el.id) };
                return el;
            }));
        } else if (mode === 'vertical') {
            const sorted = [...selectedEls].sort((a, b) => a.y - b.y);
            const first = sorted[0];
            const last = sorted[sorted.length - 1];
            const totalSpan = (last.y + last.h) - first.y;
            const sumH = sorted.reduce((acc, el) => acc + el.h, 0);
            const gap = (totalSpan - sumH) / (sorted.length - 1);

            let curr = first.y;
            sorted.forEach(el => {
                newMap.set(el.id, curr);
                curr += el.h + gap;
            });

            setElements(elements.map(el => {
                if (newMap.has(el.id)) return { ...el, y: newMap.get(el.id) };
                return el;
            }));
        }
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
                        <Ico name="folder-open" />
                        <span className="text-[10px] font-bold">Import UI</span>
                    </button>
                    <button onClick={handleSaveUI} className="toolbar-btn flex gap-2" title="Save .ui">
                        <Ico name="save" />
                        <span className="text-[10px] font-bold">Save UI</span>
                    </button>
                    <button onClick={handleSavePy} className="toolbar-btn flex gap-2" title="Export .py">
                        <Ico name="file-code" />
                        <span className="text-[10px] font-bold">Export Python</span>
                    </button>
                    <div className="toolbar-sep" />
                    <button onClick={handleUndo} disabled={history.length === 0} className={`toolbar-btn flex gap-2 ${history.length === 0 ? 'opacity-50' : ''}`} title="Undo (Ctrl+Z)">
                        <Ico name="undo-2" />
                        <span className="text-[10px] font-bold">Undo</span>
                    </button>
                    <button onClick={handleRedo} disabled={future.length === 0} className={`toolbar-btn flex gap-2 ${future.length === 0 ? 'opacity-50' : ''}`} title="Redo (Ctrl+Y)">
                        <Ico name="redo-2" />
                        <span className="text-[10px] font-bold">Redo</span>
                    </button>
                    <div className="toolbar-sep" />
                    <button onClick={() => handleAlign('left')} disabled={selectedIds.length < 2} className={`toolbar-btn ${selectedIds.length < 2 ? 'opacity-50' : ''}`} title="Align Left">
                        <Ico name="align-left" />
                    </button>
                    <button onClick={() => handleAlign('center')} disabled={selectedIds.length < 2} className={`toolbar-btn ${selectedIds.length < 2 ? 'opacity-50' : ''}`} title="Align Horizontal Center">
                        <Ico name="align-center-horizontal" />
                    </button>
                    <button onClick={() => handleAlign('right')} disabled={selectedIds.length < 2} className={`toolbar-btn ${selectedIds.length < 2 ? 'opacity-50' : ''}`} title="Align Right">
                        <Ico name="align-right" />
                    </button>
                    <div className="toolbar-sep" />
                    <button onClick={() => handleAlign('top')} disabled={selectedIds.length < 2} className={`toolbar-btn ${selectedIds.length < 2 ? 'opacity-50' : ''}`} title="Align Top">
                        <Ico name="align-start-vertical" />
                    </button>
                    <button onClick={() => handleAlign('middle')} disabled={selectedIds.length < 2} className={`toolbar-btn ${selectedIds.length < 2 ? 'opacity-50' : ''}`} title="Align Vertical Center">
                        <Ico name="align-center-vertical" />
                    </button>
                    <button onClick={() => handleAlign('bottom')} disabled={selectedIds.length < 2} className={`toolbar-btn ${selectedIds.length < 2 ? 'opacity-50' : ''}`} title="Align Bottom">
                        <Ico name="align-end-vertical" />
                    </button>
                    <div className="toolbar-sep" />
                    <button onClick={() => handleDistribute('horizontal')} disabled={selectedIds.length < 3} className={`toolbar-btn ${selectedIds.length < 3 ? 'opacity-50' : ''}`} title="Distribute Horizontally">
                        <Ico name="align-horizontal-distribute-center" />
                    </button>
                    <button onClick={() => handleDistribute('vertical')} disabled={selectedIds.length < 3} className={`toolbar-btn ${selectedIds.length < 3 ? 'opacity-50' : ''}`} title="Distribute Vertically">
                        <Ico name="align-vertical-distribute-center" />
                    </button>
                    <div className="toolbar-sep" />
                    <button onClick={handleGroup} disabled={selectedIds.length < 2} className={`toolbar-btn ${selectedIds.length < 2 ? 'opacity-50' : ''}`} title="Group">
                        <Ico name="group" />
                    </button>
                    <button onClick={handleUngroup} disabled={selectedIds.length === 0} className={`toolbar-btn ${selectedIds.length === 0 ? 'opacity-50' : ''}`} title="Ungroup">
                        <Ico name="ungroup" />
                    </button>
                    <div className="toolbar-sep" />
                    <button onClick={() => setSnapEnabled(!snapEnabled)} className={`toolbar-btn flex gap-2 ${snapEnabled ? 'active' : ''}`}>
                        <Ico name="grid-3x3" />
                        <span className="text-[10px] font-bold">Snap</span>
                    </button>
                    <button onClick={() => setPreviewMode(!previewMode)} className={`toolbar-btn flex gap-2 ${previewMode ? 'active' : ''}`} style={{ color: previewMode ? 'var(--green)' : 'var(--text3)' }}>
                        <Ico name="play" />
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
                    hoverId={hoverId}
                    setHoverId={setHoverId}
                    onNameChange={handleNameChange}
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
                    onEditStart={saveHistory}
                    onMoveElement={handleMoveElement}
                    onDuplicate={handleDuplicate}
                    onDelete={handleDelete}
                    hoverId={hoverId}
                    setHoverId={setHoverId}
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

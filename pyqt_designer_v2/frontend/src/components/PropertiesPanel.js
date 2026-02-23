window.Designer = window.Designer || {};

window.Designer.PropertiesPanel = ({
    activeTab,
    onTabChange,
    element,
    onChange,
    canvasProps,
    onCanvasChange,
    themes,
    activeTheme,
    onThemeChange,
    connections,
    onAddConnection,
    onDeleteConnection,
    pyqtVersion,
    onPyqtVersionChange,
    exportTheme,
    onExportThemeChange
}) => {

    const FONT_FAMILIES = window.Designer.FONT_FAMILIES;

    const setProp = (k, v) => onChange(k, v);

    if (activeTab === 'signals') {
        return (
            <div className="w-72 shrink-0 flex flex-col border-l" style={{ background: 'var(--bg2)', borderColor: 'var(--border)' }}>
                <div className="flex border-b" style={{ borderColor: 'var(--border)' }}>
                    <button onClick={() => onTabChange('props')} className={`flex-1 py-2 text-[10px] font-bold uppercase tracking-wider border-b-2 transition-colors ${activeTab === 'props' ? 'border-[var(--accent)] text-[var(--accent)]' : 'border-transparent text-[var(--text3)] hover:text-[var(--text)]'}`}>Properties</button>
                    <button onClick={() => onTabChange('signals')} className={`flex-1 py-2 text-[10px] font-bold uppercase tracking-wider border-b-2 transition-colors ${activeTab === 'signals' ? 'border-[var(--accent)] text-[var(--accent)]' : 'border-transparent text-[var(--text3)] hover:text-[var(--text)]'}`}>Signals</button>
                </div>
                <div className="p-4 text-xs text-[var(--text3)]">
                    Signal/Slot editor placeholder.
                </div>
            </div>
        );
    }

    return (
        <div className="w-72 shrink-0 flex flex-col border-l overflow-hidden" style={{ background: 'var(--bg2)', borderColor: 'var(--border)' }}>
            <div className="flex border-b" style={{ borderColor: 'var(--border)' }}>
                <button onClick={() => onTabChange('props')} className={`flex-1 py-2 text-[10px] font-bold uppercase tracking-wider border-b-2 transition-colors ${activeTab === 'props' ? 'border-[var(--accent)] text-[var(--accent)]' : 'border-transparent text-[var(--text3)] hover:text-[var(--text)]'}`}>Properties</button>
                <button onClick={() => onTabChange('signals')} className={`flex-1 py-2 text-[10px] font-bold uppercase tracking-wider border-b-2 transition-colors ${activeTab === 'signals' ? 'border-[var(--accent)] text-[var(--accent)]' : 'border-transparent text-[var(--text3)] hover:text-[var(--text)]'}`}>Signals</button>
            </div>

            <div className="flex-1 overflow-y-auto scr">
                {element ? (
                    <>
                        {/* Identity */}
                        <div className="panel-section">
                            <span className="panel-label">Identity</span>
                            <div className="prop-row"><span className="text-[9px] font-bold min-w-[40px] text-[var(--text3)]">Name</span><input className="prop-input font-mono" value={element.name} onChange={e => setProp('name', e.target.value)} /></div>
                            <div className="prop-row"><span className="text-[9px] font-bold min-w-[40px] text-[var(--text3)]">Class</span><span className="text-[10px] font-mono text-[var(--text3)]">{element.type}</span></div>
                            <div className="prop-row mt-1">
                                <label className="flex items-center gap-2 cursor-pointer select-none">
                                    <input type="checkbox" checked={element.enabled !== false} onChange={e => setProp('enabled', e.target.checked)} />
                                    <span className="text-[9px] font-bold text-[var(--text3)]">Enabled</span>
                                </label>
                                <label className="flex items-center gap-2 cursor-pointer select-none ml-3">
                                    <input type="checkbox" checked={element.visible !== false} onChange={e => setProp('visible', e.target.checked)} />
                                    <span className="text-[9px] font-bold text-[var(--text3)]">Visible</span>
                                </label>
                            </div>
                            <div className="prop-row mt-1"><span className="text-[9px] font-bold min-w-[40px] text-[var(--text3)]">ToolTip</span><input className="prop-input" value={element.tooltip || ''} onChange={e => setProp('tooltip', e.target.value)} /></div>
                            <div className="prop-row"><span className="text-[9px] font-bold min-w-[40px] text-[var(--text3)]">Status</span><input className="prop-input" value={element.statusTip || ''} onChange={e => setProp('statusTip', e.target.value)} /></div>
                        </div>

                        {/* Geometry */}
                        <div className="panel-section">
                            <span className="panel-label">Geometry</span>
                            <div className="grid grid-cols-2 gap-2">
                                {[['X', 'x'], ['Y', 'y'], ['W', 'w'], ['H', 'h']].map(([l, k]) => (
                                    <div key={k} className="geo-box">
                                        <span className="geo-label">{l}</span>
                                        <input type="number" className="prop-input-sm" value={Math.round(element[k])} onChange={e => setProp(k, parseInt(e.target.value) || 0)} />
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Content & Input */}
                        <div className="panel-section">
                            <span className="panel-label">Content</span>
                            {['QPushButton', 'QLabel', 'QLineEdit', 'QCheckBox', 'QRadioButton', 'QCommandLinkButton', 'QGroupBox'].includes(element.type) && (
                                <div className="mb-2">
                                    <span className="text-[9px] font-bold mb-1 block text-[var(--text3)]">Text / Title</span>
                                    <textarea className="prop-input" rows={2} style={{ resize: 'none' }} value={element.text || ''} onChange={e => setProp('text', e.target.value)} />
                                </div>
                            )}
                            {['QLineEdit', 'QTextEdit', 'QPlainTextEdit'].includes(element.type) && (
                                <div className="mb-2">
                                    <span className="text-[9px] font-bold mb-1 block text-[var(--text3)]">Placeholder</span>
                                    <input className="prop-input" value={element.placeholderText || ''} onChange={e => setProp('placeholderText', e.target.value)} />
                                </div>
                            )}
                            {element.type === 'QCommandLinkButton' && (
                                <div className="mb-2">
                                    <span className="text-[9px] font-bold mb-1 block text-[var(--text3)]">Description</span>
                                    <input className="prop-input" value={element.description || ''} onChange={e => setProp('description', e.target.value)} />
                                </div>
                            )}

                            <div className="flex flex-wrap gap-3 mt-2">
                                {['QPushButton', 'QToolButton', 'QGroupBox', 'QCheckBox', 'QRadioButton'].includes(element.type) && (
                                    <label className="flex items-center gap-1 cursor-pointer">
                                        <input type="checkbox" checked={!!element.checkable} onChange={e => setProp('checkable', e.target.checked)} />
                                        <span className="text-[9px] text-[var(--text2)]">Checkable</span>
                                    </label>
                                )}
                                {['QPushButton', 'QToolButton', 'QCheckBox', 'QRadioButton', 'QGroupBox'].includes(element.type) && (
                                    <label className="flex items-center gap-1 cursor-pointer">
                                        <input type="checkbox" checked={!!element.checked} onChange={e => setProp('checked', e.target.checked)} />
                                        <span className="text-[9px] text-[var(--text2)]">Checked</span>
                                    </label>
                                )}
                                {['QLineEdit', 'QTextEdit', 'QPlainTextEdit', 'QSpinBox', 'QDoubleSpinBox'].includes(element.type) && (
                                    <label className="flex items-center gap-1 cursor-pointer">
                                        <input type="checkbox" checked={!!element.readOnly} onChange={e => setProp('readOnly', e.target.checked)} />
                                        <span className="text-[9px] text-[var(--text2)]">ReadOnly</span>
                                    </label>
                                )}
                                {['QPushButton', 'QGroupBox'].includes(element.type) && (
                                    <label className="flex items-center gap-1 cursor-pointer">
                                        <input type="checkbox" checked={!!element.flat} onChange={e => setProp('flat', e.target.checked)} />
                                        <span className="text-[9px] text-[var(--text2)]">Flat</span>
                                    </label>
                                )}
                            </div>
                        </div>

                        {/* Numeric Values */}
                        {['QSpinBox', 'QDoubleSpinBox', 'QSlider', 'QProgressBar', 'QLCDNumber'].includes(element.type) && (
                            <div className="panel-section">
                                <span className="panel-label">Values</span>
                                <div className="grid grid-cols-2 gap-2">
                                    <div className="geo-box"><span className="geo-label">Val</span><input type="number" className="prop-input-sm" value={element.value || 0} onChange={e => setProp('value', parseFloat(e.target.value))} /></div>
                                    {element.type !== 'QLCDNumber' && (
                                        <>
                                            <div className="geo-box"><span className="geo-label">Min</span><input type="number" className="prop-input-sm" value={element.minimum || 0} onChange={e => setProp('minimum', parseFloat(e.target.value))} /></div>
                                            <div className="geo-box"><span className="geo-label">Max</span><input type="number" className="prop-input-sm" value={element.maximum || (element.type === 'QProgressBar' || element.type === 'QSlider' ? 100 : 99)} onChange={e => setProp('maximum', parseFloat(e.target.value))} /></div>
                                        </>
                                    )}
                                </div>
                            </div>
                        )}

                        {/* Alignment */}
                        {['QLabel', 'QLineEdit', 'QImage', 'QProgressBar'].includes(element.type) && (
                            <div className="panel-section">
                                <span className="panel-label">Alignment</span>
                                <div className="flex gap-2">
                                    <div className="flex-1">
                                        <span className="text-[9px] font-bold mb-1 block text-[var(--text3)]">Horizontal</span>
                                        <select className="prop-select" value={element.hAlign || 'left'} onChange={e => setProp('hAlign', e.target.value)}>
                                            <option value="left">Left</option>
                                            <option value="center">Center</option>
                                            <option value="right">Right</option>
                                            <option value="justify">Justify</option>
                                        </select>
                                    </div>
                                    <div className="flex-1">
                                        <span className="text-[9px] font-bold mb-1 block text-[var(--text3)]">Vertical</span>
                                        <select className="prop-select" value={element.vAlign || 'center'} onChange={e => setProp('vAlign', e.target.value)}>
                                            <option value="top">Top</option>
                                            <option value="center">Center</option>
                                            <option value="bottom">Bottom</option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Typography */}
                        <div className="panel-section">
                            <span className="panel-label">Typography</span>
                            <select className="prop-select mb-2" value={element.fontFamily} onChange={e => setProp('fontFamily', e.target.value)}>
                                <option value="">Default Font</option>
                                {FONT_FAMILIES.map(f => <option key={f} value={f}>{f}</option>)}
                            </select>
                            <div className="flex gap-2 items-center">
                                <input type="number" className="prop-input-sm" placeholder="Size" value={element.fontSize || ''} onChange={e => setProp('fontSize', parseInt(e.target.value) || 0)} />
                                <button
                                    aria-label="Bold"
                                    aria-pressed={element.fontWeight === 'bold'}
                                    title="Bold"
                                    onClick={() => setProp('fontWeight', element.fontWeight === 'bold' ? 'normal' : 'bold')}
                                    className={`toggle-btn ${element.fontWeight === 'bold' ? 'active' : ''}`}
                                    style={{ fontWeight: 'bold' }}
                                >B</button>
                                <button
                                    aria-label="Italic"
                                    aria-pressed={!!element.fontItalic}
                                    title="Italic"
                                    onClick={() => setProp('fontItalic', !element.fontItalic)}
                                    className={`toggle-btn ${element.fontItalic ? 'active' : ''}`}
                                    style={{ fontStyle: 'italic' }}
                                >I</button>
                            </div>
                        </div>

                        {/* Colors & Style */}
                        <div className="panel-section">
                            <span className="panel-label">Style</span>
                            <div className="flex gap-3 mb-2">
                                <div><span className="text-[9px] font-bold mb-1 block text-[var(--text3)]">Text</span><div className="prop-color" style={{ backgroundColor: element.color || '#000' }}><input type="color" value={element.color || '#000000'} onChange={e => setProp('color', e.target.value)} /></div></div>
                                <div><span className="text-[9px] font-bold mb-1 block text-[var(--text3)]">Bg</span><div className="prop-color" style={{ backgroundColor: element.bg || '#fff' }}><input type="color" value={element.bg || '#ffffff'} onChange={e => setProp('bg', e.target.value)} /></div></div>
                            </div>
                            <span className="text-[9px] font-bold mb-1 block text-[var(--text3)]">StyleSheet</span>
                            <textarea className="prop-input font-mono text-[9px]" rows={4} placeholder="color: red; ..." value={element.styleSheet || ''} onChange={e => setProp('styleSheet', e.target.value)} />
                        </div>
                    </>
                ) : (
                    <div>
                        <div className="panel-section">
                            <span className="panel-label">Canvas Properties</span>
                            <span className="text-[9px] font-bold mb-1 block text-[var(--text3)]">Title</span>
                            <input className="prop-input mb-2" placeholder="Window Title" value={canvasProps.windowTitle} onChange={e => onCanvasChange('windowTitle', e.target.value)} />
                            <div className="grid grid-cols-2 gap-2 mb-2">
                                <div className="geo-box"><span className="geo-label">W</span><input type="number" className="prop-input-sm" value={canvasProps.canvasSize.w} onChange={e => onCanvasChange('canvasSize', { ...canvasProps.canvasSize, w: parseInt(e.target.value) || 800 })} /></div>
                                <div className="geo-box"><span className="geo-label">H</span><input type="number" className="prop-input-sm" value={canvasProps.canvasSize.h} onChange={e => onCanvasChange('canvasSize', { ...canvasProps.canvasSize, h: parseInt(e.target.value) || 600 })} /></div>
                            </div>
                        </div>

                        <div className="panel-section">
                            <span className="panel-label">Generation Settings</span>

                            <div className="mb-3">
                                <span className="text-[9px] font-bold mb-1 block text-[var(--text3)]">PyQt Version</span>
                                <div className="flex gap-2 bg-[var(--bg)] p-1 rounded border border-[var(--border)]">
                                    <button onClick={() => onPyqtVersionChange(5)} className={`flex-1 text-[10px] py-1 rounded transition-colors ${pyqtVersion === 5 ? 'bg-[var(--accent)] text-white' : 'text-[var(--text3)] hover:text-[var(--text)]'}`}>PyQt5</button>
                                    <button onClick={() => onPyqtVersionChange(6)} className={`flex-1 text-[10px] py-1 rounded transition-colors ${pyqtVersion === 6 ? 'bg-[var(--accent)] text-white' : 'text-[var(--text3)] hover:text-[var(--text)]'}`}>PyQt6</button>
                                </div>
                            </div>

                            <div className="mb-3">
                                <span className="text-[9px] font-bold mb-1 block text-[var(--text3)]">Theme Export</span>
                                <label className="flex items-center gap-2 cursor-pointer p-2 rounded hover:bg-[var(--bg)] border border-transparent hover:border-[var(--border)] transition-colors">
                                    <input type="checkbox" checked={exportTheme} onChange={e => onExportThemeChange(e.target.checked)} />
                                    <div className="flex flex-col">
                                        <span className="text-[10px] font-bold text-[var(--text2)]">Include Theme Colors</span>
                                        <span className="text-[9px] text-[var(--text3)]">Generate global stylesheet for high contrast</span>
                                    </div>
                                </label>
                            </div>
                        </div>

                        <div className="panel-section">
                            <span className="panel-label">Editor Theme</span>
                            <div className="grid grid-cols-2 gap-2">
                                {Object.entries(themes).map(([key, t]) => (
                                    <button key={key} onClick={() => onThemeChange(key)}
                                        className="flex items-center gap-2 px-3 py-2 rounded-md transition-all text-[10px] font-medium text-left"
                                        style={{
                                            background: activeTheme === key ? 'var(--accent-glow)' : 'var(--bg)',
                                            border: `1px solid ${activeTheme === key ? 'var(--accent)' : 'var(--border)'}`,
                                            color: activeTheme === key ? 'var(--accent)' : 'var(--text3)'
                                        }}>
                                        <span style={{ width: 12, height: 12, borderRadius: '50%', background: t.swatch, border: '1px solid var(--border2)', flexShrink: 0 }} />
                                        {t.name}
                                    </button>
                                ))}
                            </div>
                            <p className="mt-2 text-[9px] text-[var(--text3)] italic">
                                Use "Midnight" for best contrast.
                            </p>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

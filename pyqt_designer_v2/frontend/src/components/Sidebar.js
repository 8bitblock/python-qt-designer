window.Designer = window.Designer || {};

const { useMemo, useState, useRef, useEffect } = React;
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

window.Designer.Sidebar = ({ activeTab, onTabChange, widgetSearch, setWidgetSearch, elements, selectedIds, onSelect, hoverId, setHoverId, onNameChange }) => {
    const WIDGETS = window.Designer.WIDGETS;
    const CATEGORIES = window.Designer.CATEGORIES;
    const [editingId, setEditingId] = useState(null);
    const [editName, setEditName] = useState('');

    const filteredWidgets = useMemo(() => {
        if (!widgetSearch) return null;
        const q = widgetSearch.toLowerCase();
        return Object.entries(WIDGETS).filter(([k, v]) => k.toLowerCase().includes(q) || v.label.toLowerCase().includes(q));
    }, [widgetSearch]);

    const handleRenameStart = (e, el) => {
        e.stopPropagation(); // prevent select
        setEditingId(el.id);
        setEditName(el.name);
    };

    const handleRenameSubmit = () => {
        if (editingId && editName.trim()) {
            onNameChange(editingId, editName.trim());
        }
        setEditingId(null);
    };

    const renderTree = (list, depth = 0) => {
        // Reverse the list to show top-most elements first (like a Layers panel)
        return [...list].reverse().map(el => {
            const isHover = el.id === hoverId;
            const isEditing = el.id === editingId;

            return (
                <div key={el.id}
                    className={`tree-item ${selectedIds.includes(el.id) ? 'selected' : ''}`}
                    style={{
                        paddingLeft: depth * 12 + 8,
                        background: isHover ? 'var(--bg3)' : undefined
                    }}
                    onClick={(e) => onSelect(el.id, e.shiftKey)}
                    onDoubleClick={(e) => handleRenameStart(e, el)}
                    onMouseEnter={() => setHoverId(el.id)}
                    onMouseLeave={() => setHoverId(null)}
                >
                    <Ico name={WIDGETS[el.type]?.icon || 'box'} size={12} />
                    {isEditing ? (
                        <input
                            autoFocus
                            className="bg-[var(--bg)] text-[var(--text)] text-[10px] border border-[var(--accent)] rounded px-1 flex-1 min-w-0 outline-none"
                            value={editName}
                            onChange={e => setEditName(e.target.value)}
                            onBlur={handleRenameSubmit}
                            onKeyDown={e => e.key === 'Enter' && handleRenameSubmit()}
                            onClick={e => e.stopPropagation()}
                        />
                    ) : (
                        <span className="flex-1 truncate">{el.name}</span>
                    )}
                    <span className="type-badge">{el.type}</span>
                </div>
            );
        });
    };

    return (
        <div className="w-64 shrink-0 flex flex-col border-r overflow-hidden" style={{ background: 'var(--bg2)', borderColor: 'var(--border)' }}>
            <div className="flex border-b" style={{ borderColor: 'var(--border)' }}>
                <button onClick={() => onTabChange('widgets')} className={`flex-1 py-2 text-[10px] font-bold uppercase tracking-wider border-b-2 transition-colors ${activeTab === 'widgets' ? 'border-[var(--accent)] text-[var(--accent)]' : 'border-transparent text-[var(--text3)] hover:text-[var(--text)]'}`}>Widgets</button>
                <button onClick={() => onTabChange('tree')} className={`flex-1 py-2 text-[10px] font-bold uppercase tracking-wider border-b-2 transition-colors ${activeTab === 'tree' ? 'border-[var(--accent)] text-[var(--accent)]' : 'border-transparent text-[var(--text3)] hover:text-[var(--text)]'}`}>Objects</button>
            </div>

            {activeTab === 'widgets' ? (
                <div className="flex-1 overflow-y-auto scr">
                    <div className="p-3">
                        <div className="relative mb-3">
                            <span className="absolute left-2 top-1/2 -translate-y-1/2" style={{ color: 'var(--text3)' }}><Ico name="search" size={12} /></span>
                            <input className="search-input" placeholder="Search widgets..." value={widgetSearch} onChange={e => setWidgetSearch(e.target.value)} />
                        </div>
                    </div>

                    {filteredWidgets ? (
                        <div className="px-3 pb-3 grid grid-cols-3 gap-2">
                            {filteredWidgets.map(([type, cfg]) => (
                                <div key={type} draggable onDragStart={e => e.dataTransfer.setData("widgetType", type)} className="widget-card">
                                    <div className="icon-wrap"><Ico name={cfg.icon} size={18} /></div>
                                    <span>{cfg.label}</span>
                                </div>
                            ))}
                        </div>
                    ) : (
                        Object.entries(CATEGORIES).map(([catName, cat]) => (
                            <div key={catName} className="mb-1">
                                <div className="flex items-center gap-2 px-4 py-2" style={{ color: 'var(--text3)' }}>
                                    <Ico name={cat.icon} size={12} />
                                    <span className="text-[10px] font-bold uppercase tracking-wider">{catName}</span>
                                </div>
                                <div className="px-3 pb-2 grid grid-cols-3 gap-1.5">
                                    {cat.items.map(type => {
                                        const cfg = WIDGETS[type]; if (!cfg) return null;
                                        return (
                                            <div key={type} draggable onDragStart={e => e.dataTransfer.setData("widgetType", type)} className="widget-card">
                                                <div className="icon-wrap"><Ico name={cfg.icon} size={16} /></div>
                                                <span>{cfg.label}</span>
                                            </div>
                                        );
                                    })}
                                </div>
                            </div>
                        ))
                    )}
                </div>
            ) : (
                <div className="flex-1 overflow-y-auto scr py-2">
                    {elements.length === 0 ? <div className="text-center py-8 text-[var(--text3)] text-xs">No widgets</div> : renderTree(elements)}
                </div>
            )}
        </div>
    );
};

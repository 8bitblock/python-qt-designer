window.Designer = window.Designer || {};

const { useState, useRef, useEffect, useCallback } = React;
const WidgetRenderer = window.Designer.WidgetRenderer;

window.Designer.Canvas = ({
    elements,
    selectedIds,
    canvasSize,
    canvasBg,
    zoom,
    theme,
    previewMode,
    snapEnabled,
    gridSize,
    onAddWidget,
    onSelect,
    onUpdate,
    onContextMenu
}) => {
    const canvasRef = useRef(null);
    const dragRef = useRef({ mode: null, startX: 0, startY: 0, initEls: [] });
    const [rubberBand, setRubberBand] = useState(null);

    const handleDrop = (e) => {
        e.preventDefault();
        const type = e.dataTransfer.getData("widgetType");
        if (!type) return;
        const rect = canvasRef.current.getBoundingClientRect();
        const x = (e.clientX - rect.left) / zoom;
        const y = (e.clientY - rect.top) / zoom;
        onAddWidget(type, x, y);
    };

    const startMove = (e, id) => {
        if (previewMode) return;
        e.stopPropagation();
        onSelect(id, e.shiftKey);

        dragRef.current = {
            mode: 'move',
            startX: e.clientX,
            startY: e.clientY,
            initEls: JSON.parse(JSON.stringify(elements)),
            selectedIds: e.shiftKey || selectedIds.includes(id) ? (selectedIds.includes(id) ? selectedIds : [...selectedIds, id]) : [id]
        };
    };

    const startResize = (e, id, handle) => {
        e.stopPropagation();
        e.preventDefault();
        onSelect(id, false);
        dragRef.current = {
            mode: 'resize',
            handle,
            startX: e.clientX,
            startY: e.clientY,
            initEls: JSON.parse(JSON.stringify(elements)),
            selectedIds: [id]
        };
    };

    const handleMouseDown = (e) => {
        if (e.target !== canvasRef.current) return;
        const rect = canvasRef.current.getBoundingClientRect();
        const x = (e.clientX - rect.left) / zoom;
        const y = (e.clientY - rect.top) / zoom;

        if (!e.shiftKey) onSelect(null);

        dragRef.current = {
            mode: 'rubber',
            startX: e.clientX,
            startY: e.clientY,
            rubberStart: { x, y }
        };
        setRubberBand({ x, y, w: 0, h: 0 });
    };

    const handleMouseMove = useCallback((e) => {
        const d = dragRef.current;
        if (!d.mode) return;

        const dx = (e.clientX - d.startX) / zoom;
        const dy = (e.clientY - d.startY) / zoom;

        if (d.mode === 'move') {
            const nextEls = d.initEls.map(el => {
                if (!d.selectedIds.includes(el.id) || el.locked) return el;
                let nx = el.x + dx;
                let ny = el.y + dy;
                if (snapEnabled) {
                    nx = Math.round(nx / gridSize) * gridSize;
                    ny = Math.round(ny / gridSize) * gridSize;
                }
                return { ...el, x: nx, y: ny };
            });
            onUpdate(nextEls, false);
        }
        else if (d.mode === 'resize') {
            const nextEls = d.initEls.map(el => {
                if (!d.selectedIds.includes(el.id)) return el;
                let { x, y, w, h } = el;
                const hdl = d.handle;
                if (hdl.includes('e')) w = Math.max(10, el.w + dx);
                if (hdl.includes('s')) h = Math.max(10, el.h + dy);

                if (snapEnabled) {
                    w = Math.round(w / gridSize) * gridSize;
                    h = Math.round(h / gridSize) * gridSize;
                }
                return { ...el, x, y, w, h };
            });
            onUpdate(nextEls, false);
        }
        else if (d.mode === 'rubber') {
            const rect = canvasRef.current.getBoundingClientRect();
            const cx = (e.clientX - rect.left) / zoom;
            const cy = (e.clientY - rect.top) / zoom;
            const rx = Math.min(d.rubberStart.x, cx);
            const ry = Math.min(d.rubberStart.y, cy);
            const rw = Math.abs(cx - d.rubberStart.x);
            const rh = Math.abs(cy - d.rubberStart.y);
            setRubberBand({ x: rx, y: ry, w: rw, h: rh });

            const ids = elements.filter(el =>
                el.x < rx + rw && el.x + el.w > rx &&
                el.y < ry + rh && el.y + el.h > ry
            ).map(e => e.id);
            onSelect(ids, false, true);
        }
    }, [zoom, snapEnabled, gridSize, elements, onUpdate, onSelect]);

    const handleMouseUp = () => {
        if (dragRef.current.mode === 'move' || dragRef.current.mode === 'resize') {
            onUpdate(elements, true);
        }
        dragRef.current = { mode: null };
        setRubberBand(null);
    };

    return (
        <div className="flex-1 overflow-auto scr grid-bg min-w-0" onMouseMove={handleMouseMove} onMouseUp={handleMouseUp}>
            <div style={{ padding: 40, display: 'inline-block', minWidth: '100%', minHeight: '100%' }}>
                <div ref={canvasRef}
                    className="relative shadow-2xl transition-colors"
                    style={{
                        width: canvasSize.w,
                        height: canvasSize.h,
                        backgroundColor: canvasBg,
                        transform: `scale(${zoom})`,
                        transformOrigin: 'top left',
                        border: '1px solid var(--border2)'
                    }}
                    onDrop={handleDrop}
                    onDragOver={e => e.preventDefault()}
                    onMouseDown={handleMouseDown}
                    onContextMenu={e => { e.preventDefault(); if(e.target === canvasRef.current) onSelect(null); }}
                >
                    {elements.map(el => {
                        const isSel = selectedIds.includes(el.id);
                        return (
                            <div key={el.id}
                                className="absolute"
                                style={{
                                    left: el.x, top: el.y, width: el.w, height: el.h,
                                    outline: (!previewMode && isSel) ? `2px solid ${theme.ide.accent}` : 'none',
                                    cursor: previewMode ? 'default' : 'move'
                                }}
                                onMouseDown={e => startMove(e, el.id)}
                                onContextMenu={e => onContextMenu(e, el.id)}
                            >
                                <WidgetRenderer el={el} theme={theme} />

                                {!previewMode && isSel && !el.locked && (
                                    <>
                                        {['n','s','e','w','ne','nw','se','sw'].map(h => (
                                            <div key={h}
                                                className={`resize-handle rh-${h}`}
                                                onMouseDown={e => startResize(e, el.id, h)}
                                            />
                                        ))}
                                    </>
                                )}
                            </div>
                        );
                    })}

                    {rubberBand && (
                        <div className="rubber-band"
                            style={{ left: rubberBand.x, top: rubberBand.y, width: rubberBand.w, height: rubberBand.h }}
                        />
                    )}
                </div>
            </div>
        </div>
    );
};

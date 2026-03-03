window.Designer = window.Designer || {};

const { useRef, useEffect } = React;

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

window.Designer.WidgetRenderer = ({ el, theme }) => {
    const tw = theme.widget;
    const defaultBg = tw.defaultBg || 'transparent';
    const baseColor = el.color || theme.ide.text;

    const s = {
        fontFamily: el.fontFamily || 'Segoe UI',
        fontWeight: el.fontWeight || 'normal',
        fontStyle: el.fontItalic ? 'italic' : 'normal',
        fontSize: el.fontSize ? `${el.fontSize}pt` : undefined,
        color: baseColor,
        backgroundColor: el.bg || undefined,
    };

    const isCmd = el.type === 'QCommandLinkButton';

    switch (el.type) {
        case 'QPushButton':
        case 'QCommandLinkButton':
            return (
                <div className="w-full h-full flex items-center px-2 shadow-sm transition-all widget-btn"
                    style={{
                        ...s,
                        background: el.bg || tw.defaultBg || tw.btnBg,
                        border: `1px solid ${tw.btnBorder}`,
                        borderRadius: 4,
                        color: el.color || tw.btnColor,
                        fontSize: el.fontSize ? `${el.fontSize}pt` : '11px',
                        justifyContent: isCmd ? 'flex-start' : 'center',
                        textAlign: isCmd ? 'left' : 'center',
                        gap: isCmd ? 8 : 4
                    }}>
                    {isCmd && <Ico name="arrow-right-circle" size={16} />}
                    <div className="flex flex-col">
                        <span>{el.text || (isCmd ? 'CommandLinkButton' : 'Button')}</span>
                        {isCmd && <span style={{ fontSize: '0.85em', opacity: 0.75, fontWeight: 'normal' }}>{el.description || 'Description...'}</span>}
                    </div>
                </div>
            );
        case 'QToolButton':
            return (
                <div className="w-full h-full flex items-center justify-center shadow-sm widget-btn"
                    style={{
                        ...s,
                        background: el.bg || tw.defaultBg || tw.btnBg,
                        border: `1px solid ${tw.btnBorder}`,
                        borderRadius: 4,
                        color: el.color || tw.btnColor,
                        fontSize: el.fontSize ? `${el.fontSize}pt` : '11px'
                    }}>
                    {el.text || '...'}
                </div>
            );
        case 'QLabel':
            if (el.pixmap) {
                if (el.pixmap.startsWith('http')) return <img src={el.pixmap} className="w-full h-full object-contain" alt="" />;
                return <div className="w-full h-full flex items-center justify-center text-[9px]" style={{ background: tw.inputBg, color: tw.labelColor }}><Ico name="image" size={20} /></div>;
            }
            return (
                <div className="w-full h-full flex items-center justify-center"
                    style={{
                        ...s,
                        background: el.bg || tw.defaultBg || 'transparent',
                        fontSize: el.fontSize ? `${el.fontSize}pt` : '11px',
                        borderRadius: 2
                    }}>
                    {el.text || 'Label'}
                </div>
            );
        case 'QLineEdit':
            return (
                <div className="w-full h-full flex items-center px-2 shadow-sm"
                    style={{
                        ...s,
                        background: el.bg || tw.defaultBg || tw.inputBg,
                        border: `1px solid ${tw.inputBorder}`,
                        borderRadius: 3,
                        color: el.color || tw.inputColor,
                        fontSize: el.fontSize ? `${el.fontSize}pt` : '11px'
                    }}>
                    {el.text || <span style={{ color: tw.checkColor, opacity: 0.4 }}>{el.placeholderText || ''}</span>}
                </div>
            );
        case 'QCheckBox':
            return (
                <div className="w-full h-full flex items-center gap-1.5"
                    style={{
                        ...s,
                        background: el.bg || tw.defaultBg || 'transparent',
                        color: el.color || tw.checkColor,
                        fontSize: el.fontSize ? `${el.fontSize}pt` : '11px',
                        borderRadius: 2,
                        padding: '0 2px'
                    }}>
                    <div className="w-3.5 h-3.5 flex items-center justify-center border rounded-sm" style={{ borderColor: tw.inputBorder, background: tw.inputBg }}>
                        {el.checked && <div className="w-2 h-2 rounded-[1px]" style={{ background: theme.ide.accent }} />}
                    </div>
                    {el.text || 'CheckBox'}
                </div>
            );
        case 'QGroupBox':
            return (
                <div className="w-full h-full relative" style={{ border: `1px solid ${tw.groupBorder}`, borderRadius: 4, paddingTop: 18 }}>
                    <span className="absolute left-2" style={{ top: -9, background: theme.canvas, padding: '0 4px', fontSize: 11, color: el.color || tw.groupColor, fontWeight: 600 }}>{el.text || 'Group'}</span>
                </div>
            );
        default:
            return (
                <div className="w-full h-full flex items-center justify-center text-[9px]"
                    style={{
                        ...s,
                        background: el.bg || tw.defaultBg || 'transparent',
                        color: el.color || tw.labelColor || theme.ide.text
                    }}>
                    {el.type}
                </div>
            );
    }
};

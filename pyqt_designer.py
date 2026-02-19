import sys
import os
import threading
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer

try:
    from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    from PyQt6.QtWebChannel import QWebChannel
    from PyQt6.QtCore import QUrl, QObject, pyqtSlot, pyqtSignal
    PYQT_VERSION = 6
except ImportError:
    from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    from PyQt5.QtWebChannel import QWebChannel
    from PyQt5.QtCore import QUrl, QObject, pyqtSlot, pyqtSignal
    PYQT_VERSION = 5


class DesignerBridge(QObject):
    ui_imported = pyqtSignal(str)
    python_generated = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtSlot(str)
    def save_ui_file(self, xml_content):
        if PYQT_VERSION == 6:
            file_path, _ = QFileDialog.getSaveFileName(
                None, "Save PyQt UI File", "design.ui", "UI Files (*.ui);;All Files (*)"
            )
        else:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(
                None, "Save PyQt UI File", "design.ui", "UI Files (*.ui);;All Files (*)", options=options
            )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(xml_content)
                print(f"Saved: {file_path}")
            except Exception as e:
                print(f"Error saving: {e}")

    @pyqtSlot(str)
    def save_python_file(self, python_content):
        if PYQT_VERSION == 6:
            file_path, _ = QFileDialog.getSaveFileName(
                None, "Save Python File", "ui_main.py", "Python Files (*.py);;All Files (*)"
            )
        else:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(
                None, "Save Python File", "ui_main.py", "Python Files (*.py);;All Files (*)", options=options
            )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(python_content)
                print(f"Saved: {file_path}")
            except Exception as e:
                print(f"Error saving: {e}")

    @pyqtSlot()
    def import_ui_file(self):
        if PYQT_VERSION == 6:
            file_path, _ = QFileDialog.getOpenFileName(
                None, "Open PyQt UI File", "", "UI Files (*.ui);;All Files (*)"
            )
        else:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getOpenFileName(
                None, "Open PyQt UI File", "", "UI Files (*.ui);;All Files (*)", options=options
            )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.ui_imported.emit(content)
            except Exception as e:
                print(f"Error loading: {e}")


HTML_CONTENT = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>PyQt6 Designer Pro</title>
<script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://unpkg.com/lucide@latest"></script>
<script src="qrc:///qtwebchannel/qwebchannel.js"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');
*{box-sizing:border-box}
body{margin:0;padding:0;overflow:hidden;font-family:'DM Sans',system-ui,sans-serif;background:var(--bg);color:var(--text)}
#root{height:100vh;width:100vw;background:var(--bg)}
:root{--bg:#09090b;--bg2:#18181b;--bg3:#27272a;--bg4:#3f3f46;--border:#27272a;--border2:#3f3f46;--text:#fafafa;--text2:#a1a1aa;--text3:#71717a;--accent:#3b82f6;--accent2:#2563eb;--accent-glow:rgba(59,130,246,0.15);--red:#ef4444;--green:#22c55e;--yellow:#eab308;--purple:#a855f7}
.grid-bg{background-color:var(--bg);background-image:radial-gradient(circle,var(--border) 1px,transparent 1px);background-size:20px 20px;min-height:100%;min-width:100%}
.scr::-webkit-scrollbar{width:5px;height:5px}
.scr::-webkit-scrollbar-track{background:transparent}
.scr::-webkit-scrollbar-thumb{background:var(--bg4);border-radius:3px}
.scr::-webkit-scrollbar-thumb:hover{background:#52525b}
input:focus,textarea:focus,select:focus{outline:none;box-shadow:0 0 0 1px var(--accent)}
.ctx-menu{position:fixed;background:var(--bg2);border:1px solid var(--border2);border-radius:8px;padding:4px;z-index:9999;box-shadow:0 20px 40px rgba(0,0,0,0.6);min-width:180px;backdrop-filter:blur(12px)}
.ctx-item{display:flex;align-items:center;gap:8px;width:100%;text-align:left;padding:6px 10px;font-size:11px;border-radius:4px;color:var(--text2);border:none;background:none;cursor:pointer;transition:all 0.1s}
.ctx-item:hover{background:var(--accent);color:white}
.ctx-item.danger:hover{background:var(--red)}
.ctx-sep{height:1px;background:var(--border);margin:3px 4px}

/* Widget preview styles */
.wp-btn{background:linear-gradient(180deg,#f0f0f0,#e0e0e0);border:1px solid #b0b0b0;border-radius:4px;color:#1a1a1a;display:flex;align-items:center;justify-content:center;font-size:11px;font-family:Segoe UI,sans-serif}
.wp-input{background:#fff;border:1px solid #b0b0b0;border-radius:3px;color:#1a1a1a;padding:2px 4px;font-size:11px;font-family:Segoe UI,sans-serif;display:flex;align-items:center}
.wp-combo{background:#fff;border:1px solid #b0b0b0;border-radius:3px;color:#1a1a1a;padding:2px 4px;font-size:11px;display:flex;align-items:center;justify-content:space-between}
.wp-check{display:flex;align-items:center;gap:4px;font-size:11px;font-family:Segoe UI,sans-serif}
.wp-group{border:1px solid #999;border-radius:4px;position:relative;padding-top:16px}
.wp-group-title{position:absolute;top:-8px;left:8px;background:inherit;padding:0 4px;font-size:11px}
.wp-progress{background:#e0e0e0;border:1px solid #b0b0b0;border-radius:3px;overflow:hidden;position:relative}
.wp-progress-fill{height:100%;background:linear-gradient(90deg,#06b6d4,#3b82f6);width:45%;transition:width 0.3s}
.wp-slider{display:flex;align-items:center;position:relative}
.wp-slider-track{width:100%;height:4px;background:#d0d0d0;border-radius:2px}
.wp-slider-thumb{position:absolute;left:45%;width:12px;height:12px;background:#fff;border:2px solid #3b82f6;border-radius:50%;transform:translate(-50%,-50%);top:50%}
.wp-spin{background:#fff;border:1px solid #b0b0b0;border-radius:3px;display:flex;align-items:center}
.wp-lcd{background:#1a1a2e;color:#00ff88;font-family:'Courier New',monospace;display:flex;align-items:center;justify-content:center;border:2px inset #333;letter-spacing:2px}
.wp-dial{border-radius:50%;background:conic-gradient(from 220deg,#3b82f6 0%,#3b82f6 45%,#e0e0e0 45%,#e0e0e0 100%);border:2px solid #999;position:relative}
.wp-dial::after{content:'';position:absolute;top:50%;left:50%;width:40%;height:40%;background:radial-gradient(circle,#f0f0f0,#ccc);border-radius:50%;transform:translate(-50%,-50%)}
.wp-list{background:#fff;border:1px solid #b0b0b0;font-size:10px;color:#1a1a1a;overflow:hidden}
.wp-list-item{padding:2px 6px;border-bottom:1px solid #eee}
.wp-list-item:first-child{background:#3b82f6;color:white}
.wp-tree{background:#fff;border:1px solid #b0b0b0;font-size:10px;color:#1a1a1a;overflow:hidden;padding:2px}
.wp-cal{background:#fff;border:1px solid #b0b0b0;font-size:8px;color:#1a1a1a;display:flex;flex-direction:column}
.wp-cal-header{background:#f0f0f0;text-align:center;padding:2px;font-weight:bold;border-bottom:1px solid #ddd;font-size:10px}
.wp-cal-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:1px;padding:2px;flex:1}
.wp-cal-cell{text-align:center;padding:1px;font-size:7px}
.wp-tab{display:flex;flex-direction:column}
.wp-tab-bar{display:flex;background:#e8e8e8;border-bottom:1px solid #b0b0b0}
.wp-tab-item{padding:3px 10px;font-size:10px;border-right:1px solid #ccc;cursor:default}
.wp-tab-item.active{background:#fff;border-bottom:1px solid #fff;margin-bottom:-1px}
.wp-tab-body{flex:1;background:#fff;border:1px solid #b0b0b0;border-top:none}
.wp-frame{border:1px solid #b0b0b0;background:rgba(255,255,255,0.05)}
.wp-table{background:#fff;border:1px solid #b0b0b0;font-size:9px;color:#1a1a1a;display:flex;flex-direction:column}
.wp-table-header{display:flex;background:#f0f0f0;border-bottom:1px solid #ccc}
.wp-table-cell{flex:1;padding:2px 4px;border-right:1px solid #ddd}
.wp-table-row{display:flex;border-bottom:1px solid #eee}
.wp-date{background:#fff;border:1px solid #b0b0b0;border-radius:3px;display:flex;align-items:center;justify-content:space-between;padding:2px 6px;font-size:10px;color:#1a1a1a}
.wp-scroll{border:1px solid #b0b0b0;overflow:hidden;position:relative;background:#fff}

.resize-handle{position:absolute;z-index:200}
.rh-n{top:-3px;left:6px;right:6px;height:6px;cursor:n-resize}
.rh-s{bottom:-3px;left:6px;right:6px;height:6px;cursor:s-resize}
.rh-w{left:-3px;top:6px;bottom:6px;width:6px;cursor:w-resize}
.rh-e{right:-3px;top:6px;bottom:6px;width:6px;cursor:e-resize}
.rh-nw{top:-4px;left:-4px;width:8px;height:8px;cursor:nw-resize;border-radius:2px;background:var(--accent);border:1px solid white}
.rh-ne{top:-4px;right:-4px;width:8px;height:8px;cursor:ne-resize;border-radius:2px;background:var(--accent);border:1px solid white}
.rh-sw{bottom:-4px;left:-4px;width:8px;height:8px;cursor:sw-resize;border-radius:2px;background:var(--accent);border:1px solid white}
.rh-se{bottom:-4px;right:-4px;width:8px;height:8px;cursor:se-resize;border-radius:2px;background:var(--accent);border:1px solid white}

.rubber-band{position:absolute;border:1px dashed var(--accent);background:rgba(59,130,246,0.08);pointer-events:none;z-index:999}
.guide-line{position:absolute;pointer-events:none;z-index:998}
.guide-h{left:0;right:0;height:1px;background:var(--red);opacity:0.5}
.guide-v{top:0;bottom:0;width:1px;background:var(--red);opacity:0.5}
.drop-highlight{box-shadow:inset 0 0 0 2px var(--accent);border-radius:4px}

.panel-section{padding:12px 16px;border-bottom:1px solid var(--border)}
.panel-label{font-size:10px;font-weight:600;color:var(--text3);text-transform:uppercase;letter-spacing:0.05em;margin-bottom:8px;display:block}
.prop-row{display:flex;align-items:center;gap:6px;margin-bottom:6px}
.prop-input{width:100%;background:var(--bg);border:1px solid var(--border);border-radius:4px;padding:5px 8px;font-size:11px;color:var(--text);font-family:'DM Sans',sans-serif}
.prop-input:focus{border-color:var(--accent)}
.prop-input-sm{width:56px;background:var(--bg);border:1px solid var(--border);border-radius:4px;padding:4px 6px;font-size:11px;color:var(--text);text-align:right;font-family:'JetBrains Mono',monospace}
.prop-select{width:100%;background:var(--bg);border:1px solid var(--border);border-radius:4px;padding:5px 8px;font-size:11px;color:var(--text);font-family:'DM Sans',sans-serif}
.prop-check{display:flex;align-items:center;gap:6px;font-size:11px;color:var(--text2);cursor:pointer}
.prop-color{width:24px;height:24px;border-radius:4px;border:1px solid var(--border);cursor:pointer;padding:0;overflow:hidden}
.prop-color input{opacity:0;width:100%;height:100%;cursor:pointer}
.geo-box{background:var(--bg);border:1px solid var(--border);border-radius:6px;padding:6px 8px;display:flex;align-items:center;justify-content:space-between}
.geo-label{font-size:9px;font-weight:700;color:var(--text3);min-width:14px}
.toggle-btn{padding:4px 8px;border-radius:4px;font-size:10px;font-weight:600;border:1px solid var(--border);cursor:pointer;transition:all 0.15s}
.toggle-btn.active{background:var(--accent);border-color:var(--accent);color:white}
.toggle-btn:not(.active){background:var(--bg);color:var(--text3)}
.align-btn{flex:1;padding:5px;border-radius:4px;display:flex;align-items:center;justify-content:center;cursor:pointer;border:none;background:none;color:var(--text3);transition:all 0.1s}
.align-btn:hover{background:var(--bg3);color:var(--text)}
.align-btn.active{background:var(--bg3);color:var(--accent)}

.tree-item{display:flex;align-items:center;gap:6px;padding:3px 8px;font-size:11px;cursor:pointer;border-radius:4px;color:var(--text2);transition:all 0.1s}
.tree-item:hover{background:var(--bg3);color:var(--text)}
.tree-item.selected{background:var(--accent-glow);color:var(--accent)}
.tree-item .type-badge{font-size:9px;padding:1px 4px;background:var(--bg3);border-radius:3px;color:var(--text3);font-family:'JetBrains Mono',monospace}

.tab-btn{padding:6px 14px;font-size:11px;font-weight:600;border:none;cursor:pointer;transition:all 0.15s;border-radius:6px}
.tab-btn.active{background:var(--accent);color:white;box-shadow:0 2px 8px rgba(59,130,246,0.3)}
.tab-btn:not(.active){background:transparent;color:var(--text3)}
.tab-btn:not(.active):hover{color:var(--text);background:var(--bg3)}

.toolbar-btn{padding:5px;border-radius:6px;border:none;cursor:pointer;color:var(--text3);background:none;display:flex;align-items:center;justify-content:center;transition:all 0.1s}
.toolbar-btn:hover{background:var(--bg3);color:var(--text)}
.toolbar-btn.active{background:var(--accent-glow);color:var(--accent)}
.toolbar-sep{width:1px;height:20px;background:var(--border);margin:0 4px}

.code-view{font-family:'JetBrains Mono',monospace;font-size:11px;line-height:1.6;color:#93c5fd;white-space:pre;tab-size:4}
.code-view .kw{color:#c084fc}
.code-view .str{color:#86efac}
.code-view .cm{color:#71717a}
.code-view .fn{color:#fbbf24}
.code-view .num{color:#f87171}

.widget-card{background:var(--bg2);border:1px solid var(--border);border-radius:8px;padding:8px;display:flex;flex-direction:column;align-items:center;gap:4px;cursor:grab;transition:all 0.15s;user-select:none}
.widget-card:hover{border-color:var(--accent);background:var(--bg3);transform:translateY(-1px);box-shadow:0 4px 12px rgba(0,0,0,0.3)}
.widget-card:active{transform:scale(0.96)}
.widget-card .icon-wrap{color:var(--text3);transition:color 0.15s}
.widget-card:hover .icon-wrap{color:var(--accent)}
.widget-card span{font-size:9px;font-weight:500;color:var(--text3);text-align:center;line-height:1.2}
.widget-card:hover span{color:var(--text)}

.search-input{width:100%;background:var(--bg);border:1px solid var(--border);border-radius:6px;padding:6px 10px 6px 30px;font-size:11px;color:var(--text);font-family:'DM Sans',sans-serif}
</style>
</head>
<body>
<div id="root"></div>
<script type="text/babel">
const{useState,useRef,useEffect,useCallback,useMemo}=React;

/* ───── Constants ───── */
const FONT_FAMILIES=['Segoe UI','Arial','Helvetica Neue','Times New Roman','Courier New','Verdana','Georgia','Trebuchet MS','Tahoma','Palatino','Lucida Console','Consolas','Roboto','Open Sans','monospace','sans-serif','serif'];

const THEMES={
    midnight:{
        name:'Midnight',
        swatch:'#09090b',
        ide:{bg:'#09090b',bg2:'#18181b',bg3:'#27272a',bg4:'#3f3f46',border:'#27272a',border2:'#3f3f46',text:'#fafafa',text2:'#a1a1aa',text3:'#71717a',accent:'#3b82f6',accent2:'#2563eb','accent-glow':'rgba(59,130,246,0.15)',red:'#ef4444',green:'#22c55e',yellow:'#eab308',purple:'#a855f7'},
        canvas:'#1e1e2e',
        widget:{btnBg:'linear-gradient(180deg,#484860,#3a3a50)',btnBorder:'#6a6a80',btnColor:'#e8e8f0',inputBg:'#2e2e42',inputBorder:'#5a5a70',inputColor:'#e0e0ea',comboBg:'#2e2e42',comboBorder:'#5a5a70',comboColor:'#e0e0ea',checkColor:'#e0e0ea',groupBorder:'#5a5a70',groupColor:'#e0e0ea',frameBorder:'#5a5a70',progressBg:'#2a2a3e',progressBorder:'#5a5a70',progressFill:'linear-gradient(90deg,#06b6d4,#3b82f6)',sliderTrack:'#3a3a50',sliderThumb:'#3b82f6',sliderThumbBorder:'#fff',spinBg:'#2e2e42',spinBorder:'#5a5a70',spinColor:'#e0e0ea',lcdBg:'#0a0a1e',lcdColor:'#00ff88',listBg:'#2a2a3e',listBorder:'#5a5a70',listColor:'#e0e0ea',listSelBg:'#3b82f6',listSelColor:'#fff',listItemBorder:'#3a3a50',treeBg:'#2a2a3e',treeBorder:'#5a5a70',treeColor:'#e0e0ea',tableBg:'#2a2a3e',tableBorder:'#5a5a70',tableColor:'#e0e0ea',tableHeaderBg:'#363650',tabBarBg:'#363650',tabActiveBg:'#2e2e42',tabBorder:'#5a5a70',tabColor:'#ccc',calBg:'#2a2a3e',calBorder:'#5a5a70',calColor:'#e0e0ea',calHeaderBg:'#363650',calCellColor:'#ccc',dateBg:'#2e2e42',dateBorder:'#5a5a70',dateColor:'#e0e0ea',scrollBg:'#3a3a50',dialBg:'conic-gradient(from 220deg,#3b82f6 0%,#3b82f6 45%,#3a3a50 45%,#3a3a50 100%)',dialBorder:'#6a6a80',labelColor:'#e0e0ea'}
    },
    snow:{
        name:'Snow',
        swatch:'#f8fafc',
        ide:{bg:'#f1f5f9',bg2:'#ffffff',bg3:'#e2e8f0',bg4:'#cbd5e1',border:'#e2e8f0',border2:'#cbd5e1',text:'#0f172a',text2:'#475569',text3:'#94a3b8',accent:'#2563eb',accent2:'#1d4ed8','accent-glow':'rgba(37,99,235,0.12)',red:'#dc2626',green:'#16a34a',yellow:'#ca8a04',purple:'#7c3aed'},
        canvas:'#ffffff',
        widget:{btnBg:'linear-gradient(180deg,#f0f0f5,#dcdce5)',btnBorder:'#b0b0c0',btnColor:'#212529',inputBg:'#fafafe',inputBorder:'#b0b0c0',inputColor:'#212529',comboBg:'#fafafe',comboBorder:'#b0b0c0',comboColor:'#212529',checkColor:'#212529',groupBorder:'#9a9ab0',groupColor:'#212529',frameBorder:'#b0b0c0',progressBg:'#e9ecf2',progressBorder:'#b0b0c0',progressFill:'linear-gradient(90deg,#06b6d4,#3b82f6)',sliderTrack:'#d0d0dd',sliderThumb:'#fff',sliderThumbBorder:'#3b82f6',spinBg:'#fafafe',spinBorder:'#b0b0c0',spinColor:'#212529',lcdBg:'#1a1a2e',lcdColor:'#00ff88',listBg:'#fafafe',listBorder:'#b0b0c0',listColor:'#212529',listSelBg:'#3b82f6',listSelColor:'#fff',listItemBorder:'#e8e8f0',treeBg:'#fafafe',treeBorder:'#b0b0c0',treeColor:'#212529',tableBg:'#fafafe',tableBorder:'#b0b0c0',tableColor:'#212529',tableHeaderBg:'#f0f0f5',tabBarBg:'#e4e4ee',tabActiveBg:'#fafafe',tabBorder:'#b0b0c0',tabColor:'#212529',calBg:'#fafafe',calBorder:'#b0b0c0',calColor:'#212529',calHeaderBg:'#f0f0f5',calCellColor:'#333',dateBg:'#fafafe',dateBorder:'#b0b0c0',dateColor:'#212529',scrollBg:'#d4d4de',dialBg:'conic-gradient(from 220deg,#3b82f6 0%,#3b82f6 45%,#d0d0dd 45%,#d0d0dd 100%)',dialBorder:'#9a9ab0',labelColor:'#212529'}
    },
    classic:{
        name:'Classic',
        swatch:'#c0c0c0',
        ide:{bg:'#6b6b6b',bg2:'#808080',bg3:'#999999',bg4:'#aaaaaa',border:'#555555',border2:'#777777',text:'#ffffff',text2:'#dddddd',text3:'#bbbbbb',accent:'#000080',accent2:'#0000aa','accent-glow':'rgba(0,0,128,0.2)',red:'#cc0000',green:'#008800',yellow:'#ccaa00',purple:'#880088'},
        canvas:'#c0c0c0',
        widget:{btnBg:'linear-gradient(180deg,#e8e8e8,#d4d4d4)',btnBorder:'#888888',btnColor:'#000000',inputBg:'#ffffff',inputBorder:'#888888',inputColor:'#000000',comboBg:'#ffffff',comboBorder:'#888888',comboColor:'#000000',checkColor:'#000000',groupBorder:'#888888',groupColor:'#000000',frameBorder:'#888888',progressBg:'#e0e0e0',progressBorder:'#888888',progressFill:'linear-gradient(90deg,#000080,#0000cc)',sliderTrack:'#aaaaaa',sliderThumb:'#e8e8e8',sliderThumbBorder:'#000080',spinBg:'#fff',spinBorder:'#888888',spinColor:'#000',lcdBg:'#1a1a2e',lcdColor:'#00ff00',listBg:'#fff',listBorder:'#888888',listColor:'#000',listSelBg:'#000080',listSelColor:'#fff',listItemBorder:'#d0d0d0',treeBg:'#fff',treeBorder:'#888888',treeColor:'#000',tableBg:'#fff',tableBorder:'#888888',tableColor:'#000',tableHeaderBg:'#d0d0d0',tabBarBg:'#d0d0d0',tabActiveBg:'#e8e8e8',tabBorder:'#888888',tabColor:'#000',calBg:'#fff',calBorder:'#888888',calColor:'#000',calHeaderBg:'#d0d0d0',calCellColor:'#000',dateBg:'#fff',dateBorder:'#888888',dateColor:'#000',scrollBg:'#aaaaaa',dialBg:'conic-gradient(from 220deg,#000080 0%,#000080 45%,#aaaaaa 45%,#aaaaaa 100%)',dialBorder:'#888888',labelColor:'#000000'}
    },
    hacker:{
        name:'Hacker',
        swatch:'#001100',
        ide:{bg:'#000a00',bg2:'#001a00',bg3:'#002200',bg4:'#003300',border:'#003300',border2:'#004400',text:'#00ff00',text2:'#00cc00',text3:'#009900',accent:'#00ff00',accent2:'#00cc00','accent-glow':'rgba(0,255,0,0.1)',red:'#ff3333',green:'#00ff00',yellow:'#ffff00',purple:'#cc00ff'},
        canvas:'#000800',
        widget:{btnBg:'linear-gradient(180deg,#003a00,#002800)',btnBorder:'#00cc00',btnColor:'#00ff00',inputBg:'#001800',inputBorder:'#00bb00',inputColor:'#00ff00',comboBg:'#001800',comboBorder:'#00bb00',comboColor:'#00ff00',checkColor:'#00ff00',groupBorder:'#00bb00',groupColor:'#00ff00',frameBorder:'#00bb00',progressBg:'#001800',progressBorder:'#00bb00',progressFill:'linear-gradient(90deg,#005500,#00ff00)',sliderTrack:'#004400',sliderThumb:'#00ff00',sliderThumbBorder:'#000',spinBg:'#001800',spinBorder:'#00bb00',spinColor:'#00ff00',lcdBg:'#000500',lcdColor:'#00ff00',listBg:'#001800',listBorder:'#00bb00',listColor:'#00ff00',listSelBg:'#006600',listSelColor:'#00ff00',listItemBorder:'#003300',treeBg:'#001800',treeBorder:'#00bb00',treeColor:'#00ff00',tableBg:'#001800',tableBorder:'#00bb00',tableColor:'#00ff00',tableHeaderBg:'#003300',tabBarBg:'#003300',tabActiveBg:'#001800',tabBorder:'#00bb00',tabColor:'#00ff00',calBg:'#001800',calBorder:'#00bb00',calColor:'#00ff00',calHeaderBg:'#003300',calCellColor:'#00cc00',dateBg:'#001800',dateBorder:'#00bb00',dateColor:'#00ff00',scrollBg:'#004400',dialBg:'conic-gradient(from 220deg,#00ff00 0%,#00ff00 45%,#004400 45%,#004400 100%)',dialBorder:'#00bb00',labelColor:'#00ff00'}
    },
    ocean:{
        name:'Ocean',
        swatch:'#0c1222',
        ide:{bg:'#0c1222',bg2:'#131c31',bg3:'#1a2640',bg4:'#243352',border:'#1e2d4a',border2:'#2a3d5e',text:'#e2e8f0',text2:'#94a3b8',text3:'#64748b',accent:'#06b6d4',accent2:'#0891b2','accent-glow':'rgba(6,182,212,0.15)',red:'#f43f5e',green:'#10b981',yellow:'#f59e0b',purple:'#8b5cf6'},
        canvas:'#0f1729',
        widget:{btnBg:'linear-gradient(180deg,#253a58,#1c3048)',btnBorder:'#3a5575',btnColor:'#e2e8f0',inputBg:'#162238',inputBorder:'#3a5575',inputColor:'#e2e8f0',comboBg:'#162238',comboBorder:'#3a5575',comboColor:'#e2e8f0',checkColor:'#e2e8f0',groupBorder:'#3a5575',groupColor:'#e2e8f0',frameBorder:'#3a5575',progressBg:'#162238',progressBorder:'#3a5575',progressFill:'linear-gradient(90deg,#06b6d4,#0891b2)',sliderTrack:'#253a58',sliderThumb:'#06b6d4',sliderThumbBorder:'#e2e8f0',spinBg:'#162238',spinBorder:'#3a5575',spinColor:'#e2e8f0',lcdBg:'#060d1a',lcdColor:'#06b6d4',listBg:'#162238',listBorder:'#3a5575',listColor:'#e2e8f0',listSelBg:'#06b6d4',listSelColor:'#fff',listItemBorder:'#253a58',treeBg:'#162238',treeBorder:'#3a5575',treeColor:'#e2e8f0',tableBg:'#162238',tableBorder:'#3a5575',tableColor:'#e2e8f0',tableHeaderBg:'#1f3350',tabBarBg:'#1f3350',tabActiveBg:'#162238',tabBorder:'#3a5575',tabColor:'#94a3b8',calBg:'#162238',calBorder:'#3a5575',calColor:'#e2e8f0',calHeaderBg:'#1f3350',calCellColor:'#94a3b8',dateBg:'#162238',dateBorder:'#3a5575',dateColor:'#e2e8f0',scrollBg:'#253a58',dialBg:'conic-gradient(from 220deg,#06b6d4 0%,#06b6d4 45%,#253a58 45%,#253a58 100%)',dialBorder:'#3a5575',labelColor:'#e2e8f0'}
    }
};

const CATEGORIES={
    Buttons:{icon:'mouse-pointer-2',items:['QPushButton','QToolButton','QRadioButton','QCheckBox','QCommandLinkButton']},
    Input:{icon:'text-cursor',items:['QLineEdit','QTextEdit','QPlainTextEdit','QSpinBox','QDoubleSpinBox','QComboBox','QFontComboBox','QKeySequenceEdit','QDateEdit','QTimeEdit','QDateTimeEdit']},
    Display:{icon:'monitor',items:['QLabel','QProgressBar','QLCDNumber','QCalendarWidget','QImage','QTextBrowser']},
    Controls:{icon:'sliders-horizontal',items:['QSlider','QDial','QScrollBar']},
    Containers:{icon:'box',items:['QGroupBox','QTabWidget','QFrame','QScrollArea','QStackedWidget','QToolBox']},
    Views:{icon:'table',items:['QListWidget','QTreeWidget','QTableWidget']},
    Separators:{icon:'minus',items:['HLine','VLine']},
};

const W={
    QPushButton:{label:'Push Button',icon:'mouse-pointer-2',dw:100,dh:30,cat:'Buttons'},
    QToolButton:{label:'Tool Button',icon:'square',dw:32,dh:32,cat:'Buttons'},
    QLabel:{label:'Label',icon:'type',dw:80,dh:22,cat:'Display'},
    QLineEdit:{label:'Line Edit',icon:'text-cursor-input',dw:150,dh:26,cat:'Input'},
    QTextEdit:{label:'Text Edit',icon:'file-text',dw:200,dh:120,cat:'Input'},
    QPlainTextEdit:{label:'Plain Text',icon:'align-left',dw:200,dh:120,cat:'Input'},
    QGroupBox:{label:'Group Box',icon:'box',dw:240,dh:160,cat:'Containers',container:true},
    QTabWidget:{label:'Tab Widget',icon:'panel-top',dw:320,dh:220,cat:'Containers',container:true},
    QFrame:{label:'Frame',icon:'layout',dw:200,dh:150,cat:'Containers',container:true},
    QScrollArea:{label:'Scroll Area',icon:'scroll',dw:200,dh:150,cat:'Containers',container:true},
    QStackedWidget:{label:'Stacked',icon:'layers',dw:200,dh:150,cat:'Containers',container:true},
    QToolBox:{label:'Tool Box',icon:'briefcase',dw:200,dh:200,cat:'Containers',container:true},
    QCheckBox:{label:'Check Box',icon:'check-square',dw:110,dh:22,cat:'Buttons'},
    QRadioButton:{label:'Radio Button',icon:'circle-dot',dw:110,dh:22,cat:'Buttons'},
    QCommandLinkButton:{label:'Command Link',icon:'link',dw:180,dh:40,cat:'Buttons'},
    QComboBox:{label:'Combo Box',icon:'chevron-down',dw:130,dh:26,cat:'Input'},
    QFontComboBox:{label:'Font Combo',icon:'type',dw:160,dh:26,cat:'Input'},
    QKeySequenceEdit:{label:'Key Sequence',icon:'keyboard',dw:140,dh:26,cat:'Input'},
    QProgressBar:{label:'Progress Bar',icon:'loader',dw:200,dh:22,cat:'Display'},
    QSlider:{label:'Slider',icon:'sliders-horizontal',dw:160,dh:22,cat:'Controls'},
    QScrollBar:{label:'Scroll Bar',icon:'grip-vertical',dw:16,dh:120,cat:'Controls'},
    QSpinBox:{label:'Spin Box',icon:'hash',dw:80,dh:26,cat:'Input'},
    QDoubleSpinBox:{label:'Double Spin',icon:'hash',dw:90,dh:26,cat:'Input'},
    QLCDNumber:{label:'LCD Number',icon:'monitor',dw:80,dh:34,cat:'Display'},
    QDial:{label:'Dial',icon:'disc',dw:64,dh:64,cat:'Controls'},
    QCalendarWidget:{label:'Calendar',icon:'calendar',dw:280,dh:200,cat:'Display'},
    QListWidget:{label:'List Widget',icon:'list',dw:160,dh:150,cat:'Views'},
    QTreeWidget:{label:'Tree Widget',icon:'git-branch',dw:160,dh:150,cat:'Views'},
    QTableWidget:{label:'Table Widget',icon:'table',dw:240,dh:150,cat:'Views'},
    QDateEdit:{label:'Date Edit',icon:'calendar',dw:110,dh:26,cat:'Input'},
    QTimeEdit:{label:'Time Edit',icon:'clock',dw:90,dh:26,cat:'Input'},
    QDateTimeEdit:{label:'DateTime',icon:'calendar-clock',dw:160,dh:26,cat:'Input'},
    QTextBrowser:{label:'Text Browser',icon:'globe',dw:200,dh:150,cat:'Display'},
    QImage:{label:'Image',icon:'image',dw:100,dh:100,cat:'Display',xmlClass:'QLabel'},
    VLine:{label:'V-Line',icon:'grip-vertical',dw:3,dh:100,cat:'Separators',xmlClass:'Line'},
    HLine:{label:'H-Line',icon:'grip-horizontal',dw:100,dh:3,cat:'Separators',xmlClass:'Line'},
};

const CURSORS=["ArrowCursor","UpArrowCursor","CrossCursor","WaitCursor","IBeamCursor","SizeVerCursor","SizeHorCursor","SizeBDiagCursor","SizeFDiagCursor","SizeAllCursor","BlankCursor","SplitVCursor","SplitHCursor","PointingHandCursor","ForbiddenCursor","OpenHandCursor","ClosedHandCursor","WhatsThisCursor"];
const SIZE_POLICIES=["Fixed","Minimum","Maximum","Preferred","Expanding","MinimumExpanding","Ignored"];

/* ───── QSS Generator ───── */
const parseGradient=(val)=>{
    if(!val||!val.includes('gradient'))return val;
    if(val.startsWith('linear-gradient')){
        const parts=val.match(/linear-gradient\((\d+)deg,\s*(.+)\)/);
        if(!parts)return val;
        const deg=parseInt(parts[1]);
        const colors=parts[2].split(',').map(s=>s.trim());
        let x1=0,y1=0,x2=0,y2=0;
        if(deg===180){x1=0;y1=0;x2=0;y2=1;}
        else if(deg===90){x1=0;y1=0;x2=1;y2=0;}
        if(colors.length>=2){
            return `qlineargradient(spread:pad, x1:${x1}, y1:${y1}, x2:${x2}, y2:${y2}, stop:0 ${colors[0]}, stop:1 ${colors[1]})`;
        }
        return colors[0];
    }
    if(val.startsWith('conic-gradient')){
        const match=val.match(/#[0-9a-fA-F]{3,6}/);
        return match?match[0]:'transparent';
    }
    return val;
};

const generateThemeQSS=(themeName)=>{
    const t=THEMES[themeName];if(!t)return '';
    const w=t.widget;
    const btnBg=parseGradient(w.btnBg);
    const progressFill=parseGradient(w.progressFill);

    return `
/* Global Defaults */
QWidget{font-family:'Segoe UI',sans-serif;font-size:11px}
/* QPushButton */
QPushButton{background-color:${btnBg};border:1px solid ${w.btnBorder};border-radius:4px;color:${w.btnColor};padding:4px 12px}
QPushButton:hover{background-color:${w.btnBorder}}
QPushButton:pressed{background-color:${w.btnColor};color:${w.btnBg.includes('gradient')?'#000':'#fff'}}
/* QToolButton */
QToolButton{background-color:${btnBg};border:1px solid ${w.btnBorder};border-radius:4px;color:${w.btnColor}}
/* QLineEdit, QAbstractSpinBox */
QLineEdit,QAbstractSpinBox,QDateEdit,QTimeEdit,QDateTimeEdit{background-color:${w.inputBg};border:1px solid ${w.inputBorder};border-radius:3px;color:${w.inputColor};padding:2px 4px}
QLineEdit:focus,QAbstractSpinBox:focus{border:1px solid ${t.ide.accent}}
/* QTextEdit, QPlainTextEdit */
QTextEdit,QPlainTextEdit{background-color:${w.inputBg};border:1px solid ${w.inputBorder};border-radius:3px;color:${w.inputColor}}
/* QComboBox */
QComboBox{background-color:${w.comboBg};border:1px solid ${w.comboBorder};border-radius:3px;color:${w.comboColor};padding:2px 4px}
QComboBox::drop-down{border:none;background:transparent}
QComboBox::down-arrow{image:none;border-left:1px solid ${w.comboBorder};width:12px;height:12px;background:${w.comboBorder}}
/* QCheckBox, QRadioButton */
QCheckBox,QRadioButton{color:${w.checkColor};spacing:5px}
QCheckBox::indicator,QRadioButton::indicator{width:14px;height:14px;border:1px solid ${w.inputBorder};background:${w.inputBg};border-radius:2px}
QRadioButton::indicator{border-radius:7px}
QCheckBox::indicator:checked,QRadioButton::indicator:checked{background-color:${t.ide.accent};border-color:${t.ide.accent}}
/* QGroupBox */
QGroupBox{border:1px solid ${w.groupBorder};border-radius:4px;margin-top:16px;font-weight:bold}
QGroupBox::title{subcontrol-origin:margin;subcontrol-position:top left;left:8px;padding:0 3px;color:${w.groupColor};background-color:${t.canvas}}
/* QProgressBar */
QProgressBar{background-color:${w.progressBg};border:1px solid ${w.progressBorder};border-radius:3px;text-align:center;color:${w.labelColor}}
QProgressBar::chunk{background-color:${t.ide.accent};width:20px}
/* QSlider */
QSlider::groove:horizontal{border:1px solid ${w.sliderTrack};height:4px;background:${w.sliderTrack};margin:2px 0;border-radius:2px}
QSlider::handle:horizontal{background:${w.sliderThumb};border:1px solid ${w.sliderThumbBorder};width:12px;height:12px;margin:-5px 0;border-radius:6px}
/* QTabWidget */
QTabWidget::pane{border:1px solid ${w.tabBorder};background:${w.tabActiveBg};border-top:none}
QTabBar::tab{background:${w.tabBarBg};border:1px solid ${w.tabBorder};border-bottom-color:${w.tabBorder};color:${w.tabColor};padding:4px 10px;border-top-left-radius:4px;border-top-right-radius:4px}
QTabBar::tab:selected{background:${w.tabActiveBg};border-bottom-color:${w.tabActiveBg};margin-bottom:-1px}
/* Item Views */
QListWidget,QTreeWidget,QTableWidget{background-color:${w.listBg};border:1px solid ${w.listBorder};color:${w.listColor};outline:none}
QHeaderView::section{background-color:${w.tableHeaderBg};color:${w.labelColor};padding:4px;border:1px solid ${w.tableBorder}}
/* QCalendarWidget */
QCalendarWidget QWidget{background-color:${w.calBg};color:${w.calColor}}
QCalendarWidget QTableView{background-color:${w.calBg};selection-background-color:${t.ide.accent}}
/* QLabel */
QLabel{color:${w.labelColor};background-color:${w.inputBg};border:1px solid transparent;border-radius:3px;padding:2px}
/* QLCDNumber */
QLCDNumber{background-color:${w.lcdBg};color:${w.lcdColor};border:2px inset ${w.frameBorder}}
    `.replace(/\n/g,'');
};

/* ───── Icon Component ───── */
const Ico=({name,size=16})=>{
    const r=useRef(null);
    useEffect(()=>{
        if(window.lucide&&r.current){
            r.current.innerHTML=`<i data-lucide="${name}"></i>`;
            window.lucide.createIcons({attrs:{width:size,height:size},nameAttr:'data-lucide',root:r.current});
        }
    },[name,size]);
    return <span ref={r} className="inline-flex items-center justify-center pointer-events-none"/>;
};

/* ───── Helpers ───── */
const snap=(v,grid)=>Math.round(v/grid)*grid;
const clamp=(v,min,max)=>Math.max(min,Math.min(max,v));
const uid=()=>`w${Date.now().toString(36)}${Math.random().toString(36).slice(2,6)}`;

const defaultEl=(type,x,y,idx,gridSize)=>{
    const c=W[type];if(!c)return null;
    return{
        id:uid(),type,
        name:`${(c.xmlClass||type).replace('Q','').toLowerCase()}_${idx}`,
        x:snap(x,gridSize),y:snap(y,gridSize),
        w:c.dw,h:c.dh,
        zIndex:idx,locked:false,
        text:type.includes('Button')?'Button':type.includes('Label')?'Label':type==='QGroupBox'?'Group':'',
        bg:'',color:'',fontSize:0,fontWeight:'normal',fontItalic:false,fontFamily:'',
        enabled:true,visible:true,tooltip:'',
        items:type==='QComboBox'?['Item 1','Item 2','Item 3']:[],
        pixmap:'',cursor:'ArrowCursor',
        placeholderText:'',readOnly:false,flat:false,checkable:false,checked:false,
        tabs:type==='QTabWidget'?['Tab 1','Tab 2']:[],
        pages:type==='QStackedWidget'?['Page 1','Page 2']:type==='QToolBox'?['Section 1','Section 2']:[],
        hAlign:'center',vAlign:'center',
        minW:0,minH:0,maxW:16777215,maxH:16777215,
        sizeH:'Preferred',sizeV:'Preferred',
        value:type==='QProgressBar'?45:type==='QSlider'?50:type==='QSpinBox'||type==='QDoubleSpinBox'?0:type==='QLCDNumber'?42:0,
        minimum:0,maximum:type==='QProgressBar'||type==='QSlider'?100:type==='QSpinBox'?99:type==='QDoubleSpinBox'?99.99:0,
        orientation:type==='QScrollBar'?'vertical':'horizontal',
        rows:type==='QTableWidget'?3:0,
        columns:type==='QTableWidget'?3:0,
        columnHeaders:type==='QTableWidget'?['Col 1','Col 2','Col 3']:[],
        echoMode:'Normal',
        inputMask:'',
        keySequence:type==='QKeySequenceEdit'?'Ctrl+O':'',
        styleSheet:'',
    };
};

/* ───── Main App ───── */
const App=()=>{
    const[elements,setElements]=useState([]);
    const[selectedIds,setSelectedIds]=useState([]);
    const[snapEnabled,setSnapEnabled]=useState(true);
    const[gridSize,setGridSize]=useState(20);
    const[canvasSize,setCanvasSize]=useState({w:800,h:600});
    const[canvasBg,setCanvasBg]=useState('#f0f0f0');
    const[windowTitle,setWindowTitle]=useState('MainWindow');
    const[bridge,setBridge]=useState(null);
    const[tab,setTab]=useState('design');  // design | xml | python
    const[ctxMenu,setCtxMenu]=useState(null);
    const[zoom,setZoom]=useState(1);
    const[menus,setMenus]=useState([]);
    const[clipboard,setClipboard]=useState([]);
    const[widgetSearch,setWidgetSearch]=useState('');
    const[rubberBand,setRubberBand]=useState(null);
    const[panOffset,setPanOffset]=useState({x:0,y:0});
    const[guides,setGuides]=useState([]);
    const[leftPanel,setLeftPanel]=useState('widgets'); // widgets | tree
    const[counter,setCounter]=useState(1);
    const[activeTheme,setActiveTheme]=useState('midnight');

    // Apply theme to CSS variables
    const applyTheme=useCallback((key)=>{
        const t=THEMES[key];if(!t)return;
        setActiveTheme(key);
        setCanvasBg(t.canvas);
        const r=document.documentElement;
        Object.entries(t.ide).forEach(([k,v])=>{r.style.setProperty('--'+k,v);});
    },[]);

    // Get current theme's widget palette
    const tw=THEMES[activeTheme]?.widget||THEMES.midnight.widget;

    // History
    const[history,setHistory]=useState([JSON.stringify([])]);
    const[histIdx,setHistIdx]=useState(0);
    const histRef=useRef({history:[JSON.stringify([])],idx:0});

    const elemRef=useRef(elements);
    useEffect(()=>{elemRef.current=elements;},[elements]);
    const selRef=useRef(selectedIds);
    useEffect(()=>{selRef.current=selectedIds;},[selectedIds]);

    const canvasRef=useRef(null);
    const dragRef=useRef({mode:null,startX:0,startY:0,handle:'',initEls:[],rubberStart:null});

    // Push to history
    const pushHistory=useCallback((els)=>{
        const s=JSON.stringify(els);
        const h=histRef.current;
        const trimmed=h.history.slice(0,h.idx+1);
        trimmed.push(s);
        if(trimmed.length>80)trimmed.shift();
        histRef.current={history:trimmed,idx:trimmed.length-1};
        setHistory(trimmed);
        setHistIdx(trimmed.length-1);
    },[]);

    const updateEls=useCallback((els)=>{
        setElements(els);
        pushHistory(els);
    },[pushHistory]);

    const undo=useCallback(()=>{
        const h=histRef.current;
        if(h.idx>0){
            const ni=h.idx-1;
            histRef.current.idx=ni;
            setHistIdx(ni);
            setElements(JSON.parse(h.history[ni]));
        }
    },[]);

    const redo=useCallback(()=>{
        const h=histRef.current;
        if(h.idx<h.history.length-1){
            const ni=h.idx+1;
            histRef.current.idx=ni;
            setHistIdx(ni);
            setElements(JSON.parse(h.history[ni]));
        }
    },[]);

    // Bridge
    useEffect(()=>{
        if(typeof qt!=='undefined'){
            new QWebChannel(qt.webChannelTransport,(ch)=>{
                const b=ch.objects.pyBridge;
                setBridge(b);
                b.ui_imported.connect((xml)=>importFromXml(xml));
            });
        }
    },[]);

    /* ── XML Import ── */
    const importFromXml=(xmlString)=>{
        try{
            const doc=new DOMParser().parseFromString(xmlString,"text/xml");
            const root=doc.getElementsByTagName("widget")[0];
            if(!root)return;
            const central=Array.from(root.children).find(c=>c.getAttribute('name')==='centralwidget');
            if(!central)return;
            const parsed=parseXmlNode(central,0,0);
            updateEls(parsed);
        }catch(e){console.error("Import error",e);}
    };

    const parseXmlNode=(node,px,py)=>{
        const results=[];
        let x=0,y=0,w=100,h=30;
        for(let p of node.children){
            if(p.tagName==='property'&&p.getAttribute('name')==='geometry'){
                const rect=p.getElementsByTagName('rect')[0];
                if(rect){
                    x=parseInt(rect.getElementsByTagName('x')[0]?.textContent||0);
                    y=parseInt(rect.getElementsByTagName('y')[0]?.textContent||0);
                    w=parseInt(rect.getElementsByTagName('width')[0]?.textContent||100);
                    h=parseInt(rect.getElementsByTagName('height')[0]?.textContent||30);
                }
            }
        }
        const ax=px+x,ay=py+y;
        const cls=node.getAttribute('class');
        const nm=node.getAttribute('name');
        if(W[cls]||cls==='QLabel'||cls==='Line'){
            const el=defaultEl(cls,ax,ay,results.length+1,gridSize);
            if(el){
                el.name=nm||el.name;
                el.x=ax;el.y=ay;el.w=w;el.h=h;
                for(let p of node.children){
                    if(p.tagName==='property'){
                        const n=p.getAttribute('name');
                        const s=p.getElementsByTagName('string')[0]?.textContent;
                        const b=p.getElementsByTagName('bool')[0]?.textContent==='true';
                        if(n==='text'||n==='title')el.text=s||'';
                        if(n==='toolTip')el.tooltip=s||'';
                        if(n==='readOnly')el.readOnly=b;
                        if(n==='placeholderText')el.placeholderText=s||'';
                        if(n==='flat')el.flat=b;
                        if(n==='checkable')el.checkable=b;
                        if(n==='checked')el.checked=b;
                    }
                }
                results.push(el);
            }
        }
        for(let child of node.children){
            if(child.tagName==='widget')results.push(...parseXmlNode(child,ax,ay));
        }
        return results;
    };

    /* ── XML Generation ── */
    const buildHierarchy=(flat)=>{
        const nodes=flat.map(e=>({...e,children:[]}));
        const roots=[];
        const sorted=[...nodes].sort((a,b)=>(a.w*a.h)-(b.w*b.h));
        sorted.forEach(node=>{
            let best=null,minArea=Infinity;
            nodes.forEach(p=>{
                if(node.id===p.id)return;
                if(!W[p.type]?.container)return;
                if(node.x>=p.x&&node.y>=p.y&&node.x+node.w<=p.x+p.w&&node.y+node.h<=p.y+p.h){
                    const a=p.w*p.h;
                    if(a<minArea){minArea=a;best=p;}
                }
            });
            if(best)best.children.push(node);
            else roots.push(node);
        });
        return roots;
    };

    const xmlProp=(name,type,val)=>{
        if(type==='string')return `<property name="${name}"><string>${escXml(val)}</string></property>`;
        if(type==='bool')return `<property name="${name}"><bool>${val}</bool></property>`;
        if(type==='number')return `<property name="${name}"><number>${val}</number></property>`;
        if(type==='enum')return `<property name="${name}"><enum>${val}</enum></property>`;
        if(type==='set')return `<property name="${name}"><set>${val}</set></property>`;
        return '';
    };
    const escXml=(s)=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');

    const genWidgetXml=(el,rx,ry,indent='    ')=>{
        const cls=W[el.type]?.xmlClass||el.type;
        let xmlCls=cls;
        let props='';
        let extra='';

        // Whitelists for properties that only apply to certain widgets
        const HAS_TEXT=new Set(['QPushButton','QToolButton','QCommandLinkButton','QLabel','QLineEdit','QTextEdit','QPlainTextEdit','QTextBrowser','QCheckBox','QRadioButton','QGroupBox','QImage']);
        const HAS_ALIGN=new Set(['QLabel','QLineEdit','QImage','QProgressBar','QSpinBox','QDoubleSpinBox','QDateEdit','QTimeEdit','QDateTimeEdit']);
        const HAS_PLACEHOLDER=new Set(['QLineEdit','QTextEdit','QPlainTextEdit']);
        const HAS_READONLY=new Set(['QLineEdit','QTextEdit','QPlainTextEdit','QTextBrowser','QSpinBox','QDoubleSpinBox','QDateEdit','QTimeEdit','QDateTimeEdit']);
        const HAS_FLAT=new Set(['QPushButton','QCommandLinkButton','QGroupBox']);
        const HAS_CHECKABLE=new Set(['QPushButton','QToolButton','QCommandLinkButton','QGroupBox']);
        const HAS_CHECKED=new Set(['QPushButton','QToolButton','QCommandLinkButton','QCheckBox','QRadioButton','QGroupBox']);
        const HAS_PIXMAP=new Set(['QLabel','QImage']);

        // Geometry
        props+=`${indent}  <property name="geometry"><rect><x>${Math.round(rx)}</x><y>${Math.round(ry)}</y><width>${Math.round(el.w)}</width><height>${Math.round(el.h)}</height></rect></property>\n`;

        // Text (only for widgets that have setText)
        if(el.text&&HAS_TEXT.has(el.type)&&el.type!=='QComboBox')props+=`${indent}  `+xmlProp('text','string',el.text)+'\n';
        // GroupBox title uses 'title' property
        if(el.text&&el.type==='QGroupBox')props=props.replace(xmlProp('text','string',el.text),xmlProp('title','string',el.text));

        if(el.tooltip)props+=`${indent}  `+xmlProp('toolTip','string',el.tooltip)+'\n';
        if(!el.enabled)props+=`${indent}  `+xmlProp('enabled','bool','false')+'\n';
        if(!el.visible)props+=`${indent}  `+xmlProp('visible','bool','false')+'\n';
        if(el.cursor&&el.cursor!=='ArrowCursor')props+=`${indent}  <property name="cursor"><cursorShape>${el.cursor}</cursorShape></property>\n`;
        if(el.readOnly&&HAS_READONLY.has(el.type))props+=`${indent}  `+xmlProp('readOnly','bool','true')+'\n';
        if(el.placeholderText&&HAS_PLACEHOLDER.has(el.type))props+=`${indent}  `+xmlProp('placeholderText','string',el.placeholderText)+'\n';
        if(el.flat&&HAS_FLAT.has(el.type))props+=`${indent}  `+xmlProp('flat','bool','true')+'\n';
        if(el.checkable&&HAS_CHECKABLE.has(el.type))props+=`${indent}  `+xmlProp('checkable','bool','true')+'\n';
        if(el.checked&&HAS_CHECKED.has(el.type))props+=`${indent}  `+xmlProp('checked','bool','true')+'\n';
        if(el.keySequence&&el.type==='QKeySequenceEdit')props+=`${indent}  `+xmlProp('keySequence','string',el.keySequence)+'\n';
        if(el.pixmap&&HAS_PIXMAP.has(el.type))props+=`${indent}  <property name="pixmap"><pixmap>${escXml(el.pixmap)}</pixmap></property>\n`;
        if(el.value&&(el.type==='QProgressBar'||el.type==='QSlider'||el.type==='QSpinBox'||el.type==='QDoubleSpinBox'||el.type==='QLCDNumber'))
            props+=`${indent}  `+xmlProp('value','number',el.value)+'\n';
        if(el.minimum&&(el.type==='QProgressBar'||el.type==='QSlider'||el.type==='QSpinBox'||el.type==='QDoubleSpinBox'))
            props+=`${indent}  `+xmlProp('minimum','number',el.minimum)+'\n';
        if(el.maximum&&(el.type==='QProgressBar'||el.type==='QSlider'||el.type==='QSpinBox'||el.type==='QDoubleSpinBox'))
            props+=`${indent}  `+xmlProp('maximum','number',el.maximum)+'\n';

        // StyleSheet
        let ss=el.styleSheet||'';
        if(el.bg)ss+=`background-color:${el.bg};`;
        if(el.color)ss+=`color:${el.color};`;
        if(el.fontSize)ss+=`font-size:${el.fontSize}pt;`;
        if(el.fontFamily)ss+=`font-family:'${el.fontFamily}';`;
        if(el.fontWeight!=='normal')ss+=`font-weight:${el.fontWeight};`;
        if(el.fontItalic)ss+=`font-style:italic;`;
        if(ss)props+=`${indent}  `+xmlProp('styleSheet','string',ss)+'\n';

        // Alignment (only for widgets that actually support it)
        if(HAS_ALIGN.has(el.type)){
            let als=[];
            if(el.hAlign==='left')als.push('Qt::AlignLeft');
            else if(el.hAlign==='right')als.push('Qt::AlignRight');
            else if(el.hAlign==='justify')als.push('Qt::AlignJustify');
            else als.push('Qt::AlignHCenter');
            if(el.vAlign==='top')als.push('Qt::AlignTop');
            else if(el.vAlign==='bottom')als.push('Qt::AlignBottom');
            else als.push('Qt::AlignVCenter');
            if(als.length)props+=`${indent}  `+xmlProp('alignment','set',als.join('|'))+'\n';
        }

        // Size policy
        if(el.sizeH!=='Preferred'||el.sizeV!=='Preferred'){
            props+=`${indent}  <property name="sizePolicy"><sizepolicy hsizetype="${el.sizeH}" vsizetype="${el.sizeV}"/></property>\n`;
        }
        if(el.minW||el.minH)props+=`${indent}  <property name="minimumSize"><size><width>${el.minW}</width><height>${el.minH}</height></size></property>\n`;
        if(el.maxW<16777215||el.maxH<16777215)props+=`${indent}  <property name="maximumSize"><size><width>${el.maxW}</width><height>${el.maxH}</height></size></property>\n`;

        // Type-specific
        if(el.type==='VLine'){xmlCls='Line';extra+=`${indent}  `+xmlProp('orientation','enum','Qt::Vertical')+'\n';}
        if(el.type==='HLine'){xmlCls='Line';extra+=`${indent}  `+xmlProp('orientation','enum','Qt::Horizontal')+'\n';}
        if(el.type==='QComboBox'){el.items.forEach(it=>{extra+=`${indent}  <item><property name="text"><string>${escXml(it)}</string></property></item>\n`;});}
        if(el.type==='QTabWidget'){el.tabs.forEach((t,i)=>{extra+=`${indent}  <widget class="QWidget" name="tab_${el.name}_${i}"><attribute name="title"><string>${escXml(t)}</string></attribute></widget>\n`;});}

        // Children
        let childXml='';
        if(el.children)el.children.forEach(ch=>{childXml+=genWidgetXml(ch,ch.x-el.x,ch.y-el.y,indent+'  ');});

        return `${indent}<widget class="${xmlCls}" name="${el.name}">\n${props}${extra}${childXml}${indent}</widget>\n`;
    };

    const generateXML=()=>{
        const hier=buildHierarchy(elements);
        let wxml='';
        hier.forEach(el=>{wxml+=genWidgetXml(el,el.x,el.y,'   ');});

        let mbar='';
        if(menus.length>0){
            mbar=`  <widget class="QMenuBar" name="menubar">\n   <property name="geometry"><rect><x>0</x><y>0</y><width>${canvasSize.w}</width><height>22</height></rect></property>\n`;
            menus.forEach(m=>{mbar+=`   <widget class="QMenu" name="menu_${m.replace(/\s+/g,'_').toLowerCase()}"><property name="title"><string>${escXml(m)}</string></property></widget>\n`;});
            mbar+=`  </widget>\n`;
        }

        return `<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry"><rect><x>0</x><y>0</y><width>${canvasSize.w}</width><height>${canvasSize.h}</height></rect></property>
  <property name="windowTitle"><string>${escXml(windowTitle)}</string></property>
  <widget class="QWidget" name="centralwidget">
   <property name="styleSheet"><string>${escXml(generateThemeQSS(activeTheme))}\nQWidget#centralwidget{background-color:${canvasBg};}</string></property>
${wxml}  </widget>
${mbar}  <widget class="QStatusBar" name="statusbar"/>
 </widget>
</ui>`;
    };

    /* ── Python Code Generation ── */
    const generatePython=()=>{
        const cls='Ui_MainWindow';
        let lines=[];
        lines.push(`# Auto-generated by PyQt Designer Pro`);
        lines.push(`# WARNING: Changes will be overwritten if regenerated\n`);
        lines.push(`from PyQt6.QtWidgets import *`);
        lines.push(`from PyQt6.QtCore import *`);
        lines.push(`from PyQt6.QtGui import *\n`);
        lines.push(`class ${cls}:`);
        lines.push(`    def setupUi(self, MainWindow):`);
        lines.push(`        MainWindow.setObjectName("MainWindow")`);
        lines.push(`        MainWindow.resize(${canvasSize.w}, ${canvasSize.h})`);
        lines.push(`        MainWindow.setWindowTitle("${windowTitle}")`);
        lines.push(`        self.centralwidget = QWidget(MainWindow)`);
        lines.push(`        self.centralwidget.setObjectName("centralwidget")`);
        const themeQSS = generateThemeQSS(activeTheme);
        const fullQSS = themeQSS + (canvasBg ? `\nQWidget#centralwidget{background-color:${canvasBg};}` : '');
        lines.push(`        self.centralwidget.setStyleSheet(\"\"\"${fullQSS}\"\"\")`);
        lines.push('');

        elements.forEach(el=>{
            const cls=W[el.type]?.xmlClass||el.type;
            const pyClass=cls==='Line'?'QFrame':cls;

            // Whitelists
            const HAS_TEXT=new Set(['QPushButton','QToolButton','QCommandLinkButton','QLabel','QLineEdit','QTextEdit','QPlainTextEdit','QTextBrowser','QCheckBox','QRadioButton','QImage']);
            const HAS_TITLE=new Set(['QGroupBox']);
            const HAS_ALIGN=new Set(['QLabel','QLineEdit','QImage','QProgressBar','QSpinBox','QDoubleSpinBox','QDateEdit','QTimeEdit','QDateTimeEdit']);
            const HAS_PLACEHOLDER=new Set(['QLineEdit','QTextEdit','QPlainTextEdit']);
            const HAS_READONLY=new Set(['QLineEdit','QTextEdit','QPlainTextEdit','QTextBrowser','QSpinBox','QDoubleSpinBox','QDateEdit','QTimeEdit','QDateTimeEdit']);
            const HAS_FLAT=new Set(['QPushButton','QCommandLinkButton','QGroupBox']);
            const HAS_CHECKABLE=new Set(['QPushButton','QToolButton','QCommandLinkButton','QGroupBox']);
            const HAS_CHECKED=new Set(['QPushButton','QToolButton','QCommandLinkButton','QCheckBox','QRadioButton','QGroupBox']);

            lines.push(`        self.${el.name} = ${pyClass}(self.centralwidget)`);
            lines.push(`        self.${el.name}.setObjectName("${el.name}")`);
            lines.push(`        self.${el.name}.setGeometry(QRect(${Math.round(el.x)}, ${Math.round(el.y)}, ${Math.round(el.w)}, ${Math.round(el.h)}))`);
            if(el.text&&HAS_TEXT.has(el.type)&&el.type!=='QComboBox')lines.push(`        self.${el.name}.setText("${el.text.replace(/"/g,'\\"')}")`);
            if(el.text&&HAS_TITLE.has(el.type))lines.push(`        self.${el.name}.setTitle("${el.text.replace(/"/g,'\\"')}")`);
            if(el.tooltip)lines.push(`        self.${el.name}.setToolTip("${el.tooltip.replace(/"/g,'\\"')}")`);
            if(!el.enabled)lines.push(`        self.${el.name}.setEnabled(False)`);
            if(el.placeholderText&&HAS_PLACEHOLDER.has(el.type))lines.push(`        self.${el.name}.setPlaceholderText("${el.placeholderText.replace(/"/g,'\\"')}")`);
            if(el.readOnly&&HAS_READONLY.has(el.type))lines.push(`        self.${el.name}.setReadOnly(True)`);
            if(el.flat&&HAS_FLAT.has(el.type))lines.push(`        self.${el.name}.setFlat(True)`);
            if(el.checkable&&HAS_CHECKABLE.has(el.type))lines.push(`        self.${el.name}.setCheckable(True)`);
            if(el.checked&&HAS_CHECKED.has(el.type))lines.push(`        self.${el.name}.setChecked(True)`);
            if(el.keySequence&&el.type==='QKeySequenceEdit')lines.push(`        self.${el.name}.setKeySequence("${el.keySequence.replace(/"/g,'\\"')}")`);
            if(el.type==='QComboBox'&&el.items.length)lines.push(`        self.${el.name}.addItems(${JSON.stringify(el.items)})`);
            if(el.type==='VLine'){lines.push(`        self.${el.name}.setFrameShape(QFrame.Shape.VLine)`);lines.push(`        self.${el.name}.setFrameShadow(QFrame.Shadow.Sunken)`);}
            if(el.type==='HLine'){lines.push(`        self.${el.name}.setFrameShape(QFrame.Shape.HLine)`);lines.push(`        self.${el.name}.setFrameShadow(QFrame.Shadow.Sunken)`);}
            if(el.value&&(el.type==='QProgressBar'||el.type==='QSlider'||el.type==='QSpinBox'||el.type==='QDoubleSpinBox'))lines.push(`        self.${el.name}.setValue(${el.value})`);
            if(el.value&&el.type==='QLCDNumber')lines.push(`        self.${el.name}.display(${el.value})`);
            if(el.type==='QTabWidget'&&el.tabs){el.tabs.forEach((t,i)=>{lines.push(`        self.tab_${el.name}_${i} = QWidget()`);lines.push(`        self.${el.name}.addTab(self.tab_${el.name}_${i}, "${t.replace(/"/g,'\\"')}")`);});}
            if(el.type==='QListWidget'&&el.items){el.items.forEach(it=>{lines.push(`        self.${el.name}.addItem("${it.replace(/"/g,'\\"')}")`);});}

            // Alignment (only for supported widgets)
            if(HAS_ALIGN.has(el.type)&&(el.hAlign!=='center'||el.vAlign!=='center')){
                let alParts=[];
                if(el.hAlign==='left')alParts.push('Qt.AlignmentFlag.AlignLeft');
                else if(el.hAlign==='right')alParts.push('Qt.AlignmentFlag.AlignRight');
                else if(el.hAlign==='justify')alParts.push('Qt.AlignmentFlag.AlignJustify');
                else alParts.push('Qt.AlignmentFlag.AlignHCenter');
                if(el.vAlign==='top')alParts.push('Qt.AlignmentFlag.AlignTop');
                else if(el.vAlign==='bottom')alParts.push('Qt.AlignmentFlag.AlignBottom');
                else alParts.push('Qt.AlignmentFlag.AlignVCenter');
                lines.push(`        self.${el.name}.setAlignment(${alParts.join(' | ')})`);
            }
            let ss='';
            if(el.bg)ss+=`background-color:${el.bg};`;
            if(el.color)ss+=`color:${el.color};`;
            if(el.fontSize)ss+=`font-size:${el.fontSize}pt;`;
            if(el.fontFamily)ss+=`font-family:${el.fontFamily};`;
            if(el.fontWeight!=='normal')ss+=`font-weight:${el.fontWeight};`;
            if(el.fontItalic)ss+=`font-style:italic;`;
            ss+=el.styleSheet||'';
            if(ss)lines.push(`        self.${el.name}.setStyleSheet("${ss}")`);
            lines.push('');
        });

        lines.push(`        MainWindow.setCentralWidget(self.centralwidget)`);
        if(menus.length){
            lines.push(`        self.menubar = QMenuBar(MainWindow)`);
            menus.forEach(m=>{
                const vn=m.replace(/\s+/g,'_').toLowerCase();
                lines.push(`        self.menu_${vn} = QMenu("${m}", self.menubar)`);
                lines.push(`        self.menubar.addMenu(self.menu_${vn})`);
            });
            lines.push(`        MainWindow.setMenuBar(self.menubar)`);
        }
        lines.push(`        self.statusbar = QStatusBar(MainWindow)`);
        lines.push(`        MainWindow.setStatusBar(self.statusbar)\n`);
        lines.push(`\nif __name__ == "__main__":`);
        lines.push(`    import sys`);
        lines.push(`    app = QApplication(sys.argv)`);
        lines.push(`    window = QMainWindow()`);
        lines.push(`    ui = ${cls}()`);
        lines.push(`    ui.setupUi(window)`);
        lines.push(`    window.show()`);
        lines.push(`    sys.exit(app.exec())`);
        return lines.join('\n');
    };

    /* ── Add Widget ── */
    const addWidget=(type,x,y)=>{
        const c=W[type];if(!c)return;
        const n=counter;
        setCounter(n+1);
        const el=defaultEl(type,x,y,n,snapEnabled?gridSize:1);
        if(!el)return;
        el.zIndex=elements.length+1;
        const next=[...elements,el];
        updateEls(next);
        setSelectedIds([el.id]);
    };

    /* ── Drag & Drop / Move / Resize ── */
    const startMove=(e,id)=>{
        if(tab!=='design')return;
        e.stopPropagation();
        const el=elements.find(x=>x.id===id);
        if(el?.locked)return;

        let next;
        if(e.shiftKey){
            next=selectedIds.includes(id)?selectedIds.filter(x=>x!==id):[...selectedIds,id];
        }else if(!selectedIds.includes(id)){
            next=[id];
        }else{
            next=[...selectedIds];
        }
        setSelectedIds(next);

        dragRef.current={
            mode:'move',startX:e.clientX,startY:e.clientY,
            handle:'',initEls:JSON.parse(JSON.stringify(elemRef.current)),
            selectedIds:next,rubberStart:null
        };
    };

    const startResize=(e,id,handle)=>{
        e.stopPropagation();e.preventDefault();
        setSelectedIds([id]);
        dragRef.current={
            mode:'resize',startX:e.clientX,startY:e.clientY,
            handle,initEls:JSON.parse(JSON.stringify(elemRef.current)),
            selectedIds:[id],rubberStart:null
        };
    };

    const startRubberBand=(e)=>{
        if(e.target!==canvasRef.current)return;
        const rect=canvasRef.current.getBoundingClientRect();
        const x=(e.clientX-rect.left)/zoom;
        const y=(e.clientY-rect.top)/zoom;
        setSelectedIds([]);
        dragRef.current={
            mode:'rubber',startX:e.clientX,startY:e.clientY,
            handle:'',initEls:[],selectedIds:[],
            rubberStart:{x,y}
        };
        setRubberBand({x,y,w:0,h:0});
    };

    const onMouseMove=useCallback((e)=>{
        const d=dragRef.current;
        if(!d.mode)return;

        const dx=(e.clientX-d.startX)/zoom;
        const dy=(e.clientY-d.startY)/zoom;

        if(d.mode==='move'&&d.selectedIds?.length){
            setElements(d.initEls.map(el=>{
                if(!d.selectedIds.includes(el.id)||el.locked)return el;
                let nx=el.x+dx,ny=el.y+dy;
                if(snapEnabled){nx=snap(nx,gridSize);ny=snap(ny,gridSize);}
                return{...el,x:nx,y:ny};
            }));
        }
        else if(d.mode==='resize'&&d.selectedIds?.length){
            const id=d.selectedIds[0];
            setElements(d.initEls.map(el=>{
                if(el.id!==id)return el;
                let{x,y,w,h}=el;
                const handle=d.handle;
                if(handle.includes('e')){w=Math.max(10,el.w+dx);}
                if(handle.includes('w')){const nw=Math.max(10,el.w-dx);x=el.x+(el.w-nw);w=nw;}
                if(handle.includes('s')){h=Math.max(10,el.h+dy);}
                if(handle.includes('n')){const nh=Math.max(10,el.h-dy);y=el.y+(el.h-nh);h=nh;}
                if(snapEnabled){w=snap(w,gridSize);h=snap(h,gridSize);x=snap(x,gridSize);y=snap(y,gridSize);}
                return{...el,x,y,w,h};
            }));
        }
        else if(d.mode==='rubber'&&d.rubberStart){
            const rect=canvasRef.current.getBoundingClientRect();
            const cx=(e.clientX-rect.left)/zoom;
            const cy=(e.clientY-rect.top)/zoom;
            const rs=d.rubberStart;
            const rx=Math.min(rs.x,cx),ry=Math.min(rs.y,cy);
            const rw=Math.abs(cx-rs.x),rh=Math.abs(cy-rs.y);
            setRubberBand({x:rx,y:ry,w:rw,h:rh});

            const sel=elemRef.current.filter(el=>
                el.x<rx+rw&&el.x+el.w>rx&&el.y<ry+rh&&el.y+el.h>ry
            ).map(el=>el.id);
            setSelectedIds(sel);
        }
    },[zoom,snapEnabled,gridSize]);

    const onMouseUp=useCallback(()=>{
        const d=dragRef.current;
        if(d.mode==='move'||d.mode==='resize'){
            pushHistory(elemRef.current);
        }
        dragRef.current={mode:null,startX:0,startY:0,handle:'',initEls:[],selectedIds:[],rubberStart:null};
        setRubberBand(null);
    },[pushHistory]);

    /* ── Keyboard ── */
    useEffect(()=>{
        const h=(e)=>{
            const tag=document.activeElement?.tagName;
            if(tag==='INPUT'||tag==='TEXTAREA'||tag==='SELECT')return;

            if(e.ctrlKey&&e.key==='z'){e.preventDefault();undo();}
            if(e.ctrlKey&&e.key==='y'){e.preventDefault();redo();}
            if(e.ctrlKey&&e.key==='a'){e.preventDefault();setSelectedIds(elements.map(el=>el.id));}
            if(e.ctrlKey&&e.key==='c'){
                e.preventDefault();
                setClipboard(elements.filter(el=>selectedIds.includes(el.id)));
            }
            if(e.ctrlKey&&e.key==='v'&&clipboard.length){
                e.preventDefault();
                const copies=clipboard.map(el=>({...el,id:uid(),x:el.x+20,y:el.y+20,name:el.name+'_copy'}));
                const next=[...elements,...copies];
                updateEls(next);
                setSelectedIds(copies.map(c=>c.id));
            }
            if(e.ctrlKey&&e.key==='d'&&selectedIds.length){
                e.preventDefault();
                const copies=elements.filter(el=>selectedIds.includes(el.id)).map(el=>({...el,id:uid(),x:el.x+20,y:el.y+20,name:el.name+'_dup'}));
                updateEls([...elements,...copies]);
                setSelectedIds(copies.map(c=>c.id));
            }
            if((e.key==='Delete'||e.key==='Backspace')&&selectedIds.length){
                e.preventDefault();
                updateEls(elements.filter(el=>!selectedIds.includes(el.id)));
                setSelectedIds([]);
            }
            if(selectedIds.length&&['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.key)){
                e.preventDefault();
                const step=e.shiftKey?10:snapEnabled?gridSize:1;
                const next=elements.map(el=>{
                    if(!selectedIds.includes(el.id)||el.locked)return el;
                    let{x,y}=el;
                    if(e.key==='ArrowUp')y-=step;
                    if(e.key==='ArrowDown')y+=step;
                    if(e.key==='ArrowLeft')x-=step;
                    if(e.key==='ArrowRight')x+=step;
                    return{...el,x,y};
                });
                setElements(next);
            }
            if(e.key==='Escape'){setSelectedIds([]);setCtxMenu(null);}
        };
        window.addEventListener('keydown',h);
        return()=>window.removeEventListener('keydown',h);
    },[selectedIds,elements,undo,redo,clipboard,snapEnabled,gridSize,updateEls]);

    // Zoom with wheel
    useEffect(()=>{
        const h=(e)=>{
            if(e.ctrlKey){
                e.preventDefault();
                setZoom(z=>clamp(z+(e.deltaY<0?0.1:-0.1),0.25,3));
            }
        };
        window.addEventListener('wheel',h,{passive:false});
        return()=>window.removeEventListener('wheel',h);
    },[]);

    const primaryEl=elements.find(el=>el.id===selectedIds[0]);

    // Property updater
    const setProp=(key,val)=>{
        setElements(prev=>prev.map(el=>selectedIds.includes(el.id)?{...el,[key]:val}:el));
    };
    const commitHistory=()=>pushHistory(elemRef.current);

    /* ── Widget Preview Renderer ── */
    const renderWidget=(el)=>{
        const s={fontFamily:el.fontFamily||'Segoe UI',fontWeight:el.fontWeight||'normal',fontStyle:el.fontItalic?'italic':'normal',fontSize:el.fontSize?`${el.fontSize}pt`:undefined,color:el.color||undefined,backgroundColor:el.bg||undefined};
        switch(el.type){
            case 'QPushButton':return <div className="w-full h-full flex items-center justify-center" style={{...s,background:el.bg||tw.btnBg,border:`1px solid ${tw.btnBorder}`,borderRadius:4,color:el.color||tw.btnColor,fontSize:el.fontSize?`${el.fontSize}pt`:'11px'}}>{el.text||'Button'}</div>;
            case 'QToolButton':return <div className="w-full h-full flex items-center justify-center" style={{...s,background:el.bg||tw.btnBg,border:`1px solid ${tw.btnBorder}`,borderRadius:4,color:el.color||tw.btnColor,fontSize:el.fontSize?`${el.fontSize}pt`:'11px'}}>{el.text||'...'}</div>;
            case 'QLabel':
                if(el.pixmap){
                    if(el.pixmap.startsWith('http'))return <img src={el.pixmap} className="w-full h-full object-contain" alt=""/>;
                    return <div className="w-full h-full flex items-center justify-center text-[9px]" style={{background:tw.inputBg,color:tw.labelColor}}><Ico name="image" size={20}/></div>;
                }
                return <div className="w-full h-full flex items-center justify-center" style={{...s,color:el.color||tw.labelColor,fontSize:el.fontSize?`${el.fontSize}pt`:'11px'}}>{el.text||'Label'}</div>;
            case 'QImage':
                if(el.pixmap&&el.pixmap.startsWith('http'))return <img src={el.pixmap} className="w-full h-full object-cover" alt=""/>;
                return <div className="w-full h-full flex items-center justify-center text-[9px]" style={{background:tw.inputBg,color:tw.labelColor,border:`1px solid ${tw.inputBorder}`}}><Ico name="image" size={24}/></div>;
            case 'QLineEdit':return <div className="w-full h-full flex items-center px-1" style={{...s,background:el.bg||tw.inputBg,border:`1px solid ${tw.inputBorder}`,borderRadius:3,color:el.color||tw.inputColor,fontSize:el.fontSize?`${el.fontSize}pt`:'11px'}}>{el.text||<span style={{color:tw.checkColor,opacity:0.4}}>{el.placeholderText||''}</span>}</div>;
            case 'QTextEdit':case 'QPlainTextEdit':return <div className="w-full h-full flex items-start p-1 overflow-hidden" style={{...s,background:el.bg||tw.inputBg,border:`1px solid ${tw.inputBorder}`,borderRadius:3,color:el.color||tw.inputColor,fontSize:'10px'}}>{el.text||<span style={{color:tw.checkColor,opacity:0.4}}>{el.placeholderText||''}</span>}</div>;
            case 'QCheckBox':return <div className="w-full h-full flex items-center gap-1" style={{...s,color:el.color||tw.checkColor,fontSize:el.fontSize?`${el.fontSize}pt`:'11px'}}><span style={{fontSize:14}}>{el.checked?'☑':'☐'}</span>{el.text||'CheckBox'}</div>;
            case 'QRadioButton':return <div className="w-full h-full flex items-center gap-1" style={{...s,color:el.color||tw.checkColor,fontSize:el.fontSize?`${el.fontSize}pt`:'11px'}}><span style={{fontSize:14}}>{el.checked?'◉':'○'}</span>{el.text||'RadioButton'}</div>;
            case 'QCommandLinkButton':return <div className="w-full h-full flex items-center px-2 gap-2" style={{...s,background:el.bg||tw.btnBg,border:`1px solid ${tw.btnBorder}`,borderRadius:4,color:el.color||tw.btnColor,fontSize:el.fontSize?`${el.fontSize}pt`:'11px'}}><div style={{width:14,height:14,borderRadius:'50%',background:tw.accent,display:'flex',alignItems:'center',justifyContent:'center',color:'white',fontSize:9}}>➜</div><span style={{fontWeight:'bold'}}>{el.text||'Command Link'}</span></div>;
            case 'QComboBox':return <div className="w-full h-full flex items-center justify-between px-1" style={{background:el.bg||tw.comboBg,border:`1px solid ${tw.comboBorder}`,borderRadius:3,color:el.color||tw.comboColor,fontSize:'11px'}}>{el.items[0]||'ComboBox'}<span style={{fontSize:8}}>▼</span></div>;
            case 'QFontComboBox':return <div className="w-full h-full flex items-center justify-between px-1" style={{background:el.bg||tw.comboBg,border:`1px solid ${tw.comboBorder}`,borderRadius:3,color:el.color||tw.comboColor,fontSize:'11px'}}><span style={{fontFamily:'Segoe UI'}}>Segoe UI</span><span style={{fontSize:8}}>▼</span></div>;
            case 'QKeySequenceEdit':return <div className="w-full h-full flex items-center px-1" style={{...s,background:el.bg||tw.inputBg,border:`1px solid ${tw.inputBorder}`,borderRadius:3,color:el.color||tw.inputColor,fontSize:el.fontSize?`${el.fontSize}pt`:'11px'}}><span style={{color:tw.checkColor,opacity:0.6}}>{el.keySequence||'Ctrl+O'}</span></div>;
            case 'QGroupBox':return <div className="w-full h-full relative" style={{border:`1px solid ${tw.groupBorder}`,borderRadius:4,paddingTop:16}}><span className="absolute left-2" style={{top:-8,background:el.bg||canvasBg,padding:'0 4px',fontSize:11,color:el.color||tw.groupColor}}>{el.text||'Group'}</span></div>;
            case 'QFrame':return <div className="w-full h-full" style={{border:`1px solid ${tw.frameBorder}`,background:el.bg||'transparent'}}/>;
            case 'QScrollArea':return <div className="w-full h-full overflow-hidden relative" style={{border:`1px solid ${tw.frameBorder}`,background:el.bg||tw.inputBg}}><div style={{position:'absolute',right:0,top:0,bottom:0,width:12,background:tw.scrollBg}}/></div>;
            case 'QProgressBar':return <div className="w-full h-full overflow-hidden relative" style={{background:el.bg||tw.progressBg,border:`1px solid ${tw.progressBorder}`,borderRadius:3}}><div style={{height:'100%',width:`${el.value||45}%`,background:tw.progressFill,transition:'width 0.3s'}}/><span style={{position:'absolute',width:'100%',textAlign:'center',fontSize:9,lineHeight:el.h+'px',color:tw.labelColor}}>{el.value||45}%</span></div>;
            case 'QSlider':return <div className="w-full h-full flex items-center relative"><div style={{width:'100%',height:4,background:tw.sliderTrack,borderRadius:2}}/><div style={{position:'absolute',left:`${el.value||45}%`,width:12,height:12,background:tw.sliderThumb,border:`2px solid ${tw.sliderThumbBorder}`,borderRadius:'50%',transform:'translate(-50%,-50%)',top:'50%'}}/></div>;
            case 'QSpinBox':case 'QDoubleSpinBox':return <div className="w-full h-full flex items-center justify-between px-1" style={{background:el.bg||tw.spinBg,border:`1px solid ${tw.spinBorder}`,borderRadius:3,color:el.color||tw.spinColor,fontSize:10}}><span>{el.value||0}</span><span style={{display:'flex',flexDirection:'column',fontSize:7}}>▲▼</span></div>;
            case 'QLCDNumber':return <div className="w-full h-full flex items-center justify-center" style={{background:tw.lcdBg,color:tw.lcdColor,fontFamily:"'Courier New',monospace",fontSize:Math.max(10,el.h*0.6),border:'2px inset #333',letterSpacing:2}}>{el.value||0}</div>;
            case 'QDial':return <div className="w-full h-full" style={{borderRadius:'50%',background:tw.dialBg,border:`2px solid ${tw.dialBorder}`,position:'relative'}}><div style={{content:"''",position:'absolute',top:'50%',left:'50%',width:'40%',height:'40%',background:'radial-gradient(circle,#f0f0f0,#ccc)',borderRadius:'50%',transform:'translate(-50%,-50%)'}}/></div>;
            case 'QCalendarWidget':return <div className="w-full h-full flex flex-col" style={{background:tw.calBg,border:`1px solid ${tw.calBorder}`}}><div style={{background:tw.calHeaderBg,textAlign:'center',padding:2,fontWeight:'bold',borderBottom:`1px solid ${tw.calBorder}`,fontSize:10,color:tw.calColor}}>February 2026</div><div style={{display:'grid',gridTemplateColumns:'repeat(7,1fr)',gap:1,padding:2,flex:1}}>{['M','T','W','T','F','S','S'].map((d,i)=><div key={i} style={{textAlign:'center',padding:1,fontSize:7,fontWeight:'bold',color:tw.calCellColor}}>{d}</div>)}{Array.from({length:28},(_, i)=><div key={i+7} style={{textAlign:'center',padding:1,fontSize:7,color:tw.calCellColor}}>{i+1}</div>)}</div></div>;
            case 'QListWidget':return <div className="w-full h-full overflow-hidden" style={{background:tw.listBg,border:`1px solid ${tw.listBorder}`,fontSize:10,color:tw.listColor}}>{['Item 1','Item 2','Item 3','Item 4'].map((it,i)=><div key={i} style={{padding:'2px 6px',borderBottom:`1px solid ${tw.listItemBorder}`,background:i===0?tw.listSelBg:'transparent',color:i===0?tw.listSelColor:tw.listColor}}>{it}</div>)}</div>;
            case 'QTreeWidget':return <div className="w-full h-full overflow-hidden" style={{background:tw.treeBg,border:`1px solid ${tw.treeBorder}`,fontSize:10,color:tw.treeColor,padding:2}}>{['▸ Parent 1','  ▸ Child 1','  ▸ Child 2','▸ Parent 2'].map((it,i)=><div key={i} style={{padding:'1px 2px'}}>{it}</div>)}</div>;
            case 'QTableWidget':return <div className="w-full h-full flex flex-col overflow-hidden" style={{background:tw.tableBg,border:`1px solid ${tw.tableBorder}`,fontSize:9,color:tw.tableColor}}><div style={{display:'flex',background:tw.tableHeaderBg,borderBottom:`1px solid ${tw.tableBorder}`}}>{(el.columnHeaders||['A','B','C']).map((c,i)=><div key={i} style={{flex:1,padding:'2px 4px',borderRight:`1px solid ${tw.tableBorder}`,fontWeight:'bold'}}>{c}</div>)}</div>{Array.from({length:Math.min(el.rows||3,5)},(_, r)=><div key={r} style={{display:'flex',borderBottom:`1px solid ${tw.listItemBorder}`}}>{(el.columnHeaders||['','','']).map((_, c)=><div key={c} style={{flex:1,padding:'2px 4px',borderRight:`1px solid ${tw.listItemBorder}`}}>&nbsp;</div>)}</div>)}</div>;
            case 'QTabWidget':return <div className="w-full h-full flex flex-col"><div style={{display:'flex',background:tw.tabBarBg,borderBottom:`1px solid ${tw.tabBorder}`}}>{(el.tabs||['Tab 1']).map((t,i)=><div key={i} style={{padding:'3px 10px',fontSize:10,borderRight:`1px solid ${tw.tabBorder}`,background:i===0?tw.tabActiveBg:'transparent',color:tw.tabColor,borderBottom:i===0?`1px solid ${tw.tabActiveBg}`:'none',marginBottom:i===0?-1:0,cursor:'default'}}>{t}</div>)}</div><div style={{flex:1,background:tw.tabActiveBg,border:`1px solid ${tw.tabBorder}`,borderTop:'none'}}/></div>;
            case 'QStackedWidget':return <div className="w-full h-full flex items-center justify-center text-[9px]" style={{border:`1px solid ${tw.frameBorder}`,color:tw.labelColor,background:el.bg||'transparent'}}>{(el.pages||['Page 1'])[0]}</div>;
            case 'QToolBox':return <div className="w-full h-full flex flex-col">{(el.pages||['Section 1']).map((p,i)=><div key={i} style={{background:tw.tabBarBg,border:`1px solid ${tw.tabBorder}`,padding:'2px 6px',fontSize:10,fontWeight:'bold',color:tw.tabColor}}>{p}</div>)}<div style={{flex:1,background:tw.tabActiveBg,border:`1px solid ${tw.tabBorder}`,borderTop:'none'}}/></div>;
            case 'QDateEdit':return <div className="w-full h-full flex items-center justify-between px-1.5" style={{background:tw.dateBg,border:`1px solid ${tw.dateBorder}`,borderRadius:3,fontSize:10,color:tw.dateColor}}>2026-02-18 <span style={{fontSize:8}}>📅</span></div>;
            case 'QTimeEdit':return <div className="w-full h-full flex items-center px-1.5" style={{background:tw.dateBg,border:`1px solid ${tw.dateBorder}`,borderRadius:3,fontSize:10,color:tw.dateColor}}>12:00</div>;
            case 'QDateTimeEdit':return <div className="w-full h-full flex items-center px-1.5" style={{background:tw.dateBg,border:`1px solid ${tw.dateBorder}`,borderRadius:3,fontSize:10,color:tw.dateColor}}>2026-02-18 12:00</div>;
            case 'QScrollBar':return <div className="w-full h-full rounded" style={{background:tw.scrollBg,border:`1px solid ${tw.frameBorder}`}}><div style={{width:el.orientation==='horizontal'?'30%':'100%',height:el.orientation==='horizontal'?'100%':'30%',background:tw.sliderThumb,borderRadius:3,opacity:0.6}}/></div>;
            case 'VLine':return <div style={{width:1,height:'100%',background:tw.frameBorder,margin:'0 auto'}}/>;
            case 'HLine':return <div style={{height:1,width:'100%',background:tw.frameBorder,margin:'auto 0'}}/>;
            default:return <div className="w-full h-full flex items-center justify-center text-[9px]" style={{color:tw.labelColor}}>{el.type}</div>;
        }
    };

    /* ── Context Menu ── */
    const showCtx=(e,id)=>{
        e.preventDefault();e.stopPropagation();
        setSelectedIds(prev=>prev.includes(id)?prev:[id]);
        setCtxMenu({x:e.clientX,y:e.clientY,id});
    };

    /* ── Filtered Widgets ── */
    const filteredWidgets=useMemo(()=>{
        if(!widgetSearch)return null;
        const q=widgetSearch.toLowerCase();
        return Object.entries(W).filter(([k,v])=>k.toLowerCase().includes(q)||v.label.toLowerCase().includes(q));
    },[widgetSearch]);

    /* ── Render ── */
    return(
        <div className="flex h-screen w-screen flex-col overflow-hidden select-none" style={{background:'var(--bg)',color:'var(--text)'}} onMouseMove={onMouseMove} onMouseUp={onMouseUp} onClick={()=>setCtxMenu(null)}>

            {/* ═══ TOOLBAR ═══ */}
            <div className="h-12 shrink-0 flex items-center justify-between px-3 border-b" style={{background:'var(--bg2)',borderColor:'var(--border)'}}>
                <div className="flex items-center gap-2">
                    <div className="flex items-center gap-2 mr-3">
                        <div className="w-7 h-7 rounded-md flex items-center justify-center text-white font-bold text-xs" style={{background:'var(--accent)'}}>Qt</div>
                        <span className="text-xs font-bold" style={{color:'var(--text2)'}}>Designer Pro</span>
                    </div>
                    <div className="toolbar-sep"/>

                    <button onClick={()=>bridge?.import_ui_file()} className="toolbar-btn" title="Open .ui"><Ico name="folder-open" size={16}/></button>
                    <button onClick={()=>bridge?.save_ui_file(generateXML())} className="toolbar-btn" title="Save .ui"><Ico name="save" size={16}/></button>
                    <button onClick={()=>bridge?.save_python_file(generatePython())} className="toolbar-btn" title="Export .py"><Ico name="file-code" size={16}/></button>
                    <div className="toolbar-sep"/>

                    <button onClick={undo} className="toolbar-btn" title="Undo (Ctrl+Z)"><Ico name="undo-2" size={16}/></button>
                    <button onClick={redo} className="toolbar-btn" title="Redo (Ctrl+Y)"><Ico name="redo-2" size={16}/></button>
                    <div className="toolbar-sep"/>

                    <button onClick={()=>{if(selectedIds.length){setClipboard(elements.filter(el=>selectedIds.includes(el.id)));}}} className="toolbar-btn" title="Copy (Ctrl+C)"><Ico name="copy" size={16}/></button>
                    <button onClick={()=>{if(clipboard.length){const c=clipboard.map(el=>({...el,id:uid(),x:el.x+20,y:el.y+20,name:el.name+'_p'}));updateEls([...elements,...c]);setSelectedIds(c.map(x=>x.id));}}} className="toolbar-btn" title="Paste (Ctrl+V)"><Ico name="clipboard-paste" size={16}/></button>
                    <div className="toolbar-sep"/>

                    <button onClick={()=>setSnapEnabled(!snapEnabled)} className={`toolbar-btn ${snapEnabled?'active':''}`} title="Snap to Grid"><Ico name="grid-3x3" size={16}/></button>
                    <div className="toolbar-sep"/>
                    <div className="flex items-center gap-1 px-1 py-0.5 rounded-md" style={{background:'var(--bg)'}}>
                        {Object.entries(THEMES).map(([key,t])=>(
                            <button key={key} onClick={()=>applyTheme(key)}
                                className="rounded transition-all"
                                style={{width:18,height:18,background:t.swatch,border:activeTheme===key?'2px solid var(--accent)':'2px solid transparent',transform:activeTheme===key?'scale(1.15)':'scale(1)',opacity:activeTheme===key?1:0.55}}
                                title={t.name}/>
                        ))}
                    </div>

                    {selectedIds.length>1&&<>
                        <div className="toolbar-sep"/>
                        <button onClick={()=>{const v=Math.min(...elements.filter(e=>selectedIds.includes(e.id)).map(e=>e.x));updateEls(elements.map(e=>selectedIds.includes(e.id)?{...e,x:v}:e));}} className="toolbar-btn" title="Align Left"><Ico name="align-horizontal-justify-start" size={14}/></button>
                        <button onClick={()=>{const els=elements.filter(e=>selectedIds.includes(e.id));const minX=Math.min(...els.map(e=>e.x));const maxX=Math.max(...els.map(e=>e.x+e.w));const cx=minX+(maxX-minX)/2;updateEls(elements.map(e=>selectedIds.includes(e.id)?{...e,x:cx-e.w/2}:e));}} className="toolbar-btn" title="Align Center"><Ico name="align-center-horizontal" size={14}/></button>
                        <button onClick={()=>{const v=Math.max(...elements.filter(e=>selectedIds.includes(e.id)).map(e=>e.x+e.w));updateEls(elements.map(e=>selectedIds.includes(e.id)?{...e,x:v-e.w}:e));}} className="toolbar-btn" title="Align Right"><Ico name="align-horizontal-justify-end" size={14}/></button>
                        <button onClick={()=>{const v=Math.min(...elements.filter(e=>selectedIds.includes(e.id)).map(e=>e.y));updateEls(elements.map(e=>selectedIds.includes(e.id)?{...e,y:v}:e));}} className="toolbar-btn" title="Align Top"><Ico name="align-vertical-justify-start" size={14}/></button>
                        <button onClick={()=>{const v=Math.max(...elements.filter(e=>selectedIds.includes(e.id)).map(e=>e.y+e.h));updateEls(elements.map(e=>selectedIds.includes(e.id)?{...e,y:v-e.h}:e));}} className="toolbar-btn" title="Align Bottom"><Ico name="align-vertical-justify-end" size={14}/></button>
                    </>}
                </div>

                <div className="flex items-center gap-2">
                    <div className="flex rounded-lg p-0.5" style={{background:'var(--bg)'}}>
                        {['design','xml','python'].map(t=>(
                            <button key={t} onClick={()=>setTab(t)} className={`tab-btn ${tab===t?'active':''}`}>{t==='design'?'Design':t==='xml'?'XML':'Python'}</button>
                        ))}
                    </div>
                </div>
            </div>

            <div className="flex flex-1 overflow-hidden">
                {/* ═══ LEFT PANEL ═══ */}
                {tab==='design'&&(
                <div className="w-64 shrink-0 flex flex-col border-r overflow-hidden" style={{background:'var(--bg2)',borderColor:'var(--border)'}}>
                    <div className="flex border-b" style={{borderColor:'var(--border)'}}>
                        <button onClick={()=>setLeftPanel('widgets')} className={`flex-1 py-2 text-[10px] font-bold uppercase tracking-wider border-b-2 transition-colors ${leftPanel==='widgets'?'border-blue-500 text-blue-400':'border-transparent text-zinc-500 hover:text-zinc-300'}`}>Widgets</button>
                        <button onClick={()=>setLeftPanel('tree')} className={`flex-1 py-2 text-[10px] font-bold uppercase tracking-wider border-b-2 transition-colors ${leftPanel==='tree'?'border-blue-500 text-blue-400':'border-transparent text-zinc-500 hover:text-zinc-300'}`}>Objects</button>
                    </div>

                    {leftPanel==='widgets'?(
                    <div className="flex-1 overflow-y-auto scr">
                        <div className="p-3">
                            <div className="relative mb-3">
                                <span className="absolute left-2 top-1/2 -translate-y-1/2" style={{color:'var(--text3)'}}><Ico name="search" size={12}/></span>
                                <input className="search-input" placeholder="Search widgets..." value={widgetSearch} onChange={e=>setWidgetSearch(e.target.value)}/>
                            </div>
                        </div>

                        {filteredWidgets?(
                            <div className="px-3 pb-3 grid grid-cols-3 gap-2">
                                {filteredWidgets.map(([type,cfg])=>(
                                    <div key={type} draggable onDragStart={e=>e.dataTransfer.setData("widgetType",type)} className="widget-card">
                                        <div className="icon-wrap"><Ico name={cfg.icon} size={18}/></div>
                                        <span>{cfg.label}</span>
                                    </div>
                                ))}
                            </div>
                        ):(
                            Object.entries(CATEGORIES).map(([catName,cat])=>(
                                <div key={catName} className="mb-1">
                                    <div className="flex items-center gap-2 px-4 py-2" style={{color:'var(--text3)'}}>
                                        <Ico name={cat.icon} size={12}/>
                                        <span className="text-[10px] font-bold uppercase tracking-wider">{catName}</span>
                                    </div>
                                    <div className="px-3 pb-2 grid grid-cols-3 gap-1.5">
                                        {cat.items.map(type=>{
                                            const cfg=W[type];if(!cfg)return null;
                                            return(
                                                <div key={type} draggable onDragStart={e=>e.dataTransfer.setData("widgetType",type)} className="widget-card">
                                                    <div className="icon-wrap"><Ico name={cfg.icon} size={16}/></div>
                                                    <span>{cfg.label}</span>
                                                </div>
                                            );
                                        })}
                                    </div>
                                </div>
                            ))
                        )}
                    </div>
                    ):(
                    <div className="flex-1 overflow-y-auto scr p-2">
                        {elements.length===0?
                            <div className="text-center py-8" style={{color:'var(--text3)',fontSize:11}}>No widgets yet</div>
                        :
                            elements.map(el=>(
                                <div key={el.id} onClick={()=>setSelectedIds([el.id])} className={`tree-item ${selectedIds.includes(el.id)?'selected':''}`}>
                                    <Ico name={W[el.type]?.icon||'box'} size={12}/>
                                    <span className="flex-1 truncate">{el.name}</span>
                                    <span className="type-badge">{el.type}</span>
                                    {el.locked&&<Ico name="lock" size={10}/>}
                                </div>
                            ))
                        }
                    </div>
                    )}
                </div>
                )}

                {/* ═══ CANVAS ═══ */}
                <div className="flex-1 flex flex-col relative min-w-0">
                    {tab==='design'?(
                    <>
                    <div className="flex-1 overflow-auto scr grid-bg" style={{position:'relative'}}>
                        <div style={{padding:40,display:'inline-block',minWidth:'100%',minHeight:'100%',background:'var(--bg)'}}>
                            <div ref={canvasRef}
                                onDrop={e=>{try{e.preventDefault();const t=e.dataTransfer.getData("widgetType");if(!t||!W[t])return;const r=canvasRef.current.getBoundingClientRect();addWidget(t,(e.clientX-r.left)/zoom,(e.clientY-r.top)/zoom);}catch(err){console.error(err);}}}
                                onDragOver={e=>e.preventDefault()}
                                onMouseDown={startRubberBand}
                                className="relative shadow-2xl"
                                style={{width:canvasSize.w,height:canvasSize.h,backgroundColor:canvasBg,transform:`scale(${zoom})`,transformOrigin:'top left',border:'1px solid var(--border2)',borderRadius:2}}
                                onClick={e=>{if(e.target===canvasRef.current)setSelectedIds([]);}}>

                                {elements.map(el=>{
                                    const sel=selectedIds.includes(el.id);
                                    const isLine=el.type==='VLine'||el.type==='HLine';
                                    return(
                                        <div key={el.id}
                                            onMouseDown={e=>startMove(e,el.id)}
                                            onClick={e=>e.stopPropagation()}
                                            onContextMenu={e=>showCtx(e,el.id)}
                                            className="absolute"
                                            style={{left:el.x,top:el.y,width:el.w,height:el.h,zIndex:el.zIndex,opacity:el.visible?1:0.35,outline:sel?'2px solid var(--accent)':'none',outlineOffset:-1,cursor:el.locked?'not-allowed':'move',boxShadow:isLine?'none':sel?'0 0 0 1px var(--accent), 0 2px 8px rgba(0,0,0,0.25)':'0 1px 3px rgba(0,0,0,0.2), 0 0 0 1px rgba(128,128,128,0.12)',borderRadius:isLine?0:2}}>

                                            <div className="w-full h-full overflow-hidden pointer-events-none">
                                                {renderWidget(el)}
                                            </div>

                                            {sel&&!el.locked&&<>
                                                <div onMouseDown={e=>startResize(e,el.id,'n')} className="resize-handle rh-n"/>
                                                <div onMouseDown={e=>startResize(e,el.id,'s')} className="resize-handle rh-s"/>
                                                <div onMouseDown={e=>startResize(e,el.id,'w')} className="resize-handle rh-w"/>
                                                <div onMouseDown={e=>startResize(e,el.id,'e')} className="resize-handle rh-e"/>
                                                <div onMouseDown={e=>startResize(e,el.id,'nw')} className="resize-handle rh-nw"/>
                                                <div onMouseDown={e=>startResize(e,el.id,'ne')} className="resize-handle rh-ne"/>
                                                <div onMouseDown={e=>startResize(e,el.id,'sw')} className="resize-handle rh-sw"/>
                                                <div onMouseDown={e=>startResize(e,el.id,'se')} className="resize-handle rh-se"/>
                                                <div className="absolute -top-5 left-0 text-[8px] px-1 rounded whitespace-nowrap" style={{background:'var(--accent)',color:'white'}}>{el.name} — {Math.round(el.w)}×{Math.round(el.h)}</div>
                                            </>}
                                        </div>
                                    );
                                })}

                                {rubberBand&&<div className="rubber-band" style={{left:rubberBand.x,top:rubberBand.y,width:rubberBand.w,height:rubberBand.h}}/>}
                            </div>
                        </div>
                    </div>

                    {/* Status Bar */}
                    <div className="h-7 shrink-0 flex items-center px-4 text-[10px] justify-between border-t" style={{background:'var(--bg2)',borderColor:'var(--border)',color:'var(--text3)'}}>
                        <div className="flex gap-4">
                            <span>Widgets: {elements.length}</span>
                            <span>Selected: {selectedIds.length}</span>
                            {primaryEl&&<span>{primaryEl.name} @ ({Math.round(primaryEl.x)}, {Math.round(primaryEl.y)})</span>}
                        </div>
                        <div className="flex items-center gap-3">
                            <span>Grid: {gridSize}px</span>
                            <span>Zoom: {Math.round(zoom*100)}%</span>
                            <input type="range" min="25" max="300" step="5" value={zoom*100} onChange={e=>setZoom(parseInt(e.target.value)/100)} className="w-20 accent-blue-500" style={{height:3}}/>
                            <span>{canvasSize.w}×{canvasSize.h}</span>
                        </div>
                    </div>
                    </>
                    ):tab==='xml'?(
                    <div className="flex-1 overflow-auto scr p-6" style={{background:'var(--bg)'}}>
                        <pre className="code-view">{generateXML()}</pre>
                    </div>
                    ):(
                    <div className="flex-1 overflow-auto scr p-6" style={{background:'var(--bg)'}}>
                        <pre className="code-view">{generatePython()}</pre>
                    </div>
                    )}
                </div>

                {/* ═══ RIGHT PANEL — PROPERTIES ═══ */}
                {tab==='design'&&(
                <div className="w-72 shrink-0 flex flex-col border-l overflow-hidden" style={{background:'var(--bg2)',borderColor:'var(--border)'}}>
                    <div className="py-2 px-4 border-b flex items-center gap-2" style={{borderColor:'var(--border)'}}>
                        <Ico name="settings-2" size={12}/>
                        <span className="text-[10px] font-bold uppercase tracking-wider" style={{color:'var(--text3)'}}>Properties</span>
                    </div>
                    <div className="flex-1 overflow-y-auto scr">
                        {primaryEl?(
                        <>
                        {/* Identity */}
                        <div className="panel-section">
                            <span className="panel-label">Identity</span>
                            <div className="prop-row"><span className="text-[9px] font-bold min-w-[40px]" style={{color:'var(--text3)'}}>Name</span><input className="prop-input font-mono text-blue-400" value={primaryEl.name} onChange={e=>setProp('name',e.target.value)} onBlur={commitHistory}/></div>
                            <div className="prop-row"><span className="text-[9px] font-bold min-w-[40px]" style={{color:'var(--text3)'}}>Type</span><span className="text-[10px] font-mono" style={{color:'var(--text3)'}}>{primaryEl.type}</span></div>
                        </div>

                        {/* Geometry */}
                        <div className="panel-section">
                            <span className="panel-label">Geometry</span>
                            <div className="grid grid-cols-2 gap-2">
                                {[['X','x'],['Y','y'],['W','w'],['H','h']].map(([l,k])=>(
                                    <div key={k} className="geo-box">
                                        <span className="geo-label">{l}</span>
                                        <input type="number" className="prop-input-sm" value={Math.round(primaryEl[k])} onChange={e=>setProp(k,parseInt(e.target.value)||0)} onBlur={commitHistory}/>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Typography */}
                        <div className="panel-section">
                            <span className="panel-label">Typography</span>
                            <select className="prop-select mb-2" value={primaryEl.fontFamily} onChange={e=>{setProp('fontFamily',e.target.value);commitHistory();}}>
                                <option value="">Default</option>
                                {FONT_FAMILIES.map(f=><option key={f} value={f}>{f}</option>)}
                            </select>
                            <div className="flex gap-2 items-center">
                                <input type="number" className="prop-input-sm" placeholder="Size" value={primaryEl.fontSize||''} onChange={e=>setProp('fontSize',parseInt(e.target.value)||0)} onBlur={commitHistory}/>
                                <button onClick={()=>{setProp('fontWeight',primaryEl.fontWeight==='bold'?'normal':'bold');commitHistory();}} className={`toggle-btn ${primaryEl.fontWeight==='bold'?'active':''}`} style={{fontWeight:'bold'}}>B</button>
                                <button onClick={()=>{setProp('fontItalic',!primaryEl.fontItalic);commitHistory();}} className={`toggle-btn ${primaryEl.fontItalic?'active':''}`} style={{fontStyle:'italic'}}>I</button>
                            </div>
                        </div>

                        {/* Alignment — only for widgets that support setAlignment */}
                        {(['QLabel','QLineEdit','QImage','QProgressBar','QSpinBox','QDoubleSpinBox','QDateEdit','QTimeEdit','QDateTimeEdit'].includes(primaryEl.type))&&(
                        <div className="panel-section">
                            <span className="panel-label">Alignment</span>
                            <div className="flex gap-1 p-1 rounded-md mb-2" style={{background:'var(--bg)'}}>
                                {[['left','align-left'],['center','align-center'],['right','align-right'],['justify','align-justify']].map(([v,ic])=>(
                                    <button key={v} onClick={()=>{setProp('hAlign',v);commitHistory();}} className={`align-btn ${primaryEl.hAlign===v?'active':''}`}><Ico name={ic} size={13}/></button>
                                ))}
                            </div>
                            <div className="flex gap-1 p-1 rounded-md" style={{background:'var(--bg)'}}>
                                {[['top','align-vertical-justify-start'],['center','align-vertical-justify-center'],['bottom','align-vertical-justify-end']].map(([v,ic])=>(
                                    <button key={v} onClick={()=>{setProp('vAlign',v);commitHistory();}} className={`align-btn ${primaryEl.vAlign===v?'active':''}`}><Ico name={ic} size={13}/></button>
                                ))}
                            </div>
                        </div>
                        )}

                        {/* Content */}
                        <div className="panel-section">
                            <span className="panel-label">Content</span>
                            {primaryEl.type==='QComboBox'?
                                <><span className="text-[9px] font-bold mb-1 block" style={{color:'var(--text3)'}}>Items (one per line)</span><textarea className="prop-input" rows={4} style={{resize:'none'}} value={primaryEl.items.join('\n')} onChange={e=>setProp('items',e.target.value.split('\n'))} onBlur={commitHistory}/></>
                            :primaryEl.type==='QTabWidget'?
                                <><span className="text-[9px] font-bold mb-1 block" style={{color:'var(--text3)'}}>Tabs (one per line)</span><textarea className="prop-input" rows={3} style={{resize:'none'}} value={primaryEl.tabs.join('\n')} onChange={e=>setProp('tabs',e.target.value.split('\n'))} onBlur={commitHistory}/></>
                            :(primaryEl.type==='QStackedWidget'||primaryEl.type==='QToolBox')?
                                <><span className="text-[9px] font-bold mb-1 block" style={{color:'var(--text3)'}}>Pages (one per line)</span><textarea className="prop-input" rows={3} style={{resize:'none'}} value={primaryEl.pages.join('\n')} onChange={e=>setProp('pages',e.target.value.split('\n'))} onBlur={commitHistory}/></>
                            :primaryEl.type==='QKeySequenceEdit'?
                                <><span className="text-[9px] font-bold mb-1 block" style={{color:'var(--text3)'}}>Key Sequence</span><input className="prop-input" value={primaryEl.keySequence} onChange={e=>setProp('keySequence',e.target.value)} onBlur={commitHistory}/></>
                            :(['QPushButton','QToolButton','QCommandLinkButton','QLabel','QLineEdit','QTextEdit','QPlainTextEdit','QTextBrowser','QCheckBox','QRadioButton','QGroupBox','QImage'].includes(primaryEl.type))?
                                <textarea className="prop-input" rows={2} style={{resize:'none'}} placeholder={primaryEl.type==='QGroupBox'?'Title':'Text'} value={primaryEl.text} onChange={e=>setProp('text',e.target.value)} onBlur={commitHistory}/>
                            :
                                <span className="text-[9px]" style={{color:'var(--text3)'}}>No text property</span>
                            }
                            {(primaryEl.type==='QLabel'||primaryEl.type==='QImage')&&
                                <input className="prop-input mt-2" placeholder="Pixmap URL or path" value={primaryEl.pixmap} onChange={e=>setProp('pixmap',e.target.value)} onBlur={commitHistory}/>
                            }
                        </div>

                        {/* Colors */}
                        <div className="panel-section">
                            <span className="panel-label">Colors</span>
                            <div className="flex gap-3">
                                <div><span className="text-[9px] font-bold mb-1 block" style={{color:'var(--text3)'}}>Text</span><div className="prop-color" style={{backgroundColor:primaryEl.color||'#000'}}><input type="color" value={primaryEl.color||'#000000'} onChange={e=>setProp('color',e.target.value)}/></div></div>
                                <div><span className="text-[9px] font-bold mb-1 block" style={{color:'var(--text3)'}}>Bg</span><div className="prop-color" style={{backgroundColor:primaryEl.bg||'#fff'}}><input type="color" value={primaryEl.bg||'#ffffff'} onChange={e=>setProp('bg',e.target.value)}/></div></div>
                            </div>
                        </div>

                        {/* Value (for progress/slider/spin/lcd) */}
                        {(primaryEl.type==='QProgressBar'||primaryEl.type==='QSlider'||primaryEl.type==='QSpinBox'||primaryEl.type==='QDoubleSpinBox'||primaryEl.type==='QLCDNumber')&&(
                        <div className="panel-section">
                            <span className="panel-label">Value</span>
                            <div className="grid grid-cols-3 gap-2">
                                <div className="geo-box"><span className="geo-label">Val</span><input type="number" className="prop-input-sm" value={primaryEl.value} onChange={e=>setProp('value',parseFloat(e.target.value)||0)} onBlur={commitHistory}/></div>
                                {primaryEl.type!=='QLCDNumber'&&<>
                                    <div className="geo-box"><span className="geo-label">Min</span><input type="number" className="prop-input-sm" value={primaryEl.minimum} onChange={e=>setProp('minimum',parseFloat(e.target.value)||0)} onBlur={commitHistory}/></div>
                                    <div className="geo-box"><span className="geo-label">Max</span><input type="number" className="prop-input-sm" value={primaryEl.maximum} onChange={e=>setProp('maximum',parseFloat(e.target.value)||0)} onBlur={commitHistory}/></div>
                                </>}
                            </div>
                        </div>
                        )}

                        {/* Table properties */}
                        {primaryEl.type==='QTableWidget'&&(
                        <div className="panel-section">
                            <span className="panel-label">Table</span>
                            <div className="grid grid-cols-2 gap-2 mb-2">
                                <div className="geo-box"><span className="geo-label">Rows</span><input type="number" className="prop-input-sm" value={primaryEl.rows} onChange={e=>setProp('rows',parseInt(e.target.value)||0)} onBlur={commitHistory}/></div>
                                <div className="geo-box"><span className="geo-label">Cols</span><input type="number" className="prop-input-sm" value={primaryEl.columns} onChange={e=>setProp('columns',parseInt(e.target.value)||0)} onBlur={commitHistory}/></div>
                            </div>
                            <span className="text-[9px] font-bold mb-1 block" style={{color:'var(--text3)'}}>Column headers (one per line)</span>
                            <textarea className="prop-input" rows={3} style={{resize:'none'}} value={primaryEl.columnHeaders.join('\n')} onChange={e=>setProp('columnHeaders',e.target.value.split('\n'))} onBlur={commitHistory}/>
                        </div>
                        )}

                        {/* Settings */}
                        <div className="panel-section">
                            <span className="panel-label">Settings</span>
                            <div className="space-y-2">
                                <select className="prop-select" value={primaryEl.cursor} onChange={e=>{setProp('cursor',e.target.value);commitHistory();}}>
                                    {CURSORS.map(c=><option key={c} value={c}>{c.replace('Cursor','')}</option>)}
                                </select>
                                {(['QLineEdit','QTextEdit','QPlainTextEdit'].includes(primaryEl.type))&&<>
                                    <input className="prop-input" placeholder="Placeholder text" value={primaryEl.placeholderText} onChange={e=>setProp('placeholderText',e.target.value)} onBlur={commitHistory}/>
                                    <label className="prop-check"><input type="checkbox" checked={primaryEl.readOnly} onChange={e=>{setProp('readOnly',e.target.checked);commitHistory();}}/>Read Only</label>
                                </>}
                                {(['QPushButton','QGroupBox'].includes(primaryEl.type))&&
                                    <label className="prop-check"><input type="checkbox" checked={primaryEl.flat} onChange={e=>{setProp('flat',e.target.checked);commitHistory();}}/>Flat</label>
                                }
                                {(['QPushButton','QToolButton','QGroupBox'].includes(primaryEl.type))&&
                                    <label className="prop-check"><input type="checkbox" checked={primaryEl.checkable} onChange={e=>{setProp('checkable',e.target.checked);commitHistory();}}/>Checkable</label>
                                }
                                {(['QPushButton','QToolButton','QCheckBox','QRadioButton','QGroupBox'].includes(primaryEl.type))&&
                                    <label className="prop-check"><input type="checkbox" checked={primaryEl.checked} onChange={e=>{setProp('checked',e.target.checked);commitHistory();}}/>Checked</label>
                                }
                                <label className="prop-check"><input type="checkbox" checked={!primaryEl.enabled} onChange={e=>{setProp('enabled',!e.target.checked);commitHistory();}}/>Disabled</label>
                                <label className="prop-check"><input type="checkbox" checked={!primaryEl.visible} onChange={e=>{setProp('visible',!e.target.checked);commitHistory();}}/>Hidden</label>
                                <label className="prop-check"><input type="checkbox" checked={primaryEl.locked} onChange={e=>{setProp('locked',e.target.checked);commitHistory();}}/>Locked</label>
                            </div>
                        </div>

                        {/* Size Policy */}
                        <div className="panel-section">
                            <span className="panel-label">Size Policy</span>
                            <div className="grid grid-cols-2 gap-2 mb-2">
                                <div><span className="text-[9px] font-bold mb-1 block" style={{color:'var(--text3)'}}>Horizontal</span><select className="prop-select" value={primaryEl.sizeH} onChange={e=>{setProp('sizeH',e.target.value);commitHistory();}}>{SIZE_POLICIES.map(p=><option key={p}>{p}</option>)}</select></div>
                                <div><span className="text-[9px] font-bold mb-1 block" style={{color:'var(--text3)'}}>Vertical</span><select className="prop-select" value={primaryEl.sizeV} onChange={e=>{setProp('sizeV',e.target.value);commitHistory();}}>{SIZE_POLICIES.map(p=><option key={p}>{p}</option>)}</select></div>
                            </div>
                            <div className="grid grid-cols-2 gap-2">
                                <div className="geo-box"><span className="geo-label text-[8px]">MinW</span><input type="number" className="prop-input-sm" value={primaryEl.minW} onChange={e=>setProp('minW',parseInt(e.target.value)||0)} onBlur={commitHistory}/></div>
                                <div className="geo-box"><span className="geo-label text-[8px]">MinH</span><input type="number" className="prop-input-sm" value={primaryEl.minH} onChange={e=>setProp('minH',parseInt(e.target.value)||0)} onBlur={commitHistory}/></div>
                            </div>
                        </div>

                        {/* Custom StyleSheet */}
                        <div className="panel-section">
                            <span className="panel-label">Custom StyleSheet</span>
                            <textarea className="prop-input font-mono text-[10px]" rows={3} style={{resize:'vertical'}} placeholder="border-radius: 8px; ..." value={primaryEl.styleSheet} onChange={e=>setProp('styleSheet',e.target.value)} onBlur={commitHistory}/>
                        </div>

                        {/* Tooltip */}
                        <div className="panel-section">
                            <span className="panel-label">Tooltip</span>
                            <input className="prop-input" placeholder="Tooltip text" value={primaryEl.tooltip} onChange={e=>setProp('tooltip',e.target.value)} onBlur={commitHistory}/>
                        </div>

                        {/* Z-Index */}
                        <div className="panel-section">
                            <span className="panel-label">Z-Order</span>
                            <div className="flex gap-2">
                                <button onClick={()=>{const mx=Math.max(...elements.map(e=>e.zIndex),0);setProp('zIndex',mx+1);commitHistory();}} className="toggle-btn flex-1" style={{fontSize:10}}>Bring Front</button>
                                <button onClick={()=>{setProp('zIndex',0);commitHistory();}} className="toggle-btn flex-1" style={{fontSize:10}}>Send Back</button>
                            </div>
                        </div>

                        {/* Delete */}
                        <div className="panel-section">
                            <button onClick={()=>{updateEls(elements.filter(el=>!selectedIds.includes(el.id)));setSelectedIds([]);}} className="w-full py-2 rounded-md text-[11px] font-bold flex items-center justify-center gap-2 transition-colors" style={{background:'rgba(239,68,68,0.1)',color:'var(--red)',border:'1px solid rgba(239,68,68,0.2)'}}><Ico name="trash-2" size={13}/>Delete Widget{selectedIds.length>1?'s':''}</button>
                        </div>
                        </>
                        ):(
                        /* No selection — Canvas properties */
                        <div>
                            <div className="panel-section">
                                <span className="panel-label">Window</span>
                                <input className="prop-input mb-2" placeholder="Window Title" value={windowTitle} onChange={e=>setWindowTitle(e.target.value)}/>
                                <div className="grid grid-cols-2 gap-2 mb-2">
                                    <div className="geo-box"><span className="geo-label">W</span><input type="number" className="prop-input-sm" value={canvasSize.w} onChange={e=>setCanvasSize(p=>({...p,w:parseInt(e.target.value)||400}))}/></div>
                                    <div className="geo-box"><span className="geo-label">H</span><input type="number" className="prop-input-sm" value={canvasSize.h} onChange={e=>setCanvasSize(p=>({...p,h:parseInt(e.target.value)||300}))}/></div>
                                </div>
                            </div>
                            <div className="panel-section">
                                <span className="panel-label">Theme</span>
                                <div className="flex gap-2 flex-wrap">
                                    {Object.entries(THEMES).map(([key,t])=>(
                                        <button key={key} onClick={()=>applyTheme(key)}
                                            className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-md transition-all text-[10px] font-semibold"
                                            style={{background:activeTheme===key?'var(--accent-glow)':'var(--bg)',border:`1px solid ${activeTheme===key?'var(--accent)':'var(--border)'}`,color:activeTheme===key?'var(--accent)':'var(--text3)'}}>
                                            <span style={{width:10,height:10,borderRadius:'50%',background:t.swatch,border:'1px solid var(--border2)',display:'inline-block'}}/>
                                            {t.name}
                                        </button>
                                    ))}
                                </div>
                            </div>
                            <div className="panel-section">
                                <span className="panel-label">Background</span>
                                <div className="flex items-center gap-2">
                                    <div className="prop-color" style={{backgroundColor:canvasBg}}><input type="color" value={canvasBg} onChange={e=>setCanvasBg(e.target.value)}/></div>
                                    <span className="font-mono text-[10px]" style={{color:'var(--text3)'}}>{canvasBg}</span>
                                </div>
                            </div>
                            <div className="panel-section">
                                <span className="panel-label">Menu Bar</span>
                                <textarea className="prop-input" rows={2} style={{resize:'none'}} placeholder="File, Edit, View" value={menus.join(', ')} onChange={e=>setMenus(e.target.value.split(',').map(s=>s.trim()).filter(s=>s))}/>
                            </div>
                            <div className="panel-section">
                                <span className="panel-label">Grid</span>
                                <div className="flex items-center gap-2">
                                    <label className="prop-check"><input type="checkbox" checked={snapEnabled} onChange={e=>setSnapEnabled(e.target.checked)}/>Snap to Grid</label>
                                    <input type="number" className="prop-input-sm" min={5} max={50} value={gridSize} onChange={e=>setGridSize(clamp(parseInt(e.target.value)||10,5,50))}/>
                                    <span className="text-[9px]" style={{color:'var(--text3)'}}>px</span>
                                </div>
                            </div>
                            <div className="panel-section">
                                <span className="panel-label">Quick Actions</span>
                                <div className="space-y-2">
                                    <button onClick={()=>{if(confirm('Clear all widgets?')){updateEls([]);setSelectedIds([]);}}} className="w-full py-2 rounded-md text-[10px] font-bold transition-colors" style={{background:'var(--bg)',border:'1px solid var(--border)',color:'var(--text3)'}}>Clear Canvas</button>
                                </div>
                            </div>
                        </div>
                        )}
                    </div>
                </div>
                )}
            </div>

            {/* ═══ CONTEXT MENU ═══ */}
            {ctxMenu&&(
            <div className="ctx-menu" style={{left:ctxMenu.x,top:ctxMenu.y}} onClick={e=>e.stopPropagation()} onMouseLeave={()=>setCtxMenu(null)}>
                <button className="ctx-item" onClick={()=>{const el=elements.find(e=>e.id===ctxMenu.id);if(el){const c={...el,id:uid(),x:el.x+20,y:el.y+20,name:el.name+'_copy'};updateEls([...elements,c]);setSelectedIds([c.id]);}setCtxMenu(null);}}><Ico name="copy" size={12}/>Duplicate</button>
                <button className="ctx-item" onClick={()=>{setClipboard(elements.filter(e=>selectedIds.includes(e.id)));setCtxMenu(null);}}><Ico name="clipboard-copy" size={12}/>Copy</button>
                <div className="ctx-sep"/>
                <button className="ctx-item" onClick={()=>{const mx=Math.max(...elements.map(e=>e.zIndex),0);setElements(elements.map(e=>e.id===ctxMenu.id?{...e,zIndex:mx+1}:e));setCtxMenu(null);}}><Ico name="arrow-up-to-line" size={12}/>Bring to Front</button>
                <button className="ctx-item" onClick={()=>{setElements(elements.map(e=>e.id===ctxMenu.id?{...e,zIndex:0}:e));setCtxMenu(null);}}><Ico name="arrow-down-to-line" size={12}/>Send to Back</button>
                <div className="ctx-sep"/>
                <button className="ctx-item" onClick={()=>{setProp('locked',!primaryEl?.locked);setCtxMenu(null);}}><Ico name={primaryEl?.locked?"unlock":"lock"} size={12}/>{primaryEl?.locked?'Unlock':'Lock'}</button>
                <div className="ctx-sep"/>
                <button className="ctx-item danger" onClick={()=>{updateEls(elements.filter(el=>el.id!==ctxMenu.id));setSelectedIds([]);setCtxMenu(null);}}><Ico name="trash-2" size={12}/>Delete</button>
            </div>
            )}
        </div>
    );
};

const root=ReactDOM.createRoot(document.getElementById('root'));
root.render(<App/>);
</script>
</body>
</html>
"""


class RequestHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress server logs

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML_CONTENT.encode('utf-8'))


def start_server(port=8765):
    server = HTTPServer(('127.0.0.1', port), RequestHandler)
    server.serve_forever()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Designer Pro")
        self.resize(1680, 960)

        self.browser = QWebEngineView()
        self.channel = QWebChannel()
        self.bridge = DesignerBridge()
        self.channel.registerObject('pyBridge', self.bridge)
        self.browser.page().setWebChannel(self.channel)

        self.setCentralWidget(self.browser)
        self.browser.setUrl(QUrl("http://127.0.0.1:8765"))


if __name__ == "__main__":
    PORT = 8765
    threading.Thread(target=start_server, args=(PORT,), daemon=True).start()
    app = QApplication(sys.argv)
    if PYQT_VERSION == 5:
        app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    if PYQT_VERSION == 6:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())

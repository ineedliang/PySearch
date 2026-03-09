"""
Advanced File Search for Windows 10
Supports wildcards, file types, sizes, names, and paths
Requirements: pip install PyQt6
"""

import sys
import os
import json
import fnmatch
import subprocess
import threading
from datetime import datetime
from pathlib import Path

# Settings file lives next to the script
SETTINGS_FILE = Path(sys.argv[0]).resolve().parent / "advanced_search_settings.json"

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QFileDialog, QComboBox, QSpinBox, QCheckBox, QHeaderView,
    QProgressBar, QSplitter, QGroupBox, QGridLayout, QFrame,
    QMenu, QMessageBox, QSizePolicy, QAbstractItemView,
    QDialog, QDialogButtonBox, QRadioButton, QButtonGroup, QTextEdit,
    QListWidget, QListWidgetItem
)
from PyQt6.QtCore import (
    Qt, QThread, pyqtSignal, QTimer, QSize
)
from PyQt6.QtGui import (
    QFont, QColor, QPalette, QIcon, QAction, QCursor
)


# ─────────────────────────────────────────────
#  DARK THEME STYLESHEET
# ─────────────────────────────────────────────
DARK_STYLE = """
QMainWindow, QWidget {
    background-color: #0e1117;
    color: #e2e8f0;
    font-family: 'Consolas', 'Courier New', monospace;
}
QGroupBox {
    border: 1px solid #2d3748;
    border-radius: 6px;
    margin-top: 10px;
    padding-top: 8px;
    font-weight: bold;
    color: #63b3ed;
    font-size: 11px;
    letter-spacing: 1px;
    text-transform: uppercase;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
}
QLineEdit, QComboBox, QSpinBox {
    background-color: #1a202c;
    border: 1px solid #2d3748;
    border-radius: 4px;
    padding: 6px 10px;
    color: #e2e8f0;
    font-size: 12px;
    selection-background-color: #3182ce;
}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
    border: 1px solid #4299e1;
    background-color: #1e2733;
}
QLineEdit::placeholder {
    color: #4a5568;
}
QPushButton {
    background-color: #1a202c;
    border: 1px solid #3182ce;
    border-radius: 4px;
    padding: 7px 18px;
    color: #63b3ed;
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 0.5px;
}
QPushButton:hover {
    background-color: #2b4a7a;
    border-color: #63b3ed;
    color: #bee3f8;
}
QPushButton:pressed {
    background-color: #1a365d;
}
QPushButton#searchBtn {
    background-color: #2b6cb0;
    border: 1px solid #4299e1;
    color: #ebf8ff;
    padding: 8px 28px;
    font-size: 13px;
}
QPushButton#searchBtn:hover {
    background-color: #3182ce;
}
QPushButton#stopBtn {
    background-color: #742a2a;
    border: 1px solid #fc8181;
    color: #fed7d7;
}
QPushButton#stopBtn:hover {
    background-color: #9b2c2c;
}
QPushButton#clearBtn {
    border-color: #4a5568;
    color: #a0aec0;
}
QPushButton#clearBtn:hover {
    border-color: #718096;
    color: #e2e8f0;
}
QTableWidget {
    background-color: #0e1117;
    alternate-background-color: #141921;
    border: 1px solid #2d3748;
    border-radius: 4px;
    gridline-color: #1a202c;
    font-size: 12px;
    selection-background-color: #1e3a5f;
    selection-color: #bee3f8;
}
QTableWidget::item {
    padding: 5px 8px;
    border-bottom: 1px solid #1a202c;
}
QTableWidget::item:hover {
    background-color: #1a2535;
}
QHeaderView::section {
    background-color: #141921;
    color: #63b3ed;
    border: none;
    border-right: 1px solid #2d3748;
    border-bottom: 1px solid #2d3748;
    padding: 7px 10px;
    font-weight: bold;
    font-size: 11px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
QHeaderView::section:hover {
    background-color: #1a2535;
}
QProgressBar {
    background-color: #1a202c;
    border: 1px solid #2d3748;
    border-radius: 3px;
    height: 6px;
    text-align: center;
    color: transparent;
}
QProgressBar::chunk {
    background-color: #3182ce;
    border-radius: 3px;
}
QScrollBar:vertical {
    background-color: #0e1117;
    width: 10px;
    border: none;
}
QScrollBar::handle:vertical {
    background-color: #2d3748;
    border-radius: 5px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover {
    background-color: #4a5568;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
QScrollBar:horizontal {
    background-color: #0e1117;
    height: 10px;
    border: none;
}
QScrollBar::handle:horizontal {
    background-color: #2d3748;
    border-radius: 5px;
    min-width: 20px;
}
QScrollBar::handle:horizontal:hover {
    background-color: #4a5568;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}
QComboBox::drop-down {
    border: none;
    padding-right: 8px;
}
QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #63b3ed;
    margin-right: 6px;
}
QComboBox QAbstractItemView {
    background-color: #1a202c;
    border: 1px solid #3182ce;
    selection-background-color: #2b4a7a;
    color: #e2e8f0;
}
QCheckBox {
    color: #a0aec0;
    spacing: 6px;
}
QCheckBox::indicator {
    width: 14px;
    height: 14px;
    border: 1px solid #4a5568;
    border-radius: 3px;
    background-color: #1a202c;
}
QCheckBox::indicator:checked {
    background-color: #3182ce;
    border-color: #4299e1;
}
QLabel#statusLabel {
    color: #4a5568;
    font-size: 11px;
    padding: 2px 0;
}
QLabel#resultCount {
    color: #68d391;
    font-size: 12px;
    font-weight: bold;
}
QFrame#separator {
    background-color: #2d3748;
    max-height: 1px;
}
QMenu {
    background-color: #1a202c;
    border: 1px solid #2d3748;
    color: #e2e8f0;
    padding: 4px;
}
QMenu::item {
    padding: 6px 20px;
    border-radius: 3px;
}
QMenu::item:selected {
    background-color: #2b4a7a;
    color: #bee3f8;
}
QSplitter::handle {
    background-color: #2d3748;
}
QToolTip {
    background-color: #1a202c;
    border: 1px solid #2d3748;
    color: #e2e8f0;
    padding: 4px 8px;
}
"""


# ─────────────────────────────────────────────
#  NUMERIC SORT ITEM  (for file size column)
# ─────────────────────────────────────────────
class NumericSortItem(QTableWidgetItem):
    """QTableWidgetItem that sorts by a numeric value stored in UserRole."""
    def __lt__(self, other):
        self_val  = self.data(Qt.ItemDataRole.UserRole)
        other_val = other.data(Qt.ItemDataRole.UserRole)
        try:
            return float(self_val) < float(other_val)
        except (TypeError, ValueError):
            return super().__lt__(other)


# ─────────────────────────────────────────────
#  SEARCH WORKER THREAD
# ─────────────────────────────────────────────
class SearchWorker(QThread):
    result_found = pyqtSignal(dict)
    progress_update = pyqtSignal(str)
    search_done = pyqtSignal(int)
    error_signal = pyqtSignal(str)

    def __init__(self, params):
        super().__init__()
        self.params = params
        self._stop_flag = False

    def stop(self):
        self._stop_flag = True

    def run(self):
        p = self.params
        root = p["root"]
        name_pattern = p["name_pattern"].strip()
        ext_filter = p["ext_filter"].strip().lower()
        min_size = p["min_size"]   # bytes, -1 = ignore
        max_size = p["max_size"]   # bytes, -1 = ignore
        path_contains = p["path_contains"].strip().lower()
        exclude_raw = p.get("exclude_patterns", "").strip()
        exclude_patterns = [e.strip() for e in exclude_raw.split(",") if e.strip()]
        excl_folder_raw = p.get("exclude_folders", "").strip()
        exclude_folders = [f.strip() for f in excl_folder_raw.split(",") if f.strip()]
        case_sensitive = p["case_sensitive"]
        include_hidden = p["include_hidden"]
        search_subdirs = p["search_subdirs"]

        count = 0

        # Build effective name pattern
        if not name_pattern:
            name_pattern = "*"

        try:
            walker = os.walk(root)
        except PermissionError as e:
            self.error_signal.emit(str(e))
            self.search_done.emit(0)
            return

        for dirpath, dirnames, filenames in walker:
            if self._stop_flag:
                break

            # Skip hidden dirs unless requested
            if not include_hidden:
                dirnames[:] = [d for d in dirnames if not d.startswith('.')]

            # Prune excluded folders (wildcards supported) — prevents descending into them
            if exclude_folders:
                def folder_excluded(d):
                    d_check = d if case_sensitive else d.lower()
                    for pat in exclude_folders:
                        p_check = pat if case_sensitive else pat.lower()
                        if fnmatch.fnmatch(d_check, p_check) or d_check == p_check:
                            return True
                    return False
                dirnames[:] = [d for d in dirnames if not folder_excluded(d)]

            if not search_subdirs:
                dirnames.clear()

            self.progress_update.emit(f"Scanning: {dirpath[:80]}...")

            for filename in filenames:
                if self._stop_flag:
                    break

                # Skip hidden files
                if not include_hidden and filename.startswith('.'):
                    continue

                full_path = os.path.join(dirpath, filename)

                # ── Name pattern match (wildcards) ──
                fn_check = filename if case_sensitive else filename.lower()
                pat_check = name_pattern if case_sensitive else name_pattern.lower()
                if not fnmatch.fnmatch(fn_check, pat_check):
                    continue

                # ── Exclude patterns ──
                if exclude_patterns:
                    fn_ex = filename if case_sensitive else filename.lower()
                    if any(fnmatch.fnmatch(fn_ex, p if case_sensitive else p.lower())
                           for p in exclude_patterns):
                        continue

                # ── Extension filter ──
                if ext_filter:
                    # Support comma-separated: .py,.txt
                    exts = [e.strip().lstrip('.') for e in ext_filter.split(',')]
                    file_ext = Path(filename).suffix.lstrip('.').lower()
                    if file_ext not in exts:
                        continue

                # ── Path contains ──
                if path_contains:
                    if path_contains not in dirpath.lower():
                        continue

                # ── File size ──
                try:
                    size = os.path.getsize(full_path)
                except OSError:
                    continue

                if min_size >= 0 and size < min_size:
                    continue
                if max_size >= 0 and size > max_size:
                    continue

                # ── Date ──
                try:
                    mtime = os.path.getmtime(full_path)
                    mod_date = datetime.fromtimestamp(mtime)
                except OSError:
                    mod_date = None

                count += 1
                self.result_found.emit({
                    "name": filename,
                    "path": dirpath,
                    "full_path": full_path,
                    "size": size,
                    "modified": mod_date,
                    "ext": Path(filename).suffix,
                })

        self.search_done.emit(count)


# ─────────────────────────────────────────────
#  MAIN WINDOW
# ─────────────────────────────────────────────
class AdvancedSearchWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.result_count = 0
        self.setWindowTitle("Advanced File Search")
        self.setMinimumSize(1100, 700)
        self.resize(1200, 780)
        self._build_ui()
        self.setStyleSheet(DARK_STYLE)
        self._load_settings()

    def closeEvent(self, event):
        self._save_settings()
        super().closeEvent(event)

    # ── SETTINGS PERSISTENCE ─────────────────
    def _save_settings(self):
        data = {
            "search_dir":        self.dir_input.text(),
            "name_pattern":      self.name_input.text(),
            "extensions":        self.ext_input.text(),
            "path_contains":     self.path_input.text(),
            "exclude_patterns":  self.exclude_input.text(),
            "exclude_folders":   self.exclude_folders_input.text(),
            "min_size_value":    self.min_size_spin.value(),
            "min_size_unit":     self.min_size_unit.currentText(),
            "min_size_enabled":  self.min_size_enabled.isChecked(),
            "max_size_value":    self.max_size_spin.value(),
            "max_size_unit":     self.max_size_unit2.currentText(),
            "max_size_enabled":  self.max_size_enabled.isChecked(),
            "search_subdirs":    self.chk_subdirs.isChecked(),
            "case_sensitive":    self.chk_case.isChecked(),
            "include_hidden":    self.chk_hidden.isChecked(),
            # window geometry
            "window_x":          self.x(),
            "window_y":          self.y(),
            "window_w":          self.width(),
            "window_h":          self.height(),
        }
        try:
            SETTINGS_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
        except Exception:
            pass  # never crash on save failure

    def _load_settings(self):
        if not SETTINGS_FILE.exists():
            return
        try:
            data = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
        except Exception:
            return  # corrupt/missing file — just use defaults

        def s(key, widget, setter):
            if key in data:
                try:
                    setter(widget, data[key])
                except Exception:
                    pass

        s("search_dir",       self.dir_input,       lambda w, v: w.setText(v))
        s("name_pattern",     self.name_input,      lambda w, v: w.setText(v))
        s("extensions",       self.ext_input,       lambda w, v: w.setText(v))
        s("path_contains",    self.path_input,      lambda w, v: w.setText(v))
        s("exclude_patterns", self.exclude_input,          lambda w, v: w.setText(v))
        s("exclude_folders",  self.exclude_folders_input,  lambda w, v: w.setText(v))
        s("min_size_value",   self.min_size_spin,   lambda w, v: w.setValue(int(v)))
        s("min_size_unit",    self.min_size_unit,   lambda w, v: w.setCurrentText(v))
        s("min_size_enabled", self.min_size_enabled,lambda w, v: w.setChecked(bool(v)))
        s("max_size_value",   self.max_size_spin,   lambda w, v: w.setValue(int(v)))
        s("max_size_unit",    self.max_size_unit2,  lambda w, v: w.setCurrentText(v))
        s("max_size_enabled", self.max_size_enabled,lambda w, v: w.setChecked(bool(v)))
        s("search_subdirs",   self.chk_subdirs,     lambda w, v: w.setChecked(bool(v)))
        s("case_sensitive",   self.chk_case,        lambda w, v: w.setChecked(bool(v)))
        s("include_hidden",   self.chk_hidden,      lambda w, v: w.setChecked(bool(v)))

        # Restore window geometry if it fits on screen
        try:
            screen = QApplication.primaryScreen().availableGeometry()
            x = data.get("window_x", self.x())
            y = data.get("window_y", self.y())
            w = data.get("window_w", self.width())
            h = data.get("window_h", self.height())
            # Clamp so window is never off-screen
            x = max(0, min(x, screen.width()  - 200))
            y = max(0, min(y, screen.height() - 100))
            w = max(self.minimumWidth(),  min(w, screen.width()))
            h = max(self.minimumHeight(), min(h, screen.height()))
            self.setGeometry(x, y, w, h)
        except Exception:
            pass

    # ── UI CONSTRUCTION ──────────────────────
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(14, 14, 14, 10)
        root_layout.setSpacing(10)

        # ── Title bar ──
        title_row = QHBoxLayout()
        title_lbl = QLabel("⌕  ADVANCED FILE SEARCH")
        title_lbl.setFont(QFont("Consolas", 15, QFont.Weight.Bold))
        title_lbl.setStyleSheet("color: #4299e1; letter-spacing: 2px;")
        subtitle = QLabel("Windows 10  ·  Wildcard  ·  Filters  ·  Fast")
        subtitle.setStyleSheet("color: #4a5568; font-size: 11px; margin-left: 8px; margin-top: 3px;")
        title_row.addWidget(title_lbl)
        title_row.addWidget(subtitle)
        title_row.addStretch()
        root_layout.addLayout(title_row)

        sep = QFrame(); sep.setObjectName("separator"); sep.setFixedHeight(1)
        root_layout.addWidget(sep)

        # ── Search form (top panel) ──
        form_layout = QHBoxLayout()
        form_layout.setSpacing(10)

        # Left column: primary filters
        left_group = QGroupBox("Search Criteria")
        left_grid = QGridLayout(left_group)
        left_grid.setSpacing(8)
        left_grid.setContentsMargins(10, 18, 10, 10)

        # Search directory
        left_grid.addWidget(QLabel("Search In:"), 0, 0)
        dir_row = QHBoxLayout(); dir_row.setSpacing(6)
        self.dir_input = QLineEdit()
        self.dir_input.setPlaceholderText("C:\\Users\\You\\Documents")
        self.dir_input.setText(str(Path.home()))
        browse_btn = QPushButton("Browse…")
        browse_btn.setFixedWidth(80)
        browse_btn.clicked.connect(self._browse_dir)
        dir_row.addWidget(self.dir_input)
        dir_row.addWidget(browse_btn)
        left_grid.addLayout(dir_row, 0, 1)

        # File name / pattern
        left_grid.addWidget(QLabel("File Name:"), 1, 0)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g.  *report*  or  data_*.csv  or  *.py")
        self.name_input.returnPressed.connect(self._start_search)
        left_grid.addWidget(self.name_input, 1, 1)

        # Extension filter
        left_grid.addWidget(QLabel("Extensions:"), 2, 0)
        ext_row = QHBoxLayout(); ext_row.setSpacing(6)
        self.ext_input = QLineEdit()
        self.ext_input.setPlaceholderText(".py, .txt, .csv  (comma-separated, or blank for all)")
        self.ext_quick = QComboBox()
        self.ext_quick.addItems(["— quick pick —", ".py", ".txt", ".csv", ".xlsx",
                                  ".pdf", ".docx", ".jpg", ".png", ".mp4", ".zip", ".exe", ".log"])
        self.ext_quick.setFixedWidth(130)
        self.ext_quick.currentTextChanged.connect(self._quick_ext)
        ext_row.addWidget(self.ext_input)
        ext_row.addWidget(self.ext_quick)
        left_grid.addLayout(ext_row, 2, 1)

        # Path contains
        left_grid.addWidget(QLabel("Path Contains:"), 3, 0)
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("e.g.  projects\\backend  (leave blank for any)")
        left_grid.addWidget(self.path_input, 3, 1)

        # Exclude file patterns
        left_grid.addWidget(QLabel("Exclude Files:"), 4, 0)
        self.exclude_input = QLineEdit()
        self.exclude_input.setPlaceholderText("e.g.  __*,  *.min.js,  test_*  (comma-separated wildcards)")
        self.exclude_input.returnPressed.connect(self._start_search)
        left_grid.addWidget(self.exclude_input, 4, 1)

        # Exclude folder patterns
        left_grid.addWidget(QLabel("Exclude Folders:"), 5, 0)
        excl_folder_row = QHBoxLayout(); excl_folder_row.setSpacing(6)
        self.exclude_folders_input = QLineEdit()
        self.exclude_folders_input.setPlaceholderText("e.g.  .venv,  Lib,  site-packages,  __pycache__,  node_modules")
        self.exclude_folders_input.returnPressed.connect(self._start_search)
        self.excl_folder_quick = QComboBox()
        self.excl_folder_quick.addItems([
            "— quick add —", ".venv", "venv", "env", "__pycache__",
            "Lib", "site-packages", "node_modules", ".git", "dist", "build", ".idea", ".vscode"
        ])
        self.excl_folder_quick.setFixedWidth(145)
        self.excl_folder_quick.currentTextChanged.connect(self._quick_excl_folder)
        excl_folder_row.addWidget(self.exclude_folders_input)
        excl_folder_row.addWidget(self.excl_folder_quick)
        left_grid.addLayout(excl_folder_row, 5, 1)

        left_grid.setColumnMinimumWidth(0, 110)
        left_grid.setColumnStretch(1, 1)
        form_layout.addWidget(left_group, 3)

        # Right column: size + options
        right_group = QGroupBox("Filters & Options")
        right_grid = QGridLayout(right_group)
        right_grid.setSpacing(8)
        right_grid.setContentsMargins(10, 18, 10, 10)

        # Size filter
        right_grid.addWidget(QLabel("Min Size:"), 0, 0)
        size_min_row = QHBoxLayout(); size_min_row.setSpacing(4)
        self.min_size_spin = QSpinBox()
        self.min_size_spin.setRange(0, 999999)
        self.min_size_spin.setValue(0)
        self.min_size_spin.setFixedWidth(80)
        self.min_size_unit = QComboBox()
        self.min_size_unit.addItems(["bytes", "KB", "MB", "GB"])
        self.min_size_unit.setCurrentText("KB")
        self.min_size_unit.setFixedWidth(65)
        self.min_size_enabled = QCheckBox("Enable")
        self.min_size_enabled.setChecked(False)
        size_min_row.addWidget(self.min_size_spin)
        size_min_row.addWidget(self.min_size_unit)
        size_min_row.addWidget(self.min_size_enabled)
        right_grid.addLayout(size_min_row, 0, 1)

        right_grid.addWidget(QLabel("Max Size:"), 1, 0)
        size_max_row = QHBoxLayout(); size_max_row.setSpacing(4)
        self.max_size_spin = QSpinBox()
        self.max_size_spin.setRange(0, 999999)
        self.max_size_spin.setValue(100)
        self.max_size_spin.setFixedWidth(80)
        self.max_size_unit2 = QComboBox()
        self.max_size_unit2.addItems(["bytes", "KB", "MB", "GB"])
        self.max_size_unit2.setCurrentText("MB")
        self.max_size_unit2.setFixedWidth(65)
        self.max_size_enabled = QCheckBox("Enable")
        self.max_size_enabled.setChecked(False)
        size_max_row.addWidget(self.max_size_spin)
        size_max_row.addWidget(self.max_size_unit2)
        size_max_row.addWidget(self.max_size_enabled)
        right_grid.addLayout(size_max_row, 1, 1)

        # Options
        right_grid.addWidget(QLabel("Options:"), 2, 0, Qt.AlignmentFlag.AlignTop)
        opts_col = QVBoxLayout(); opts_col.setSpacing(4)
        self.chk_subdirs = QCheckBox("Search subdirectories")
        self.chk_subdirs.setChecked(True)
        self.chk_case = QCheckBox("Case-sensitive name match")
        self.chk_hidden = QCheckBox("Include hidden files/folders")
        opts_col.addWidget(self.chk_subdirs)
        opts_col.addWidget(self.chk_case)
        opts_col.addWidget(self.chk_hidden)
        right_grid.addLayout(opts_col, 2, 1)

        right_grid.setColumnMinimumWidth(0, 80)
        right_grid.setColumnStretch(1, 1)
        form_layout.addWidget(right_group, 2)
        root_layout.addLayout(form_layout)

        # ── Action buttons ──
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        self.search_btn = QPushButton("▶  Search")
        self.search_btn.setObjectName("searchBtn")
        self.search_btn.setFixedHeight(36)
        self.search_btn.clicked.connect(self._start_search)

        self.stop_btn = QPushButton("■  Stop")
        self.stop_btn.setObjectName("stopBtn")
        self.stop_btn.setFixedHeight(36)
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self._stop_search)

        self.clear_btn = QPushButton("✕  Clear")
        self.clear_btn.setObjectName("clearBtn")
        self.clear_btn.setFixedHeight(36)
        self.clear_btn.clicked.connect(self._clear_results)

        self.result_count_lbl = QLabel("No results yet")
        self.result_count_lbl.setObjectName("resultCount")

        self.new_proj_btn = QPushButton("＋  New Project")
        self.new_proj_btn.setFixedHeight(36)
        self.new_proj_btn.setStyleSheet(
            "QPushButton{background:#276749;border:1px solid #48bb78;color:#c6f6d5;"
            "font-weight:bold;border-radius:4px;padding:7px 16px;font-size:12px;}"
            "QPushButton:hover{background:#2f855a;}")
        self.new_proj_btn.clicked.connect(self._open_new_project)

        btn_row.addWidget(self.search_btn)
        btn_row.addWidget(self.stop_btn)
        btn_row.addWidget(self.clear_btn)
        btn_row.addWidget(self.new_proj_btn)
        btn_row.addStretch()
        btn_row.addWidget(self.result_count_lbl)
        root_layout.addLayout(btn_row)

        # ── Progress bar ──
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setVisible(False)
        root_layout.addWidget(self.progress_bar)

        # ── Results table ──
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["File Name", "Extension", "Path", "Size", "Modified"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setColumnWidth(0, 260)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSortingEnabled(True)
        self.table.doubleClicked.connect(self._open_file)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._context_menu)
        root_layout.addWidget(self.table)

        # ── Status bar ──
        self.status_lbl = QLabel("Ready — Enter a search pattern and click Search")
        self.status_lbl.setObjectName("statusLabel")
        root_layout.addWidget(self.status_lbl)

    # ── HELPERS ─────────────────────────────
    def _size_to_bytes(self, value, unit):
        mult = {"bytes": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3}
        return value * mult.get(unit, 1)

    def _format_size(self, n):
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if n < 1024:
                return f"{n:.1f} {unit}"
            n /= 1024
        return f"{n:.1f} PB"

    def _quick_ext(self, text):
        if not text.startswith("—"):
            current = self.ext_input.text().strip()
            ext_clean = text.lstrip('.')
            if current:
                self.ext_input.setText(current + ", ." + ext_clean)
            else:
                self.ext_input.setText(text)
        self.ext_quick.setCurrentIndex(0)

    def _quick_excl_folder(self, text):
        if not text.startswith("—"):
            current = self.exclude_folders_input.text().strip()
            if current:
                # Don't add duplicates
                existing = [x.strip() for x in current.split(",")]
                if text not in existing:
                    self.exclude_folders_input.setText(current + ", " + text)
            else:
                self.exclude_folders_input.setText(text)
        self.excl_folder_quick.setCurrentIndex(0)

    def _browse_dir(self):
        d = QFileDialog.getExistingDirectory(self, "Select Search Directory",
                                              self.dir_input.text())
        if d:
            self.dir_input.setText(d)

    # ── SEARCH ──────────────────────────────
    def _start_search(self):
        if self.worker and self.worker.isRunning():
            return

        root = self.dir_input.text().strip()
        if not root or not os.path.isdir(root):
            QMessageBox.warning(self, "Invalid Directory",
                                "Please select a valid search directory.")
            return

        # Collect params
        min_bytes = -1
        max_bytes = -1
        if self.min_size_enabled.isChecked():
            min_bytes = self._size_to_bytes(self.min_size_spin.value(),
                                             self.min_size_unit.currentText())
        if self.max_size_enabled.isChecked():
            max_bytes = self._size_to_bytes(self.max_size_spin.value(),
                                             self.max_size_unit2.currentText())

        params = {
            "root": root,
            "name_pattern": self.name_input.text() or "*",
            "ext_filter": self.ext_input.text(),
            "min_size": min_bytes,
            "max_size": max_bytes,
            "path_contains": self.path_input.text(),
            "exclude_patterns": self.exclude_input.text(),
            "exclude_folders": self.exclude_folders_input.text(),
            "case_sensitive": self.chk_case.isChecked(),
            "include_hidden": self.chk_hidden.isChecked(),
            "search_subdirs": self.chk_subdirs.isChecked(),
        }

        # Reset UI
        self.table.setRowCount(0)
        self.result_count = 0
        self.result_count_lbl.setText("Searching…")
        self.progress_bar.setVisible(True)
        self.search_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.table.setSortingEnabled(False)

        self.worker = SearchWorker(params)
        self.worker.result_found.connect(self._add_result)
        self.worker.progress_update.connect(self._update_status)
        self.worker.search_done.connect(self._search_finished)
        self.worker.error_signal.connect(self._search_error)
        self.worker.start()

    def _stop_search(self):
        if self.worker:
            self.worker.stop()
            self.stop_btn.setEnabled(False)
            self.status_lbl.setText("Stopping…")

    def _clear_results(self):
        if self.worker and self.worker.isRunning():
            self.worker.stop()
        self.table.setRowCount(0)
        self.result_count = 0
        self.result_count_lbl.setText("No results yet")
        self.status_lbl.setText("Cleared.")

    # ── RESULT SLOTS ────────────────────────
    def _add_result(self, info):
        row = self.table.rowCount()
        self.table.insertRow(row)

        name_item = QTableWidgetItem(info["name"])
        name_item.setData(Qt.ItemDataRole.UserRole, info["full_path"])
        name_item.setToolTip(info["full_path"])
        name_item.setForeground(QColor("#90cdf4"))

        ext_item = QTableWidgetItem(info["ext"])
        ext_item.setForeground(QColor("#f6ad55"))
        ext_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        path_item = QTableWidgetItem(info["path"])
        path_item.setForeground(QColor("#a0aec0"))
        path_item.setToolTip(info["path"])

        size_item = NumericSortItem(self._format_size(info["size"]))
        size_item.setData(Qt.ItemDataRole.UserRole, info["size"])
        size_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        size_item.setForeground(QColor("#68d391"))

        date_str = info["modified"].strftime("%Y-%m-%d  %H:%M") if info["modified"] else "—"
        date_item = QTableWidgetItem(date_str)
        date_item.setForeground(QColor("#b794f4"))

        self.table.setItem(row, 0, name_item)
        self.table.setItem(row, 1, ext_item)
        self.table.setItem(row, 2, path_item)
        self.table.setItem(row, 3, size_item)
        self.table.setItem(row, 4, date_item)

        self.result_count += 1
        if self.result_count % 20 == 0:
            self.result_count_lbl.setText(f"{self.result_count:,}  results found")

    def _update_status(self, msg):
        self.status_lbl.setText(msg)

    def _search_finished(self, count):
        self.table.setSortingEnabled(True)
        self.progress_bar.setVisible(False)
        self.search_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.result_count_lbl.setText(f"{count:,}  result{'s' if count != 1 else ''} found")
        self.status_lbl.setText(f"Search complete. {count:,} file(s) matched.")

    def _search_error(self, msg):
        self.status_lbl.setText(f"Error: {msg}")

    # ── TABLE INTERACTIONS ──────────────────
    def _open_file(self, index):
        row = index.row()
        item = self.table.item(row, 0)
        if not item:
            return
        path = item.data(Qt.ItemDataRole.UserRole)
        if not path or not os.path.exists(path):
            return
        if path.lower().endswith(".py"):
            self._run_python_file(path)
        else:
            os.startfile(path)

    def _run_python_file(self, full_path):
        dlg = RunPythonDialog(full_path, parent=self)
        dlg.exec()
        self.status_lbl.setText(f"Launched: {os.path.basename(full_path)}")

    def _open_new_project(self):
        dlg = NewProjectDialog(parent=self)
        dlg.exec()

    def _context_menu(self, pos):
        row = self.table.rowAt(pos.y())
        if row < 0:
            return
        item = self.table.item(row, 0)
        if not item:
            return
        full_path = item.data(Qt.ItemDataRole.UserRole)
        if not full_path:
            return

        is_py = full_path.lower().endswith(".py")
        menu = QMenu(self)

        if is_py:
            act_run = QAction("▶  Run Python File…", self)
            act_run.setToolTip("Launch this script in a terminal window")
            act_run.triggered.connect(lambda: self._run_python_file(full_path))
            act_run.setFont(QFont("Consolas", 10, QFont.Weight.Bold))
            menu.addAction(act_run)
            menu.addSeparator()

        act_open = QAction("🗒  Open in Editor", self)
        act_open.triggered.connect(lambda: os.startfile(full_path) if os.path.exists(full_path) else None)

        act_folder = QAction("📁  Open Containing Folder", self)
        act_folder.triggered.connect(lambda: os.startfile(os.path.dirname(full_path)))

        act_copy_path = QAction("📋  Copy Full Path", self)
        act_copy_path.triggered.connect(lambda: QApplication.clipboard().setText(full_path))

        act_copy_name = QAction("📋  Copy File Name", self)
        act_copy_name.triggered.connect(lambda: QApplication.clipboard().setText(os.path.basename(full_path)))

        menu.addAction(act_open)
        menu.addAction(act_folder)
        menu.addSeparator()
        menu.addAction(act_copy_path)
        menu.addAction(act_copy_name)
        menu.exec(QCursor.pos())


# ─────────────────────────────────────────────
#  RUN PYTHON DIALOG
# ─────────────────────────────────────────────
def _find_python_interpreters(target_script_path=None):
    """Return a list of (label, path) tuples for available Python interpreters.
    Searches for venvs in the target script's folder first, then the app folder."""
    found = []
    seen_paths = set()

    def add(label, path):
        norm = str(Path(path).resolve()).lower()
        if norm not in seen_paths and Path(path).exists():
            seen_paths.add(norm)
            found.append((label, path))

    # 1. Venv LOCAL to the target script being launched (highest priority)
    if target_script_path:
        target_dir = Path(target_script_path).resolve().parent
        for venv_name in [".venv", "venv", "env"]:
            candidate = target_dir / venv_name / "Scripts" / "python.exe"
            if candidate.exists():
                add(f"📁 Local venv  ({target_dir / venv_name})  ← recommended", str(candidate))

    # 2. Venv next to THIS search app
    app_dir = Path(sys.argv[0]).resolve().parent
    for venv_name in [".venv", "venv", "env"]:
        candidate = app_dir / venv_name / "Scripts" / "python.exe"
        if candidate.exists():
            add(f"App venv  ({app_dir / venv_name})", str(candidate))

    # 3. The interpreter currently running this app
    add(f"Current  ({sys.executable})", sys.executable)

    # 4. 'python' / 'python3' on PATH
    for cmd in ("python", "python3"):
        try:
            result = subprocess.run([cmd, "--version"], capture_output=True, text=True, timeout=3)
            if result.returncode == 0:
                full = subprocess.run(
                    [cmd, "-c", "import sys; print(sys.executable)"],
                    capture_output=True, text=True, timeout=3
                ).stdout.strip()
                if full:
                    ver = (result.stdout + result.stderr).strip()
                    add(f"PATH  {ver}  ({full})", full)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

    return found



class _ConsoleRunner(QThread):
    line_out     = pyqtSignal(str)
    line_err     = pyqtSignal(str)
    finished_sig = pyqtSignal(int)

    def __init__(self, interp, script, args, cwd):
        super().__init__()
        self.interp = interp
        self.script = script
        self.args   = args
        self.cwd    = cwd
        self._proc  = None

    def kill(self):
        if self._proc:
            self._proc.kill()

    def run(self):
        import threading as _threading
        try:
            self._proc = subprocess.Popen(
                ([self.interp] + ([self.script] if self.script else []) + self.args),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self.cwd,
                text=True,
                encoding="utf-8",
                errors="replace"
            )
            def pump(pipe, sig):
                for line in pipe:
                    sig.emit(line.rstrip())
                pipe.close()
            t1 = _threading.Thread(target=pump, args=(self._proc.stdout, self.line_out), daemon=True)
            t2 = _threading.Thread(target=pump, args=(self._proc.stderr, self.line_err), daemon=True)
            t1.start(); t2.start()
            t1.join();  t2.join()
            self._proc.wait()
            self.finished_sig.emit(self._proc.returncode)
        except Exception as e:
            self.line_err.emit(str(e))
            self.finished_sig.emit(-1)


class RunPythonDialog(QDialog):
    def __init__(self, filepath, parent=None):
        super().__init__(parent)
        self.filepath = filepath
        self.setWindowTitle("Run Python File")
        self.setMinimumWidth(560)
        self.setStyleSheet(DARK_STYLE + """
            QDialog { border: 1px solid #2d3748; }
            QRadioButton { color: #e2e8f0; spacing: 8px; padding: 3px 0; }
            QRadioButton::indicator { width: 14px; height: 14px;
                border: 1px solid #4a5568; border-radius: 7px; background: #1a202c; }
            QRadioButton::indicator:checked {
                background: #3182ce; border-color: #4299e1; }
            QTextEdit { background: #0e1117; border: 1px solid #2d3748;
                border-radius: 4px; color: #68d391; font-family: Consolas;
                font-size: 11px; padding: 4px; }
        """)
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 12)

        # File label
        file_lbl = QLabel(f"<b style='color:#90cdf4'>▶  {Path(self.filepath).name}</b>")
        file_lbl.setStyleSheet("font-size: 13px;")
        layout.addWidget(file_lbl)

        path_lbl = QLabel(self.filepath)
        path_lbl.setStyleSheet("color: #4a5568; font-size: 10px; font-family: Consolas;")
        path_lbl.setWordWrap(True)
        layout.addWidget(path_lbl)

        # Separator
        sep = QFrame(); sep.setObjectName("separator"); sep.setFixedHeight(1)
        layout.addWidget(sep)

        # Interpreter selection
        interp_lbl = QLabel("Python Interpreter:")
        interp_lbl.setStyleSheet("color: #63b3ed; font-weight: bold; font-size: 11px; letter-spacing: 0.5px;")
        layout.addWidget(interp_lbl)

        self.interp_group = QButtonGroup(self)
        self.interpreters = _find_python_interpreters(self.filepath)

        for i, (label, path) in enumerate(self.interpreters):
            rb = QRadioButton(label)
            rb.setToolTip(path)
            if i == 0:
                rb.setChecked(True)
            self.interp_group.addButton(rb, i)
            layout.addWidget(rb)

        if not self.interpreters:
            layout.addWidget(QLabel("⚠  No Python interpreter found on PATH."))

        # Arguments
        sep2 = QFrame(); sep2.setObjectName("separator"); sep2.setFixedHeight(1)
        layout.addWidget(sep2)

        args_lbl = QLabel("Script Arguments  <span style='color:#4a5568'>(optional)</span>:")
        args_lbl.setStyleSheet("color: #63b3ed; font-weight: bold; font-size: 11px; letter-spacing: 0.5px;")
        layout.addWidget(args_lbl)

        self.args_input = QLineEdit()
        self.args_input.setPlaceholderText('e.g.  --input file.csv  --verbose')
        layout.addWidget(self.args_input)

        # Preview command
        sep3 = QFrame(); sep3.setObjectName("separator"); sep3.setFixedHeight(1)
        layout.addWidget(sep3)

        prev_lbl = QLabel("Command Preview:")
        prev_lbl.setStyleSheet("color: #63b3ed; font-weight: bold; font-size: 11px;")
        layout.addWidget(prev_lbl)

        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setFixedHeight(46)
        layout.addWidget(self.preview)

        # Wire up live preview
        self.interp_group.buttonClicked.connect(self._update_preview)
        self.args_input.textChanged.connect(self._update_preview)
        self._update_preview()

        # Progress bar (hidden until an operation is running)
        self.op_progress = QProgressBar()
        self.op_progress.setRange(0, 0)   # indeterminate
        self.op_progress.setFixedHeight(6)
        self.op_progress.setVisible(False)
        layout.addWidget(self.op_progress)

        # Built-in console output (hidden until used)
        self.console_out = QTextEdit()
        self.console_out.setReadOnly(True)
        self.console_out.setMinimumHeight(160)
        self.console_out.setMaximumHeight(260)
        self.console_out.setStyleSheet(
            "background:#060a0f; color:#a0aec0; font-family:Consolas; font-size:11px; border:1px solid #2d3748;")
        self.console_out.setVisible(False)
        layout.addWidget(self.console_out)

        # ── Package Manager (hidden until venv exists) ──────────────
        self.pkg_sep = QFrame(); self.pkg_sep.setObjectName("separator"); self.pkg_sep.setFixedHeight(1)
        self.pkg_sep.setVisible(False)
        layout.addWidget(self.pkg_sep)

        self.pkg_lbl = QLabel("📦  Package Manager")
        self.pkg_lbl.setStyleSheet("color:#63b3ed; font-weight:bold; font-size:11px; letter-spacing:0.5px;")
        self.pkg_lbl.setVisible(False)
        layout.addWidget(self.pkg_lbl)

        # Installed packages list
        self.pkg_list = QTableWidget(0, 2)
        self.pkg_list.setHorizontalHeaderLabels(["Package", "Version"])
        self.pkg_list.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.pkg_list.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.pkg_list.verticalHeader().setVisible(False)
        self.pkg_list.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.pkg_list.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.pkg_list.setAlternatingRowColors(True)
        self.pkg_list.setFixedHeight(140)
        self.pkg_list.setVisible(False)
        layout.addWidget(self.pkg_list)

        # Install row
        pkg_install_row = QHBoxLayout()
        self.pkg_input = QLineEdit()
        self.pkg_input.setPlaceholderText("package name  e.g. requests  numpy  discord.py")
        self.pkg_input.setVisible(False)
        self.pkg_install_btn = QPushButton("⬇  Install")
        self.pkg_install_btn.setObjectName("searchBtn")
        self.pkg_install_btn.setFixedWidth(90)
        self.pkg_install_btn.setFixedHeight(30)
        self.pkg_install_btn.setVisible(False)
        self.pkg_req_btn = QPushButton("📄  Install requirements.txt")
        self.pkg_req_btn.setFixedHeight(30)
        self.pkg_req_btn.setVisible(False)
        pkg_install_row.addWidget(self.pkg_input)
        pkg_install_row.addWidget(self.pkg_install_btn)
        pkg_install_row.addWidget(self.pkg_req_btn)
        layout.addLayout(pkg_install_row)

        self.pkg_input.returnPressed.connect(self._on_install_pkg)
        self.pkg_install_btn.clicked.connect(self._on_install_pkg)
        self.pkg_req_btn.clicked.connect(self._on_install_requirements)
        # ────────────────────────────────────────────────────────────

        # Buttons
        btn_row2 = QHBoxLayout()
        self.run_btn = QPushButton("▶  Run")
        self.run_btn.setObjectName("searchBtn")
        self.run_btn.setFixedHeight(34)
        self.kill_btn = QPushButton("■  Kill")
        self.kill_btn.setObjectName("stopBtn")
        self.kill_btn.setFixedHeight(34)
        self.kill_btn.setVisible(False)
        cancel_btn = QPushButton("Close")
        cancel_btn.setObjectName("clearBtn")
        cancel_btn.setFixedHeight(34)
        btn_row2.addWidget(self.run_btn)
        btn_row2.addWidget(self.kill_btn)
        btn_row2.addStretch()
        btn_row2.addWidget(cancel_btn)
        layout.addLayout(btn_row2)

        self.run_btn.clicked.connect(self._on_run)
        self.kill_btn.clicked.connect(self._on_kill)
        cancel_btn.clicked.connect(self.reject)
        if not self.interpreters:
            self.run_btn.setEnabled(False)

        self._proc_thread   = None
        self._recreate_btn  = None
        self._venv_interp   = None   # set after successful recreate

        # If venv already healthy, show pkg manager immediately
        idx = max(self.interp_group.checkedId(), 0)
        if self.interpreters:
            self._maybe_show_pkg_manager(self.interpreters[idx][1])

    def _update_preview(self):
        cmd = self._build_command(preview=True)
        self.preview.setPlainText(cmd)

    def _build_command(self, preview=False):
        idx = max(self.interp_group.checkedId(), 0)
        interp = self.interpreters[idx][1] if self.interpreters else "python"
        args = self.args_input.text().strip().split() if self.args_input.text().strip() else []
        script_dir = str(Path(self.filepath).parent)
        inner = subprocess.list2cmdline([interp, self.filepath] + args)
        if preview:
            return f'[cwd: {script_dir}]\n{inner}'
        return inner

    # ── Launch ───────────────────────────────────────────────────────
    def _on_run(self):
        self._run_in_console()

    def _on_kill(self):
        if self._proc_thread:
            self._proc_thread.kill()

    def _run_in_console(self):
        idx = max(self.interp_group.checkedId(), 0)
        interp = self.interpreters[idx][1] if self.interpreters else "python"
        args = self.args_input.text().strip().split() if self.args_input.text().strip() else []
        script_dir = str(Path(self.filepath).parent)

        self.console_out.setVisible(True)
        self.console_out.clear()
        self.run_btn.setEnabled(False)
        self.kill_btn.setVisible(True)

        self._log(f"▶ interpreter : {interp}")
        self._log(f"▶ script      : {self.filepath}")
        self._log(f"▶ cwd         : {script_dir}")
        self._log("─" * 60)

        if not Path(interp).exists():
            self._log(f"\n⚠  Interpreter not found: {interp}", color="#fc8181")
            self._log("   • Recreate the venv:  python -m venv .venv", color="#fbd38d")
            self._log("   • Or select a different interpreter above", color="#fbd38d")
            self.run_btn.setEnabled(True)
            self.kill_btn.setVisible(False)
            return

        # pyvenv.cfg stale check
        venv_dir = Path(interp).parent.parent
        cfg = venv_dir / "pyvenv.cfg"
        if cfg.exists():
            cfg_text = cfg.read_text(encoding="utf-8", errors="ignore")
            for line in cfg_text.splitlines():
                if any(line.startswith(k) for k in ("home", "executable", "command")):
                    self._log(f"   pyvenv.cfg: {line.strip()}", color="#4a5568")
            for line in cfg_text.splitlines():
                if line.startswith("executable"):
                    stored = line.split("=", 1)[1].strip()
                    if not Path(stored).exists():
                        self._log("\n⚠  Stale venv detected!", color="#fc8181")
                        self._log(f"   pyvenv.cfg points to: {stored}", color="#fc8181")
                        self._log("   That path does not exist on this machine.", color="#fc8181")
                        self._log("   The venv was built elsewhere and must be recreated here.", color="#fbd38d")
                        self._log("─" * 60)
                        self._show_recreate_btn(script_dir)
                        self.run_btn.setEnabled(True)
                        self.kill_btn.setVisible(False)
                        return

        self.op_progress.setVisible(True)
        self._proc_thread = _ConsoleRunner(interp, self.filepath, args, script_dir)
        self._proc_thread.line_out.connect(lambda t: self._log(t, color="#e2e8f0"))
        self._proc_thread.line_err.connect(self._handle_err_line)
        self._proc_thread.finished_sig.connect(self._on_proc_done)
        self._proc_thread.start()

    # ── Stale venv fix ───────────────────────────────────────────────
    def _show_recreate_btn(self, script_dir):
        if self._recreate_btn:
            return
        self._recreate_script_dir = script_dir
        self._recreate_btn = QPushButton("🔧  Auto-fix: Recreate .venv here  (python -m venv .venv)")
        self._recreate_btn.setStyleSheet(
            "background:#276749; border:1px solid #48bb78; color:#c6f6d5;"
            "font-weight:bold; padding:8px; border-radius:4px; font-size:12px;")
        self._recreate_btn.clicked.connect(self._do_recreate_venv)
        lay = self.layout()
        lay.insertWidget(lay.indexOf(self.op_progress), self._recreate_btn)

    def _do_recreate_venv(self):
        import sys as _sys
        self._recreate_btn.setEnabled(False)
        self._recreate_btn.setText("⏳  Recreating .venv ...")
        script_dir = self._recreate_script_dir
        self.console_out.setVisible(True)
        self.op_progress.setVisible(True)
        self._log("\n▶ python -m venv .venv", color="#68d391")
        self._log(f"  in: {script_dir}", color="#68d391")
        self._log("─" * 60)
        self._recreate_runner = _ConsoleRunner(
            _sys.executable, "", ["-m", "venv", ".venv"], script_dir)
        self._recreate_runner.line_out.connect(lambda t: self._log(t, color="#e2e8f0"))
        self._recreate_runner.line_err.connect(lambda t: self._log(t, color="#fc8181"))
        self._recreate_runner.finished_sig.connect(self._on_recreate_done)
        self._recreate_runner.start()

    def _on_recreate_done(self, retcode):
        self.op_progress.setVisible(False)
        script_dir = self._recreate_script_dir
        venv_python = str(Path(script_dir) / ".venv" / "Scripts" / "python.exe")
        if retcode == 0:
            self._venv_interp = venv_python
            self._log("\n✓ .venv recreated successfully!", color="#68d391")
            self._recreate_btn.setText("✓  .venv recreated")
            self._recreate_btn.setStyleSheet(
                "background:#1a365d; border:1px solid #4299e1; color:#bee3f8;"
                "font-weight:bold; padding:8px; border-radius:4px; font-size:12px;")
            self._show_pkg_manager(venv_python, script_dir)
        else:
            self._log(f"\n✗ Recreate failed (exit {retcode})", color="#fc8181")
            self._log("  Make sure 'python' is on your PATH", color="#fbd38d")
            self._recreate_btn.setEnabled(True)
            self._recreate_btn.setText("🔧  Retry: Recreate .venv")

    # ── Package Manager ──────────────────────────────────────────────
    def _maybe_show_pkg_manager(self, interp):
        """Show package manager if the venv is valid (not stale)."""
        if not Path(interp).exists():
            return
        venv_dir = Path(interp).parent.parent
        cfg = venv_dir / "pyvenv.cfg"
        if cfg.exists():
            cfg_text = cfg.read_text(encoding="utf-8", errors="ignore")
            for line in cfg_text.splitlines():
                if line.startswith("executable"):
                    stored = line.split("=", 1)[1].strip()
                    if not Path(stored).exists():
                        return  # stale — don't show manager
        script_dir = str(Path(self.filepath).parent)
        self._venv_interp = interp
        self._show_pkg_manager(interp, script_dir)

    def _show_pkg_manager(self, interp, script_dir):
        self.pkg_sep.setVisible(True)
        self.pkg_lbl.setVisible(True)
        self.pkg_list.setVisible(True)
        self.pkg_input.setVisible(True)
        self.pkg_install_btn.setVisible(True)
        req_file = Path(script_dir) / "requirements.txt"
        self.pkg_req_btn.setVisible(req_file.exists())
        self.adjustSize()
        self._load_pkg_list(interp)

    def _load_pkg_list(self, interp):
        self.pkg_list.setRowCount(0)
        try:
            result = subprocess.run(
                [interp, "-m", "pip", "list", "--format=columns"],
                capture_output=True, text=True, timeout=15)
            lines = result.stdout.strip().splitlines()
            # Skip header lines (Package / Version / -------)
            data_lines = [l for l in lines if l and not l.startswith("Package") and not l.startswith("---")]
            self.pkg_list.setRowCount(len(data_lines))
            for row, line in enumerate(data_lines):
                parts = line.split()
                pkg  = parts[0] if len(parts) > 0 else ""
                ver  = parts[1] if len(parts) > 1 else ""
                pi = QTableWidgetItem(pkg); pi.setForeground(QColor("#90cdf4"))
                vi = QTableWidgetItem(ver); vi.setForeground(QColor("#68d391"))
                vi.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.pkg_list.setItem(row, 0, pi)
                self.pkg_list.setItem(row, 1, vi)
            self.pkg_lbl.setText(f"📦  Package Manager  ({len(data_lines)} installed)")
        except Exception as e:
            self._log(f"pip list failed: {e}", color="#fc8181")

    def _on_install_pkg(self):
        pkg = self.pkg_input.text().strip()
        if not pkg or not self._venv_interp:
            return
        script_dir = str(Path(self.filepath).parent)
        self._run_pip(["install", pkg], script_dir, f"Installing {pkg}...")

    def _on_install_requirements(self):
        if not self._venv_interp:
            return
        script_dir = str(Path(self.filepath).parent)
        req = str(Path(script_dir) / "requirements.txt")
        self._run_pip(["install", "-r", req], script_dir, "Installing requirements.txt...")

    def _run_pip(self, pip_args, script_dir, label):
        self.console_out.setVisible(True)
        self.op_progress.setVisible(True)
        self.pkg_install_btn.setEnabled(False)
        self.pkg_req_btn.setEnabled(False)
        self._log(f"\n▶ pip {' '.join(pip_args)}", color="#63b3ed")
        self._log("─" * 60)
        runner = _ConsoleRunner(self._venv_interp, "", ["-m", "pip"] + pip_args, script_dir)
        runner.line_out.connect(lambda t: self._log(t, color="#e2e8f0"))
        runner.line_err.connect(lambda t: self._log(t, color="#fc8181"))
        runner.finished_sig.connect(lambda rc: self._on_pip_done(rc))
        self._pip_runner = runner
        runner.start()

    def _on_pip_done(self, retcode):
        self.op_progress.setVisible(False)
        self.pkg_install_btn.setEnabled(True)
        self.pkg_req_btn.setEnabled(True)
        self.pkg_input.clear()
        if retcode == 0:
            self._log("\n✓ Done!", color="#68d391")
            self._load_pkg_list(self._venv_interp)   # refresh list
        else:
            self._log(f"\n✗ pip failed (exit {retcode})", color="#fc8181")

    # ── Errors / logging ─────────────────────────────────────────────
    def _handle_err_line(self, line):
        self._log(line, color="#fc8181")
        suggestions = {
            "SyntaxError":       "   → Fix: check the line number above for a syntax issue",
            "PermissionError":   "   → Fix: run as administrator or check file permissions",
            "FileNotFoundError": "   → Fix: check the file/path exists",
            "RecursionError":    "   → Fix: add sys.setrecursionlimit() or fix infinite recursion",
            "MemoryError":       "   → Fix: reduce data size or increase available RAM",
            "ConnectionRefused": "   → Fix: check the server/port is running",
        }
        for key, tip in suggestions.items():
            if key in line:
                self._log(tip, color="#fbd38d")

        # Auto-detect missing module and offer one-click install
        import re as _re
        m = _re.search(r"No module named .([\w.]+).", line)
        if not m:
            m = _re.search(r"ModuleNotFoundError.*([\w.]+)", line)
        if m:
            mod = m.group(1).split(".")[0]
            pkg = MODULE_TO_PACKAGE.get(mod, mod)
            self._log(f"   → Missing module: {mod}", color="#fbd38d")
            self._log(f"   → Likely package:  {pkg}", color="#fbd38d")
            if self._venv_interp:
                self._offer_install_btn(pkg)

    def _offer_install_btn(self, pkg):
        """Show a one-click install button for a missing package."""
        btn_id = f"_install_btn_{pkg}"
        if hasattr(self, btn_id):
            return  # already showing
        btn = QPushButton(f"⬇  Install  {pkg}  into venv")
        btn.setStyleSheet(
            "background:#2b4a7a; border:1px solid #4299e1; color:#bee3f8;"
            "font-weight:bold; padding:6px 12px; border-radius:4px; font-size:11px;")
        btn.clicked.connect(lambda: self._quick_install(pkg, btn))
        setattr(self, btn_id, btn)
        lay = self.layout()
        lay.insertWidget(lay.indexOf(self.console_out) + 1, btn)

    def _quick_install(self, pkg, btn):
        btn.setEnabled(False)
        btn.setText(f"⏳  Installing {pkg}...")
        script_dir = str(Path(self.filepath).parent)
        self._run_pip(["install", pkg], script_dir, f"install {pkg}")

    def _on_proc_done(self, retcode):
        self.op_progress.setVisible(False)
        self._log("─" * 60)
        if retcode == 0:
            self._log(f"✓ Finished — exit code {retcode}", color="#68d391")
        else:
            self._log(f"✗ Exited with code {retcode}", color="#fc8181")
        self.run_btn.setEnabled(True)
        self.kill_btn.setVisible(False)

    def _log(self, text, color="#a0aec0"):
        self.console_out.setTextColor(QColor(color))
        self.console_out.append(text)

    def get_run_params(self):
        idx = max(self.interp_group.checkedId(), 0)
        interp = self.interpreters[idx][1] if self.interpreters else "python"
        args = self.args_input.text().strip().split() if self.args_input.text().strip() else []
        return interp, args


# ─────────────────────────────────────────────────────────────────────────────
#  PACKAGE DATA
#  module_name → pip_package  (for auto-fix on ImportError)
# ─────────────────────────────────────────────────────────────────────────────
MODULE_TO_PACKAGE = {
    # Web / HTTP
    "requests": "requests", "httpx": "httpx", "aiohttp": "aiohttp",
    "urllib3": "urllib3", "httplib2": "httplib2", "websocket": "websocket-client",
    "websockets": "websockets", "flask": "flask", "fastapi": "fastapi",
    "uvicorn": "uvicorn", "starlette": "starlette", "django": "django",
    "tornado": "tornado", "bottle": "bottle", "sanic": "sanic",
    "quart": "quart", "litestar": "litestar",
    # Data / Science
    "numpy": "numpy", "np": "numpy", "pandas": "pandas", "pd": "pandas",
    "scipy": "scipy", "sklearn": "scikit-learn", "matplotlib": "matplotlib",
    "plt": "matplotlib", "seaborn": "seaborn", "plotly": "plotly",
    "bokeh": "bokeh", "altair": "altair", "statsmodels": "statsmodels",
    "xgboost": "xgboost", "lightgbm": "lightgbm", "catboost": "catboost",
    # AI / ML
    "torch": "torch", "torchvision": "torchvision", "tensorflow": "tensorflow",
    "tf": "tensorflow", "keras": "keras", "transformers": "transformers",
    "openai": "openai", "anthropic": "anthropic", "langchain": "langchain",
    "langchain_core": "langchain-core", "langchain_community": "langchain-community",
    "llama_index": "llama-index", "chromadb": "chromadb", "tiktoken": "tiktoken",
    "sentence_transformers": "sentence-transformers", "diffusers": "diffusers",
    # Database
    "sqlalchemy": "SQLAlchemy", "alembic": "alembic", "pymysql": "PyMySQL",
    "psycopg2": "psycopg2-binary", "motor": "motor", "pymongo": "pymongo",
    "redis": "redis", "aioredis": "aioredis", "databases": "databases",
    "tortoise": "tortoise-orm", "peewee": "peewee", "dataset": "dataset",
    "tinydb": "tinydb",
    # Async
    "asyncio": "asyncio", "trio": "trio", "anyio": "anyio",
    "celery": "celery", "dramatiq": "dramatiq", "rq": "rq",
    # CLI / TUI
    "click": "click", "typer": "typer", "rich": "rich",
    "textual": "textual", "urwid": "urwid", "blessed": "blessed",
    "colorama": "colorama", "tqdm": "tqdm", "alive_progress": "alive-progress",
    "argparse": "argparse", "docopt": "docopt", "fire": "fire",
    # File / IO
    "openpyxl": "openpyxl", "xlrd": "xlrd", "xlwt": "xlwt",
    "xlsxwriter": "XlsxWriter", "pypdf": "pypdf", "pypdf2": "PyPDF2",
    "pdfplumber": "pdfplumber", "reportlab": "reportlab", "fpdf": "fpdf2",
    "docx": "python-docx", "docx2txt": "docx2txt", "pptx": "python-pptx",
    "csv": "csv", "toml": "toml", "tomllib": "tomli",
    "yaml": "pyyaml", "dotenv": "python-dotenv", "decouple": "python-decouple",
    # Image / Media
    "PIL": "Pillow", "cv2": "opencv-python", "imageio": "imageio",
    "skimage": "scikit-image", "wand": "Wand",
    "pydub": "pydub", "librosa": "librosa", "soundfile": "soundfile",
    "moviepy": "moviepy", "av": "av",
    # GUI
    "tkinter": "tk", "wx": "wxPython", "gi": "PyGObject",
    "PyQt5": "PyQt5", "PyQt6": "PyQt6", "PySide6": "PySide6",
    "kivy": "kivy", "customtkinter": "customtkinter",
    # Scraping
    "bs4": "beautifulsoup4", "BeautifulSoup": "beautifulsoup4",
    "scrapy": "scrapy", "selenium": "selenium", "playwright": "playwright",
    "mechanize": "mechanize", "lxml": "lxml", "parsel": "parsel",
    # Config / Validation
    "pydantic": "pydantic", "attrs": "attrs", "marshmallow": "marshmallow",
    "cerberus": "cerberus", "voluptuous": "voluptuous",
    # Networking / protocols
    "paramiko": "paramiko", "fabric": "fabric", "netmiko": "netmiko",
    "ftplib": "ftplib", "imaplib": "imaplib", "smtplib": "smtplib",
    "socket": "socket", "pyzmq": "pyzmq", "zmq": "pyzmq",
    "pika": "pika", "kafka": "kafka-python", "nats": "nats-py",
    # Security / Crypto
    "cryptography": "cryptography", "nacl": "PyNaCl", "jwt": "PyJWT",
    "bcrypt": "bcrypt", "passlib": "passlib", "pyotp": "pyotp",
    # Testing
    "pytest": "pytest", "hypothesis": "hypothesis", "faker": "Faker",
    "factory_boy": "factory-boy", "responses": "responses",
    "freezegun": "freezegun", "mock": "mock",
    # DevOps / Cloud
    "boto3": "boto3", "botocore": "botocore", "azure": "azure",
    "google.cloud": "google-cloud", "kubernetes": "kubernetes",
    "docker": "docker", "ansible": "ansible",
    # Bots / Messaging
    "discord": "discord.py", "telegram": "python-telegram-bot",
    "slack_sdk": "slack-sdk", "tweepy": "tweepy",
    "telethon": "Telethon", "pyrogram": "pyrogram",
    # Misc
    "arrow": "arrow", "pendulum": "pendulum", "dateutil": "python-dateutil",
    "humanize": "humanize", "tabulate": "tabulate", "prettytable": "PrettyTable",
    "loguru": "loguru", "structlog": "structlog",
    "apscheduler": "APScheduler", "schedule": "schedule",
    "psutil": "psutil", "pywin32": "pywin32", "winreg": "pywin32",
    "pyautogui": "pyautogui", "pynput": "pynput", "keyboard": "keyboard",
    "pyperclip": "pyperclip", "plyer": "plyer", "notify2": "notify2",
    "qrcode": "qrcode", "barcode": "python-barcode",
    "pint": "pint", "sympy": "sympy", "networkx": "networkx",
}

# Categorised package list for the picker UI
PACKAGE_CATALOG = {
    "🌐  Web & HTTP": [
        "requests", "httpx", "aiohttp", "flask", "fastapi", "uvicorn",
        "django", "tornado", "starlette", "bottle", "sanic", "quart",
        "websockets", "websocket-client", "httplib2", "litestar",
    ],
    "📊  Data & Science": [
        "numpy", "pandas", "scipy", "scikit-learn", "matplotlib",
        "seaborn", "plotly", "bokeh", "altair", "statsmodels",
        "xgboost", "lightgbm", "catboost", "pyarrow", "polars",
    ],
    "🤖  AI & ML": [
        "openai", "anthropic", "torch", "torchvision", "tensorflow",
        "keras", "transformers", "langchain", "langchain-core",
        "langchain-community", "llama-index", "chromadb", "tiktoken",
        "sentence-transformers", "diffusers", "huggingface-hub",
    ],
    "🗄️  Database": [
        "SQLAlchemy", "alembic", "pymongo", "motor", "redis", "aioredis",
        "PyMySQL", "psycopg2-binary", "databases", "tortoise-orm",
        "peewee", "dataset", "tinydb", "elasticsearch",
    ],
    "⚡  Async & Tasks": [
        "anyio", "trio", "celery", "dramatiq", "rq", "apscheduler",
        "schedule", "asyncpg", "aiofiles", "aiobotocore",
    ],
    "🖥️  CLI & TUI": [
        "click", "typer", "rich", "textual", "colorama", "tqdm",
        "alive-progress", "fire", "docopt", "blessed", "urwid",
        "questionary", "prompt-toolkit",
    ],
    "📁  Files & Formats": [
        "openpyxl", "xlrd", "XlsxWriter", "pypdf", "PyPDF2", "pdfplumber",
        "reportlab", "fpdf2", "python-docx", "python-pptx",
        "pyyaml", "toml", "tomli", "python-dotenv", "python-decouple",
        "lxml", "xmltodict", "python-magic",
    ],
    "🖼️  Image & Media": [
        "Pillow", "opencv-python", "imageio", "scikit-image",
        "Wand", "pydub", "librosa", "soundfile", "moviepy",
    ],
    "🕷️  Scraping": [
        "beautifulsoup4", "scrapy", "selenium", "playwright",
        "lxml", "parsel", "mechanize", "httpx", "pyppeteer",
    ],
    "✅  Validation & Config": [
        "pydantic", "attrs", "marshmallow", "cerberus",
        "voluptuous", "dynaconf", "confuse",
    ],
    "🔐  Security & Auth": [
        "cryptography", "PyJWT", "bcrypt", "passlib", "pyotp",
        "PyNaCl", "paramiko", "python-jose",
    ],
    "🤖  Bots & Messaging": [
        "discord.py", "python-telegram-bot", "slack-sdk",
        "tweepy", "Telethon", "pyrogram", "nextcord",
    ],
    "☁️  Cloud & DevOps": [
        "boto3", "google-cloud-storage", "azure-storage-blob",
        "kubernetes", "docker", "ansible", "fabric",
    ],
    "🧪  Testing": [
        "pytest", "hypothesis", "Faker", "factory-boy", "responses",
        "freezegun", "mock", "pytest-asyncio", "pytest-cov", "coverage",
    ],
    "🔧  Utilities": [
        "loguru", "structlog", "python-dateutil", "arrow", "pendulum",
        "humanize", "tabulate", "PrettyTable", "psutil",
        "pywin32", "pyautogui", "pynput", "keyboard", "pyperclip",
        "qrcode", "sympy", "networkx", "pint",
    ],
    "🔥  PyTorch + CUDA": [
        "torch  (CPU)",
        "torch  (CUDA 11.8)",
        "torch  (CUDA 12.1)",
        "torch  (CUDA 12.4)",
        "torch  (CUDA 12.6)  ← cu126",
        "torch  (CUDA 12.8)",
        "torchvision  (CPU)",
        "torchvision  (CUDA 11.8)",
        "torchvision  (CUDA 12.1)",
        "torchvision  (CUDA 12.4)",
        "torchvision  (CUDA 12.6)  ← cu126",
        "torchvision  (CUDA 12.8)",
        "torchaudio  (CPU)",
        "torchaudio  (CUDA 11.8)",
        "torchaudio  (CUDA 12.1)",
        "torchaudio  (CUDA 12.4)",
        "torchaudio  (CUDA 12.6)  ← cu126",
        "torchaudio  (CUDA 12.8)",
    ],
}

# Maps display label → (packages, extra_pip_args)
# Torch CUDA installs need --index-url so they can't go through normal pip install
TORCH_INSTALL_MAP = {
    "torch  (CPU)":                      (["torch", "torchvision", "torchaudio"], []),
    "torch  (CUDA 11.8)":               (["torch", "torchvision", "torchaudio"], ["--index-url", "https://download.pytorch.org/whl/cu118"]),
    "torch  (CUDA 12.1)":               (["torch", "torchvision", "torchaudio"], ["--index-url", "https://download.pytorch.org/whl/cu121"]),
    "torch  (CUDA 12.4)":               (["torch", "torchvision", "torchaudio"], ["--index-url", "https://download.pytorch.org/whl/cu124"]),
    "torch  (CUDA 12.6)  ← cu126":      (["torch", "torchvision", "torchaudio"], ["--index-url", "https://download.pytorch.org/whl/cu126"]),
    "torch  (CUDA 12.8)":               (["torch", "torchvision", "torchaudio"], ["--index-url", "https://download.pytorch.org/whl/cu128"]),
    "torchvision  (CPU)":               (["torchvision"], []),
    "torchvision  (CUDA 11.8)":         (["torchvision"], ["--index-url", "https://download.pytorch.org/whl/cu118"]),
    "torchvision  (CUDA 12.1)":         (["torchvision"], ["--index-url", "https://download.pytorch.org/whl/cu121"]),
    "torchvision  (CUDA 12.4)":         (["torchvision"], ["--index-url", "https://download.pytorch.org/whl/cu124"]),
    "torchvision  (CUDA 12.6)  ← cu126":(["torchvision"], ["--index-url", "https://download.pytorch.org/whl/cu126"]),
    "torchvision  (CUDA 12.8)":         (["torchvision"], ["--index-url", "https://download.pytorch.org/whl/cu128"]),
    "torchaudio  (CPU)":                (["torchaudio"], []),
    "torchaudio  (CUDA 11.8)":          (["torchaudio"], ["--index-url", "https://download.pytorch.org/whl/cu118"]),
    "torchaudio  (CUDA 12.1)":          (["torchaudio"], ["--index-url", "https://download.pytorch.org/whl/cu121"]),
    "torchaudio  (CUDA 12.4)":          (["torchaudio"], ["--index-url", "https://download.pytorch.org/whl/cu124"]),
    "torchaudio  (CUDA 12.6)  ← cu126": (["torchaudio"], ["--index-url", "https://download.pytorch.org/whl/cu126"]),
    "torchaudio  (CUDA 12.8)":          (["torchaudio"], ["--index-url", "https://download.pytorch.org/whl/cu128"]),
}


# ─────────────────────────────────────────────────────────────────────────────
#  NEW PROJECT DIALOG
# ─────────────────────────────────────────────────────────────────────────────
class NewProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Python Project")
        self.setMinimumSize(760, 680)
        self.resize(820, 740)
        self.setStyleSheet(DARK_STYLE + """
            QDialog { border: 1px solid #2d3748; }
            QTabWidget::pane { border: 1px solid #2d3748; background: #0e1117; }
            QTabBar::tab { background:#141921; color:#718096; padding:6px 16px;
                border:1px solid #2d3748; border-bottom:none; border-radius:3px 3px 0 0; }
            QTabBar::tab:selected { background:#0e1117; color:#63b3ed; border-bottom:1px solid #0e1117; }
            QListWidget { background:#0e1117; border:1px solid #2d3748;
                color:#e2e8f0; font-size:12px; }
            QListWidget::item { padding:4px 8px; }
            QListWidget::item:selected { background:#1e3a5f; color:#bee3f8; }
            QListWidget::item:hover { background:#1a2535; }
            QCheckBox { color:#e2e8f0; spacing:6px; }
        """)
        self._selected_pkgs  = set()   # normal packages
        self._torch_selections = set() # torch variant display labels
        self._proc_thread    = None
        self._project_dir    = None
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setSpacing(10)
        lay.setContentsMargins(16, 14, 16, 12)

        # Title
        title = QLabel("＋  New Python Project")
        title.setFont(QFont("Consolas", 13, QFont.Weight.Bold))
        title.setStyleSheet("color:#48bb78; letter-spacing:1px;")
        lay.addWidget(title)

        sep = QFrame(); sep.setObjectName("separator"); sep.setFixedHeight(1)
        lay.addWidget(sep)

        # ── Row 1: project folder ──
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Project Folder:"))
        self.dir_edit = QLineEdit()
        self.dir_edit.setPlaceholderText("e.g.  C:\\Projects\\my_bot")
        browse = QPushButton("Browse…"); browse.setFixedWidth(80)
        browse.clicked.connect(self._browse)
        row1.addWidget(self.dir_edit)
        row1.addWidget(browse)
        lay.addLayout(row1)

        # ── Row 2: project name ──
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Project Name:"))
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("my_project  (used as subfolder name)")
        row2.addWidget(self.name_edit)
        lay.addLayout(row2)

        # ── Row 3: python interpreter ──
        row3 = QHBoxLayout()
        row3.addWidget(QLabel("Python:"))
        self.interp_combo = QComboBox()
        self._populate_interpreters()
        row3.addWidget(self.interp_combo)
        lay.addLayout(row3)

        sep2 = QFrame(); sep2.setObjectName("separator"); sep2.setFixedHeight(1)
        lay.addWidget(sep2)

        # ── Package Picker ──
        pkg_hdr = QHBoxLayout()
        pkg_lbl = QLabel("Select Packages:")
        pkg_lbl.setStyleSheet("color:#63b3ed; font-weight:bold; font-size:11px;")
        self.pkg_count_lbl = QLabel("0 selected")
        self.pkg_count_lbl.setStyleSheet("color:#68d391; font-size:11px;")
        self.pkg_search = QLineEdit()
        self.pkg_search.setPlaceholderText("🔍  search packages…")
        self.pkg_search.setFixedWidth(200)
        self.pkg_search.textChanged.connect(self._filter_packages)
        pkg_hdr.addWidget(pkg_lbl)
        pkg_hdr.addWidget(self.pkg_count_lbl)
        pkg_hdr.addStretch()
        pkg_hdr.addWidget(self.pkg_search)
        lay.addLayout(pkg_hdr)

        # Category tabs + package list side by side
        pkg_body = QHBoxLayout(); pkg_body.setSpacing(8)

        self.cat_list = QListWidget()
        self.cat_list.setFixedWidth(180)
        self.cat_list.setFixedHeight(260)
        for cat in PACKAGE_CATALOG:
            self.cat_list.addItem(cat)
        self.cat_list.currentTextChanged.connect(self._load_category)
        pkg_body.addWidget(self.cat_list)

        self.pkg_check_list = QListWidget()
        self.pkg_check_list.setFixedHeight(260)
        self.pkg_check_list.itemChanged.connect(self._on_pkg_toggled)
        pkg_body.addWidget(self.pkg_check_list)

        lay.addLayout(pkg_body)

        # Selected chips display
        self.selected_lbl = QLabel("No packages selected.")
        self.selected_lbl.setStyleSheet("color:#4a5568; font-size:10px; font-family:Consolas;")
        self.selected_lbl.setWordWrap(True)
        lay.addWidget(self.selected_lbl)

        sep3 = QFrame(); sep3.setObjectName("separator"); sep3.setFixedHeight(1)
        lay.addWidget(sep3)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.setFixedHeight(6)
        self.progress.setVisible(False)
        lay.addWidget(self.progress)

        # Console output
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setFixedHeight(120)
        self.console.setStyleSheet(
            "background:#060a0f; color:#a0aec0; font-family:Consolas;"
            "font-size:11px; border:1px solid #2d3748;")
        self.console.setVisible(False)
        lay.addWidget(self.console)

        # Buttons
        btn_row = QHBoxLayout()
        self.create_btn = QPushButton("🚀  Create Project")
        self.create_btn.setObjectName("searchBtn")
        self.create_btn.setFixedHeight(36)
        self.create_btn.clicked.connect(self._create_project)
        close_btn = QPushButton("Close")
        close_btn.setObjectName("clearBtn")
        close_btn.setFixedHeight(36)
        close_btn.clicked.connect(self.reject)
        btn_row.addWidget(self.create_btn)
        btn_row.addStretch()
        btn_row.addWidget(close_btn)
        lay.addLayout(btn_row)

        # Load first category
        self.cat_list.setCurrentRow(0)

    def _populate_interpreters(self):
        interps = _find_python_interpreters()
        self._interp_paths = []
        for label, path in interps:
            self.interp_combo.addItem(label)
            self._interp_paths.append(path)
        if not interps:
            self.interp_combo.addItem("No Python found on PATH")
            self._interp_paths.append("")

    def _browse(self):
        d = QFileDialog.getExistingDirectory(self, "Select Parent Folder")
        if d:
            self.dir_edit.setText(d)

    def _load_category(self, cat_text):
        self.pkg_check_list.blockSignals(True)
        self.pkg_check_list.clear()
        pkgs = PACKAGE_CATALOG.get(cat_text, [])
        search = self.pkg_search.text().lower()
        is_torch_cat = "PyTorch" in cat_text
        for pkg in pkgs:
            if search and search not in pkg.lower():
                continue
            item = QListWidgetItem(pkg)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            if is_torch_cat:
                # Torch variants live in _torch_selections, not _selected_pkgs
                checked = pkg in self._torch_selections
                item.setForeground(QColor("#f6ad55"))
                if "← cu126" in pkg:
                    item.setForeground(QColor("#fc8181"))  # highlight recommended
            else:
                checked = pkg in self._selected_pkgs
            item.setCheckState(Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked)
            self.pkg_check_list.addItem(item)
        self.pkg_check_list.blockSignals(False)

    def _filter_packages(self):
        cat = self.cat_list.currentItem()
        if cat:
            self._load_category(cat.text())

    def _on_pkg_toggled(self, item):
        pkg = item.text()
        is_torch = pkg in TORCH_INSTALL_MAP
        if item.checkState() == Qt.CheckState.Checked:
            if is_torch:
                self._torch_selections.add(pkg)
            else:
                self._selected_pkgs.add(pkg)
        else:
            if is_torch:
                self._torch_selections.discard(pkg)
            else:
                self._selected_pkgs.discard(pkg)
        total = len(self._selected_pkgs) + len(self._torch_selections)
        self.pkg_count_lbl.setText(f"{total} selected")
        parts = sorted(self._selected_pkgs) + sorted(self._torch_selections)
        if parts:
            self.selected_lbl.setText("  ".join(parts))
            self.selected_lbl.setStyleSheet("color:#90cdf4; font-size:10px; font-family:Consolas;")
        else:
            self.selected_lbl.setText("No packages selected.")
            self.selected_lbl.setStyleSheet("color:#4a5568; font-size:10px; font-family:Consolas;")

    def _log(self, text, color="#a0aec0"):
        self.console.setTextColor(QColor(color))
        self.console.append(text)

    def _create_project(self):
        parent_dir = self.dir_edit.text().strip()
        name       = self.name_edit.text().strip()
        if not parent_dir or not name:
            QMessageBox.warning(self, "Missing Info", "Please set both a folder and a project name.")
            return
        idx = self.interp_combo.currentIndex()
        interp = self._interp_paths[idx] if idx >= 0 and self._interp_paths else ""
        if not interp or not Path(interp).exists():
            QMessageBox.warning(self, "No Interpreter", "Please select a valid Python interpreter.")
            return

        project_dir = str(Path(parent_dir) / name)
        self._project_dir = project_dir

        self.create_btn.setEnabled(False)
        self.console.setVisible(True)
        self.progress.setVisible(True)
        self.console.clear()
        self._log(f"▶ Creating project: {project_dir}", color="#48bb78")
        self._log("─" * 60)

        # Create folder
        try:
            Path(project_dir).mkdir(parents=True, exist_ok=True)
            self._log(f"✓ Folder created: {project_dir}", color="#68d391")
        except Exception as e:
            self._log(f"✗ Could not create folder: {e}", color="#fc8181")
            self.create_btn.setEnabled(True)
            self.progress.setVisible(False)
            return

        # Write blank main.py
        main_py = Path(project_dir) / "main.py"
        if not main_py.exists():
            main_py.write_text(
                '# main.py\n\ndef main():\n    pass\n\n\nif __name__ == "__main__":\n    main()\n',
                encoding="utf-8")
            self._log("✓ main.py created", color="#68d391")

        self._log("▶ Creating .venv ...", color="#63b3ed")
        self._setup_runner = _ConsoleRunner(interp, "", ["-m", "venv", ".venv"], project_dir)
        self._setup_runner.line_out.connect(lambda t: self._log(t))
        self._setup_runner.line_err.connect(lambda t: self._log(t, color="#fc8181"))
        self._setup_runner.finished_sig.connect(self._on_venv_done)
        self._setup_runner.start()

    def _on_venv_done(self, retcode):
        project_dir = self._project_dir
        if retcode != 0:
            self._log("✗ venv creation failed", color="#fc8181")
            self.create_btn.setEnabled(True)
            self.progress.setVisible(False)
            return
        self._log("✓ .venv created", color="#68d391")
        venv_python = str(Path(project_dir) / ".venv" / "Scripts" / "python.exe")

        # Build install queue: torch variants first (each needs its own --index-url),
        # then all normal packages in one shot.
        self._install_queue = []
        for label in sorted(self._torch_selections):
            pkgs_list, extra = TORCH_INSTALL_MAP[label]
            self._install_queue.append((pkgs_list, extra, label))
        normal = sorted(self._selected_pkgs)
        if normal:
            self._install_queue.append((normal, [], "standard packages"))

        self._venv_python_path = venv_python
        self._run_next_install()

    def _run_next_install(self):
        project_dir = self._project_dir
        venv_python = self._venv_python_path
        if not self._install_queue:
            self._finish_project(venv_python, project_dir, [])
            return
        pkgs_list, extra, label = self._install_queue.pop(0)
        self._log(f"▶ Installing: {label}", color="#63b3ed")
        if extra:
            self._log(f"   {' '.join(extra)}", color="#4a5568")
        self._install_runner = _ConsoleRunner(
            venv_python, "", ["-m", "pip", "install"] + pkgs_list + extra, project_dir)
        self._install_runner.line_out.connect(lambda t: self._log(t))
        self._install_runner.line_err.connect(lambda t: self._log(t, color="#fc8181"))
        self._install_runner.finished_sig.connect(self._on_install_step_done)
        self._install_runner.start()

    def _on_install_step_done(self, retcode):
        if retcode == 0:
            self._log("✓ Done", color="#68d391")
        else:
            self._log("⚠  Install step had errors — check output above", color="#fbd38d")
        self._run_next_install()

    # _on_install_done kept for compatibility but queue handles steps now

    def _finish_project(self, venv_python, project_dir, pkgs):
        # Write requirements.txt from actual pip freeze
        try:
            result = subprocess.run(
                [venv_python, "-m", "pip", "freeze"],
                capture_output=True, text=True, timeout=15, cwd=project_dir)
            req_text = result.stdout.strip()
            req_path = Path(project_dir) / "requirements.txt"
            req_path.write_text(req_text, encoding="utf-8")
            lines = [l for l in req_text.splitlines() if l]
            self._log(f"✓ requirements.txt written ({len(lines)} entries)", color="#68d391")
        except Exception as e:
            self._log(f"⚠  Could not write requirements.txt: {e}", color="#fbd38d")

        self.progress.setVisible(False)
        self._log("─" * 60)
        self._log("🚀  Project ready!", color="#48bb78")
        self._log(f"   {project_dir}", color="#90cdf4")
        self._log("   Files: main.py  .venv/  requirements.txt", color="#a0aec0")

        # Open in explorer
        open_btn = QPushButton("📁  Open Project Folder")
        open_btn.setFixedHeight(30)
        open_btn.clicked.connect(lambda: os.startfile(project_dir))
        lay = self.layout()
        # Insert above last btn row
        lay.insertWidget(lay.count() - 1, open_btn)

        self.create_btn.setEnabled(True)


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Advanced File Search")
    app.setApplicationVersion("1.0")

    window = AdvancedSearchWindow()
    window.show()
    sys.exit(app.exec())

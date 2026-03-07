# ⌕ Advanced File Search
> A fast, wildcard-powered file search tool for Windows 10/11 with a built-in Python script launcher.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/PyQt6-6.4%2B-green?logo=qt&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%2010%2F11-lightgrey?logo=windows)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Overview

Windows Explorer's built-in search struggles with wildcard patterns like `*partialname*.py`. **Advanced File Search** solves that — giving you a fast, filterable, sortable file search with full wildcard support, folder exclusions, size filters, and a built-in launcher for Python scripts, all wrapped in a clean dark UI.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🔍 **Wildcard Search** | Full `fnmatch` wildcards — `*report*`, `data_202?_*.csv`, `__*` |
| 📂 **Recursive Walk** | Searches all subdirectories with toggle to disable |
| 🗂️ **Extension Filter** | Filter by one or more extensions — `.py, .txt, .csv` — with quick-pick dropdown |
| 🚫 **Exclude Files** | Wildcard patterns to skip files — e.g. `__*`, `*.min.js`, `test_*` |
| 🚫 **Exclude Folders** | Prunes entire directories from the walk — e.g. `.venv`, `Lib`, `__pycache__`, `node_modules` |
| 📍 **Path Contains** | Filter results to a specific subfolder fragment |
| 📏 **Size Filter** | Min/max file size with bytes / KB / MB / GB units |
| 🔤 **Case-Sensitive** | Optional case-sensitive filename matching |
| 👁️ **Hidden Files** | Opt-in to include hidden/dot files and folders |
| 🔃 **Sortable Results** | Click any column header — name, extension, path, size (numeric), modified date |
| ▶️ **Python Launcher** | Double-click or right-click any `.py` file to launch it in a terminal |
| 💾 **Persistent Settings** | All search fields, filters, and window position saved and restored automatically |

---

## 🖥️ Screenshots

```
┌─────────────────────────────────────────────────────────────────┐
│  ⌕  ADVANCED FILE SEARCH      Windows 10 · Wildcard · Filters  │
├──────────────────────────────┬──────────────────────────────────┤
│  Search Criteria             │  Filters & Options               │
│  Search In:  C:\Projects\... │  Min Size: [ 0  ] [KB ] [ ]     │
│  File Name:  *bot*.py        │  Max Size: [ 100] [MB ] [ ]     │
│  Extensions: .py             │                                  │
│  Path:       frbot            │  ☑ Search subdirectories        │
│  Excl Files: __*             │  ☐ Case-sensitive                │
│  Excl Dirs:  .venv,Lib       │  ☐ Include hidden               │
├──────────────────────────────┴──────────────────────────────────┤
│  [ ▶ Search ]  [ ■ Stop ]  [ ✕ Clear ]          12 results found│
├──────────────────────────────────────────────────────────────────┤
│  File Name          Ext   Path                   Size   Modified │
│  bot_core.py        .py   F:\Sort Desktop\frbot  4.2KB  2024-... │
│  bot_utils.py       .py   F:\Sort Desktop\frbot  1.8KB  2024-... │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Option A — Double-click launcher *(recommended)*
```
1. Place launch.bat and advanced_search.py in the same folder
2. Double-click launch.bat
```
The launcher will handle everything automatically on first run.

### Option B — Manual
```bash
pip install PyQt6
python advanced_search.py
```

---

## 📦 Requirements

| Requirement | Version |
|---|---|
| Python | 3.10 or later |
| PyQt6 | 6.4 or later |
| OS | Windows 10 / 11 |

---

## 🛠️ launch.bat — Auto Setup

The included `launch.bat` handles the full setup lifecycle:

```
[1/4] Checks Python is installed and >= 3.10
[2/4] Creates a .venv virtual environment if one doesn't exist
[3/4] Installs PyQt6 into the venv if not already installed
[4/4] Launches advanced_search.py inside the venv
```

- ✅ First run: ~30 seconds (downloads PyQt6)
- ✅ Subsequent runs: opens in ~1–2 seconds
- ✅ Keeps terminal open on crash so you can read the error

---

## ▶️ Python Script Launcher

When you find a `.py` file in the results, you can launch it directly from the app.

**How to trigger:**
- **Double-click** any `.py` result row
- **Right-click → ▶ Run Python File…**

**The Run dialog lets you:**

1. **Choose interpreter** — automatically detects:
   - 📁 Local `.venv` in the *target script's own folder* (listed first, recommended)
   - The venv next to the search app itself
   - The Python interpreter currently running the app
   - Any `python` / `python3` found on your PATH

2. **Add script arguments** — e.g. `--input data.csv --verbose`

3. **Toggle terminal behaviour:**
   - `cmd /k` — keeps the terminal open after the script finishes *(default)*
   - `cmd /c` — terminal closes automatically when done

4. **Command Preview** — shows the exact command that will run, including the working directory, before you click Run

> **Note:** The script always runs with its own folder as the working directory (`cwd`), so relative file paths inside your scripts work correctly.

---

## 🔍 Search Tips

### Wildcard Patterns
| Pattern | Matches |
|---|---|
| `*.py` | All Python files |
| `*bot*` | Any file with "bot" in the name |
| `data_202?.csv` | `data_2023.csv`, `data_2024.csv` etc. |
| `test_*.py` | `test_utils.py`, `test_main.py` etc. |
| `__*` | `__init__.py`, `__main__.py` etc. |

### Excluding Folders
Folder exclusion **prunes the directory tree** — the search never descends into excluded folders, making it significantly faster on large drives.

Common exclusions for Python projects:
```
.venv, venv, env, __pycache__, Lib, site-packages, dist, build, .git
```

Common exclusions for Node projects:
```
node_modules, dist, .git, .next, .nuxt
```

---

## 💾 Settings

All settings are automatically saved to `advanced_search_settings.json` in the same folder as the script when you close the app, and restored on next launch.

**What's saved:**
- All search fields (directory, name pattern, extensions, path filter, excludes)
- Size filter values and units
- All checkboxes (subdirs, case-sensitive, hidden files)
- Window size and position

To reset to defaults, simply delete `advanced_search_settings.json`.

---

## 🖱️ Context Menu (Right-click)

Right-clicking any result row gives you:

| Action | Description |
|---|---|
| ▶ Run Python File… | *(`.py` files only)* Opens the launcher dialog |
| 🗒 Open in Editor | Opens the file with its default associated program |
| 📁 Open Containing Folder | Opens the file's parent directory in Explorer |
| 📋 Copy Full Path | Copies the complete file path to clipboard |
| 📋 Copy File Name | Copies just the filename to clipboard |

---

## 📁 File Structure

```
your-folder/
├── advanced_search.py          # Main application
├── launch.bat                  # Auto-setup & launcher
├── advanced_search_settings.json  # Auto-generated, saved settings
└── .venv/                      # Auto-generated virtual environment
```

---

## 🐛 Troubleshooting

**`Python was not found`**
Install Python 3.10+ from [python.org](https://www.python.org/downloads/) and make sure to tick **"Add Python to PATH"** during installation.

**`PyQt6 installation failed`**
Check your internet connection. You can also install manually:
```bash
pip install PyQt6
```

**Script launcher opens terminal but immediately closes**
Tick **"Keep terminal open after script finishes"** in the Run dialog so you can read any error output.

**Search is slow on large drives**
Use **Exclude Folders** to skip heavy directories like `.venv`, `node_modules`, `Lib`, and `site-packages`. These can contain tens of thousands of files.

**Window opens off-screen**
Delete `advanced_search_settings.json` to reset the saved window position.

---

## 📄 License

MIT License — free to use, modify, and distribute.

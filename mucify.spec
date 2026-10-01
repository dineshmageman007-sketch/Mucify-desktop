# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for Mucify.  Build with:  pyinstaller --noconfirm --clean mucify.spec
# Output: dist/Mucify/Mucify.exe (onedir, windowed, no console)
import os
from PyInstaller.utils.hooks import collect_submodules

ROOT = os.path.abspath(SPECPATH)


def tree(src_rel, dest, skip_ext=()):
    """(source, dest-folder) pairs for every file under src_rel, keeping the layout."""
    out = []
    base = os.path.join(ROOT, src_rel)
    for dirpath, _dirs, files in os.walk(base):
        for f in files:
            if f.lower().endswith(tuple(skip_ext)):
                continue
            rel = os.path.relpath(dirpath, base)
            out.append((os.path.join(dirpath, f), os.path.normpath(os.path.join(dest, rel))))
    return out


datas = []
datas += tree("mucify/templates", "mucify/templates")
datas += tree("mucify/static", "mucify/static")
datas += tree("assets", "assets", skip_ext=(".bmp",))          # installer-only images stay out
# The tested sldl.exe / rsgain.exe (+ their DLLs, presets, licenses). Debug symbols are not needed.
datas += tree("tools", "tools", skip_ext=(".pdb",))

hiddenimports = (
    collect_submodules("webview")
    + ["mutagen.flac", "mutagen.id3", "mutagen.mp4", "mutagen.oggvorbis", "mutagen.oggopus"]
    + collect_submodules("mucify")
)
if os.name == "nt":
    hiddenimports += ["clr", "clr_loader"]

a = Analysis(
    ["run_mucify.py"],
    pathex=[ROOT],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=["tkinter", "matplotlib", "numpy", "pandas", "PIL", "pytest", "IPython"],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Mucify",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,                       # normal desktop app: no Command Prompt window
    icon=os.path.join(ROOT, "assets", "mucify.ico"),
)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name="Mucify")

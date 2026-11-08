# -*- mode: python ; coding: utf-8 -*-
# 文件夹打包（onedir：启动快、杀软误报少）：
#   uv run pyinstaller main.spec --noconfirm
#   → dist/__APP_NAME__/__APP_NAME__.exe（依赖在 dist/__APP_NAME__/__APP_NAME__-lib/）
#
# 带原生插件目录的库（mujoco、glfw 等）用 collect_all 收齐：
#   from PyInstaller.utils.hooks import collect_all
#   mj_datas, mj_binaries, mj_hidden = collect_all("mujoco")
#   然后并入下面的 datas / binaries / hiddenimports。

import os

# 图标可选：没有 assets/icon.ico 时也能打包（exe 用默认图标，程序内用 icons.py 画的回退图标）
_ICON_DATAS = [(p, 'assets') for p in ('assets/icon.ico', 'assets/icon.png') if os.path.isfile(p)]
_EXE_ICON = 'assets/icon.ico' if os.path.isfile('assets/icon.ico') else None

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=_ICON_DATAS,
    hiddenimports=['__PKG__'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 用不到的 Qt 模块，减小体积。3D 工具要保留 QtOpenGL / QtOpenGLWidgets，
        # 纯 Widgets 工具可把它们也加进来。
        'PySide6.QtWebEngineWidgets', 'PySide6.QtWebEngineCore', 'PySide6.QtWebEngineQuick', 'PySide6.QtWebChannel',
        'PySide6.QtQml', 'PySide6.QtQuick', 'PySide6.QtQuickWidgets', 'PySide6.QtQuickControls2',
        'PySide6.QtMultimedia', 'PySide6.QtMultimediaWidgets', 'PySide6.QtPdf', 'PySide6.QtPdfWidgets',
        'PySide6.QtCharts', 'PySide6.QtDataVisualization', 'PySide6.Qt3DCore', 'PySide6.Qt3DRender',
        'PySide6.Qt3DInput', 'PySide6.Qt3DLogic', 'PySide6.Qt3DAnimation', 'PySide6.Qt3DExtras',
        'PySide6.QtBluetooth', 'PySide6.QtNfc', 'PySide6.QtPositioning', 'PySide6.QtSensors', 'PySide6.QtLocation',
        'PySide6.QtSerialPort', 'PySide6.QtSerialBus', 'PySide6.QtSql', 'PySide6.QtTest', 'PySide6.QtXml',
        'PySide6.QtDesigner', 'PySide6.QtHelp', 'PySide6.QtUiTools',
        'PySide6.QtNetworkAuth', 'PySide6.QtRemoteObjects', 'PySide6.QtScxml', 'PySide6.QtStateMachine',
        'PySide6.QtTextToSpeech', 'PySide6.QtSpatialAudio', 'PySide6.QtHttpServer', 'PySide6.QtWebSockets',
        'PySide6.QtWebView', 'PySide6.QtGraphs', 'PySide6.QtGraphsWidgets',
        'tkinter', 'matplotlib', 'IPython', 'pytest',
    ],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='__APP_NAME__',
    icon=_EXE_ICON,
    contents_directory='__APP_NAME__-lib',   # PyInstaller 6 默认 _internal；带应用名避免多个工具解压到同一目录时互相覆盖
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,          # Qt / mujoco 的 DLL 压缩后易出问题
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    name='__APP_NAME__',
    strip=False,
    upx=False,
    upx_exclude=[],
)

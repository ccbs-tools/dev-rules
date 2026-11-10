"""入口：python -m __PKG__ [file]

顺序固定：先初始化日志，再 import Qt 与业务模块，最后建 QApplication 和主窗口。
"""

from __future__ import annotations

import sys


def main(argv: list[str] | None = None) -> int:
    import platform

    from .log import logger, setup_logging

    log_file = setup_logging()

    # 有原生 DLL 加载顺序要求的库（如 mujoco）放在这里、先于 Qt import
    from PySide6 import QtCore, QtGui, QtWidgets

    from . import APP_NAME, ORG, __version__
    from .i18n import i18n
    from .icons import app_icon
    from .main_window import MainWindow

    args = sys.argv[1:] if argv is None else argv
    logger.info("=" * 60)
    logger.info(
        "{} v{} starting | python {} | PySide6 {} | {} | frozen={}",
        APP_NAME, __version__, platform.python_version(), QtCore.__version__,
        platform.platform(), bool(getattr(sys, "frozen", False)),
    )
    logger.info("log file: {}", log_file)
    logger.debug("argv: {}", args)

    # Windows：不用 Python 默认 AppID，任务栏才会显示本程序图标而不是 python.exe
    if sys.platform == "win32":
        try:
            import ctypes

            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(f"{ORG}.{APP_NAME}")
        except Exception as e:  # noqa: BLE001
            logger.warning("SetCurrentProcessExplicitAppUserModelID failed: {}", e)

    # 3D 工具在这里设置 QSurfaceFormat（4x MSAA、24 位深度、CompatibilityProfile），必须早于 QApplication

    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName(ORG)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(__version__)
    app.setStyle("Fusion")
    app.setFont(QtGui.QFont("Microsoft YaHei UI", 9))
    i18n.load()                      # 读取上次选的语言（首次跟随系统），需在 QApplication 之后
    icon = app_icon()
    app.setWindowIcon(icon)

    initial = args[0] if args else None
    if initial:
        logger.info("initial file from argv: {}", initial)
    win = MainWindow(initial)
    win.setWindowIcon(icon)
    win.show()
    code = app.exec()
    logger.info("exit code={}", code)
    return code


if __name__ == "__main__":
    raise SystemExit(main())

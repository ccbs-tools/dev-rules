"""主窗口骨架：菜单栏（文件 / 语言 / 帮助）、拖放、retranslate。

把 central 占位控件换成业务控件；新增菜单项时文案走 i18n，并在 retranslate() 里设置。
"""

from __future__ import annotations

from pathlib import Path

from PySide6 import QtCore, QtGui, QtWidgets

from .changelog import REPO_HOME, VIDEO_TUTORIAL
from .i18n import LANGUAGES, i18n, tr
from .log import LOG_DIR, logger
from .version_dialogs import ChangelogDialog, UpdateCheckDialog


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, initial: str | None = None) -> None:
        super().__init__()
        self.resize(1000, 700)
        self.setAcceptDrops(True)
        self.path: Path | None = None

        # ---- 中央区域（占位，替换成业务控件）----
        self.central = QtWidgets.QLabel()
        self.central.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.central.setStyleSheet("color: #888; font-size: 14pt;")
        self.setCentralWidget(self.central)

        # ---- 文件菜单 ----
        self.act_open = QtGui.QAction(self)
        self.act_open.setShortcut(QtGui.QKeySequence.StandardKey.Open)
        self.act_open.triggered.connect(self.open_dialog)
        self.act_quit = QtGui.QAction(self)
        self.act_quit.setShortcut(QtGui.QKeySequence.StandardKey.Quit)
        self.act_quit.triggered.connect(self.close)
        self.menu_file = self.menuBar().addMenu("")
        self.menu_file.addAction(self.act_open)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.act_quit)

        # ---- 语言菜单：各语言用自己的名字显示，不随当前语言翻译 ----
        self.menu_lang = self.menuBar().addMenu("")
        self.lang_group = QtGui.QActionGroup(self)
        self.lang_group.setExclusive(True)
        for code, label in LANGUAGES:
            act = QtGui.QAction(label, self, checkable=True)
            act.setData(code)
            act.setChecked(code == i18n.lang)
            act.triggered.connect(lambda _=False, c=code: i18n.set(c))
            self.lang_group.addAction(act)
            self.menu_lang.addAction(act)

        # ---- 帮助菜单 ----
        self.menu_help = self.menuBar().addMenu("")
        self.act_repo = QtGui.QAction(self)
        self.act_repo.triggered.connect(lambda: self._open_url(REPO_HOME))
        self.menu_help.addAction(self.act_repo)
        self.act_video: QtGui.QAction | None = None
        if VIDEO_TUTORIAL:
            self.act_video = QtGui.QAction(self)
            self.act_video.triggered.connect(lambda: self._open_url(VIDEO_TUTORIAL))
            self.menu_help.addAction(self.act_video)
        self.menu_help.addSeparator()
        self.act_changelog = QtGui.QAction(self)
        self.act_changelog.triggered.connect(self._show_changelog)
        self.act_check_update = QtGui.QAction(self)
        self.act_check_update.triggered.connect(self._show_update_check)
        self.act_open_log_dir = QtGui.QAction(self)
        self.act_open_log_dir.triggered.connect(self._open_log_dir)
        self.menu_help.addAction(self.act_changelog)
        self.menu_help.addAction(self.act_check_update)
        self.menu_help.addAction(self.act_open_log_dir)

        i18n.languageChanged.connect(self.retranslate)
        self.retranslate()

        if initial:
            QtCore.QTimer.singleShot(0, lambda: self.load(initial))

    # ---- 文案 ----

    def retranslate(self) -> None:
        self.menu_file.setTitle(tr("menu.file"))
        self.act_open.setText(tr("menu.open"))
        self.act_quit.setText(tr("menu.quit"))
        self.menu_lang.setTitle(tr("menu.language"))
        for act in self.lang_group.actions():
            act.setChecked(act.data() == i18n.lang)
        self.menu_help.setTitle(tr("menu.help"))
        self.act_repo.setText(tr("menu.repo"))
        if self.act_video is not None:
            self.act_video.setText(tr("menu.video"))
        self.act_changelog.setText(tr("menu.changelog"))
        self.act_check_update.setText(tr("menu.check_update"))
        self.act_open_log_dir.setText(tr("menu.open_log_dir"))
        self.central.setText(tr("central.placeholder"))
        self._update_title()
        if self.path is None:
            self.statusBar().showMessage(tr("status.drop_hint"))

    def _update_title(self) -> None:
        if self.path is None:
            self.setWindowTitle(tr("app.title"))
        else:
            self.setWindowTitle(f"{tr('app.title')} — {self.path.name}")

    # ---- 业务：按需替换 ----

    def load(self, path: str) -> None:
        """加载文件（占位实现：只记录路径）。"""
        self.path = Path(path)
        logger.info("load: {}", self.path)
        self.central.setText(self.path.name)
        self._update_title()
        self.statusBar().showMessage(str(self.path))

    def open_dialog(self) -> None:
        start = str(self.path.parent) if self.path else ""
        fn, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, tr("dialog.open_title"), start, tr("dialog.open_filter"))
        if fn:
            logger.info("open dialog picked: {}", fn)
            self.load(fn)
        else:
            logger.debug("open dialog cancelled")

    # ---- 拖放：整个窗口（含菜单栏、状态栏）都接受 ----

    def dragEnterEvent(self, e: QtGui.QDragEnterEvent) -> None:
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e: QtGui.QDropEvent) -> None:
        urls = e.mimeData().urls()
        if urls:
            self.load(urls[0].toLocalFile())

    # ---- 帮助菜单动作 ----

    @staticmethod
    def _open_url(url: str) -> None:
        ok = QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))
        logger.info("open url: {} -> {}", url, "ok" if ok else "failed")

    def _open_log_dir(self) -> None:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        self._open_url(QtCore.QUrl.fromLocalFile(str(LOG_DIR)).toString())

    def _show_changelog(self) -> None:
        logger.info("open changelog dialog")
        ChangelogDialog(self).exec()

    def _show_update_check(self) -> None:
        logger.info("update check triggered from menu")
        UpdateCheckDialog(self).exec()

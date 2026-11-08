"""界面文案（中英文切换）。

用法：
    from .i18n import tr, i18n
    label.setText(tr("menu.file"))
    i18n.languageChanged.connect(self.retranslate)

语言保存在 QSettings（组织 ccbs / 应用 APP_NAME）。首次运行跟随系统：系统是中文 → zh，否则 → en。
新增文案：两张表各加一条，键名用 `模块.含义`。
"""

from __future__ import annotations

from PySide6.QtCore import QLocale, QObject, QSettings, Signal

from .log import logger

LANGUAGES = (("en", "English"), ("zh", "中文（简体）"))
_FALLBACK_LANG = "en"
_SETTINGS_KEY = "language"

_STRINGS: dict[str, dict[str, str]] = {
    "en": {
        "app.title": "__APP_TITLE_EN__",
        # ---- 菜单 ----
        "menu.file": "&File",
        "menu.open": "&Open…",
        "menu.quit": "&Quit",
        "menu.language": "&Language",
        "menu.help": "&Help",
        "menu.repo": "&Repository Homepage",
        "menu.video": "&Video Tutorial",
        "menu.changelog": "Version &Info",
        "menu.check_update": "Check for &Updates",
        "menu.open_log_dir": "Open &Log Folder",
        # ---- 版本介绍 / 检查更新（version_dialogs.py 用）----
        "chg.title": "Version info  (current v{ver})",
        "chg.check": "Check for updates",
        "chg.close": "Close",
        "upd.title": "Check for updates",
        "upd.checking": "Checking for updates…",
        "upd.countdown": "{sec} s",
        "upd.cancel": "Cancel",
        "upd.close": "Close",
        "upd.download": "Download",
        "upd.latest": "You are on the latest version (v{cur}).",
        "upd.newer": "New version v{latest} available (current v{cur}).",
        "upd.failed_short": "Check failed. Please check your network and try again.",
        "upd.timeout": "No response within {sec} s. Check your network and try again.",
        # ---- 状态栏 / 对话框 ----
        "status.ready": "Ready",
        "status.drop_hint": "Drop a file into the window, or File → Open",
        "dialog.open_title": "Open",
        "dialog.open_filter": "All files (*)",
        "central.placeholder": "Drop a file here\n\n(or Ctrl+O to open)",
    },
    "zh": {
        "app.title": "__APP_TITLE_ZH__",
        "menu.file": "文件(&F)",
        "menu.open": "打开(&O)…",
        "menu.quit": "退出(&Q)",
        "menu.language": "语言(&L)",
        "menu.help": "帮助(&H)",
        "menu.repo": "仓库主页(&R)",
        "menu.video": "视频教程(&V)",
        "menu.changelog": "版本介绍(&I)",
        "menu.check_update": "检查更新(&U)",
        "menu.open_log_dir": "打开日志目录(&L)",
        "chg.title": "版本介绍（当前 v{ver}）",
        "chg.check": "检查版本更新",
        "chg.close": "关闭",
        "upd.title": "检查版本更新",
        "upd.checking": "正在检查更新…",
        "upd.countdown": "{sec} 秒",
        "upd.cancel": "取消",
        "upd.close": "关闭",
        "upd.download": "下载",
        "upd.latest": "已是最新版本（v{cur}）。",
        "upd.newer": "发现新版本 v{latest}（当前 v{cur}）。",
        "upd.failed_short": "检查失败，请检查网络后重试。",
        "upd.timeout": "{sec} 秒内没有响应，请检查网络后重试。",
        "status.ready": "就绪",
        "status.drop_hint": "把文件拖进窗口，或 文件 → 打开",
        "dialog.open_title": "打开",
        "dialog.open_filter": "所有文件 (*)",
        "central.placeholder": "把文件拖到这里\n\n（或 Ctrl+O 打开）",
    },
}


def _system_default() -> str:
    return "zh" if QLocale.system().language() == QLocale.Language.Chinese else "en"


class _I18n(QObject):
    languageChanged = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self._lang = _FALLBACK_LANG

    @property
    def lang(self) -> str:
        return self._lang

    def load(self) -> str:
        """从 QSettings 读取上次选择的语言；需在 QApplication 创建后调用。"""
        saved = QSettings().value(_SETTINGS_KEY)
        self._lang = saved if saved in _STRINGS else _system_default()
        logger.info("language: {} (saved={!r}, system={})", self._lang, saved, QLocale.system().name())
        return self._lang

    def set(self, lang: str) -> None:
        if lang not in _STRINGS or lang == self._lang:
            return
        logger.info("language switched {} -> {}", self._lang, lang)
        self._lang = lang
        QSettings().setValue(_SETTINGS_KEY, lang)
        self.languageChanged.emit(lang)

    def tr(self, key: str, **kwargs) -> str:
        table = _STRINGS.get(self._lang, {})
        text = table.get(key) or _STRINGS[_FALLBACK_LANG].get(key) or key
        return text.format(**kwargs) if kwargs else text


i18n = _I18n()


def tr(key: str, **kwargs) -> str:
    return i18n.tr(key, **kwargs)


__all__ = ["LANGUAGES", "i18n", "tr"]

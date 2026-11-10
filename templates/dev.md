# 开发

规范：`../dev-rules/CONVENTIONS.md`。

## 环境

本项目用 [uv](https://docs.astral.sh/uv/) 管理 Python 与依赖，不需要单独安装 Python。

```powershell
uv sync --group dev                        # 安装运行依赖 + pyinstaller
uv run python -m __PKG__                   # 源码运行
uv run pyinstaller main.spec --noconfirm   # 本地打包 → dist\__APP_NAME__\__APP_NAME__.exe
```

运行时文件：

| 内容 | 位置 |
| --- | --- |
| 日志 | `%APPDATA%\__ORG__\__APP_NAME__\logs\app.log`（10 MB 轮转，保留 3 个） |
| 语言设置 | QSettings（注册表 `HKCU\Software\__ORG__\__APP_NAME__`） |

## 目录

```
run.py                       PyInstaller 入口（转调 __PKG__.__main__:main）
main.spec                    PyInstaller onedir 配置（裁掉未用的 Qt 模块）
__PKG__/
  __init__.py                APP_NAME、__version__
  __main__.py                入口：日志初始化、QApplication、主窗口
  i18n.py                    中英文文案表，tr() / i18n.languageChanged
  log.py                     loguru 日志；接管未捕获异常、Qt 消息、stdlib logging
  changelog.py               版本历史（Release 说明从这里生成）+ GitHub Releases 检查更新
  version_dialogs.py         版本介绍 / 检查更新对话框
  icons.py                   应用图标
  main_window.py             主窗口、菜单栏
assets/                      icon.ico / icon.png 与 README 截图
README.md / README.zh.md     面向用户的说明（英文 / 中文）
```

## 文案

所有界面文字集中在 `__PKG__/i18n.py` 的 `_STRINGS`，中英两张表的键必须一致。新增文案时：

1. 两张表各加一条，键名用 `模块.含义` 形式（如 `dialog.open_title`、`status.loaded`）。
2. 代码里用 `tr("key", **kwargs)` 取文案；动态刷新的控件在所属类的 `retranslate()` 里更新。

日志（`logger.*`）统一英文，不走 i18n，且不得记录密码/口令。

## 发版

版本号有三处，发版时一起改、保持一致：

1. `__PKG__/__init__.py` 的 `__version__`：程序内显示、检查更新比较用。
2. `pyproject.toml` 的 `version`：GitHub Actions 打包 zip 名用这个，例如 `__APP_NAME__-v0.1.1-windows-x64.zip`。
3. `__PKG__/changelog.py` 的 `RELEASES`：在最前面加一条版本说明，Actions 发布 Release 时用它生成说明文字。中英文 `notes` 都要写。

改完后提交，再推送同名 tag：

```powershell
git tag v0.1.1
git push origin v0.1.1
```

`.github/workflows/build.yml` 在 `v*` tag 上会打包并把 zip + `SHA256SUMS.txt` 发布到 Releases；在 Actions 页面手动 "Run workflow" 则只打包，产物在 Artifacts 里保留 7 天。

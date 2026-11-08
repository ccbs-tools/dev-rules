---
name: ccbs-new-tool
description: 按 CCBS 规范从 dev-rules/templates 新建一个 Python + PySide6 桌面小工具项目（uv、loguru、i18n、PyInstaller、GitHub Actions 发 Release）。当用户要“新建一个 ccbs 工具 / 按规范起一个新项目 / 再做一个和 stl-frame-editor 类似的工具”时使用。
---

# 新建 CCBS 桌面工具

规范全文在 `dev-rules/CONVENTIONS.md`（工作区根下）；本技能只负责把模板变成能跑的项目。

## 需要的信息

从用户消息里取，缺的用 AskQuestion 一次问齐：

- `APP_NAME`：仓库名，kebab-case（如 `urdf-inspector`）。`PKG` 自动取下划线版本。
- `TITLE`：一句话中文描述。
- `APP_TITLE_EN` / `APP_TITLE_ZH`：窗口标题。
- 源码仓库是否私有：决定用哪个 `build.yml`（见步骤 4）。
- 是否 3D / 几何类工具：决定是否保留 `QtOpenGL`、设置 `QSurfaceFormat`（CONVENTIONS §11）。
- 额外运行依赖（numpy、trimesh、mujoco、paramiko…），没有就只用模板默认。

## 步骤

1. 目标目录 `<工作区根>/<APP_NAME>/` 必须不存在。
2. 复制 `dev-rules/templates/` 全部内容（含 `.github/`、`.gitignore`）到目标目录；把 `templates/__PKG__/` 重命名为 `<PKG>/`。
3. 全文替换占位符：`__APP_NAME__` → APP_NAME，`__PKG__` → PKG，`__TITLE__` → TITLE，`__APP_TITLE_EN__`、`__APP_TITLE_ZH__`。
   替换后 `rg "__APP_NAME__|__PKG__|__TITLE__|__APP_TITLE"` 必须无结果。
4. 发布目标：
   - 源码公开：保留 `.github/workflows/build.yml`，删除 `build.release-repo.yml`。
   - 源码私有：删除 `build.yml`，把 `build.release-repo.yml` 改名为 `build.yml`；把 `<PKG>/changelog.py` 的 `RELEASE_REPO` 改成 `ccbs-tools/<APP_NAME>-release`。
5. `pyproject.toml`：按需追加依赖；用到 Qt Addons 模块才把 `PySide6-Essentials` 换成 `PySide6`。
6. 3D 工具：在 `__main__.py` 标注位置加 `QSurfaceFormat`（4x MSAA、24 位深度、CompatibilityProfile）；`main.spec` 不要排除 `QtOpenGL*`。纯 Widgets 工具：可把 `PySide6.QtOpenGL`、`PySide6.QtOpenGLWidgets` 加进 `excludes`。
7. `<PKG>/changelog.py` 的 `RELEASES[0]`：版本 `0.1.0`，日期改为今天，notes 写上这个工具做什么（中英都写）。
8. `assets/`：有图标就放 `icon.ico` + `icon.png`；没有就保留空目录（`icons.py` 会画回退图标），并在最后提醒用户。
9. 验证（离屏，不弹窗）：
   ```powershell
   uv sync --group dev
   $env:QT_QPA_PLATFORM="offscreen"; $env:PYTHONUTF8="1"
   uv run python -c "import sys; from <PKG>.log import setup_logging; setup_logging(); from PySide6 import QtWidgets, QtCore; from <PKG> import APP_NAME; from <PKG>.i18n import i18n; from <PKG>.main_window import MainWindow; app = QtWidgets.QApplication(sys.argv); app.setOrganizationName('ccbs'); app.setApplicationName(APP_NAME); i18n.load(); w = MainWindow(); w.show(); i18n.set('en'); i18n.set('zh'); print(w.windowTitle()); QtCore.QTimer.singleShot(300, app.quit); sys.exit(app.exec())"
   ```
   退出码 0、打印出窗口标题，且 `%APPDATA%\ccbs\<APP_NAME>\logs\app.log` 有 `language:` 一行。
   注意 `QTimer.singleShot` 必须在 `QApplication` 创建之后调用，否则不会触发（`main()` 内部建 app，所以不能用它来做自动退出）。
   再跑 `uv run pyinstaller main.spec --noconfirm`，确认 `dist/<APP_NAME>/<APP_NAME>.exe` 和 `<APP_NAME>-lib/` 生成。
   最后正常跑一次 `uv run python -m <PKG>` 让用户看窗口。
10. `git init -b main`，首个提交；远程由用户在 GitHub `ccbs-tools` 组织下建好后再 `git remote add origin` 推送。

## 交付时说明

- 还没做的：`assets/` 图标与 README 截图（`soft-empty-view.png`、`open-xxx-view.png`）、README 的 Usage/Controls、Demo 视频链接。
- 发版流程：三处版本号 + `git tag vX.Y.Z && git push origin vX.Y.Z`（`dev.md` 已写）。
- 私有仓库还需要在仓库 Secrets 里配 `RELEASE_APP_ID`、`RELEASE_APP_PRIVATE_KEY`，并在组织里把 `ccbs-release-bot` App 授权给 `<APP_NAME>-release`。

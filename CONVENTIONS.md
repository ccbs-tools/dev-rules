# CCBS 桌面工具开发规范

本文档是 `ccbs-tools` 组织下所有 Python + PySide6 桌面小工具的统一约定。
完整的可复制文件在 `templates/`，本文只讲规则、理由和最小示例。

读者是人和 AI。新建项目时按 §12 的清单走；修改老项目时以本文为准，老项目与本文不一致的地方见 §13。

## 0. 术语与占位符

| 占位符 | 含义 | 示例 |
| --- | --- | --- |
| `__APP_NAME__` | 仓库名 / 可执行文件名 / 发布 zip 前缀，kebab-case | `stl-frame-editor` |
| `__PKG__` | Python 包名，`__APP_NAME__` 的下划线版本 | `stl_frame_editor` |
| `__TITLE__` | 一句话中文描述（pyproject `description`、`__init__` docstring） | `STL 坐标系修改器` |
| `__APP_TITLE_EN__` | 英文窗口标题（`i18n` 的 `app.title`） | `STL Coordinate Frame Editor` |
| `__APP_TITLE_ZH__` | 中文窗口标题 | `STL 坐标系修改器` |

`templates/` 下所有文件和目录名里的占位符都要替换；替换后全文搜索 `__APP_NAME__|__PKG__|__TITLE__|__APP_TITLE` 应无结果。

## 1. 项目骨架

```
__APP_NAME__/
  .github/workflows/build.yml   CI：打包 + 发 Release（§8）
  .gitignore
  AGENTS.md                     给 AI 的入口说明，指向本规范
  README.md                     英文 README（§9）
  README.zh.md                  中文 README
  dev.md                        开发/发版说明（§6）
  pyproject.toml                §2
  uv.lock                       提交入库
  run.py                        PyInstaller 入口，只转调 __PKG__.__main__:main
  main.spec                     PyInstaller onedir 配置（§7）
  assets/                       icon.ico、icon.png、README 截图
  __PKG__/
    __init__.py                 APP_NAME、__version__
    __main__.py                 main()：日志 → Qt → 主窗口（§3）
    i18n.py                     中英文文案表（§4）
    log.py                      loguru 日志（§5）
    changelog.py                版本历史 + GitHub Releases 检查更新（§6）
    version_dialogs.py          「版本介绍」「检查更新」对话框
    icons.py                    应用图标：assets/icon.ico，找不到就现画
    main_window.py              主窗口、菜单栏
    ...                         业务模块
```

- 仓库名、exe 名、zip 前缀、`APP_NAME` 四者相同（kebab-case）。
- 包名 snake_case；不要在仓库根再放一个 `main.py`，入口只有 `run.py` 和 `python -m __PKG__`。
- `assets/` 不是 `assert/`。演示视频不入库（走 GitHub issue/PR 附件上传得到的 URL），`.gitignore` 里排除 `assets/*.mp4`。

## 2. 工具链

- [uv](https://docs.astral.sh/uv/) 管理 Python 与依赖；`uv.lock` 提交；`.venv/` 在仓库内并忽略。
- `pyproject.toml`：`hatchling` 构建，`[project.scripts]` 暴露 `__APP_NAME__ = "__PKG__.__main__:main"`，这样 `uv pip install -e .` 后命令行可直接运行。
- `requires-python = ">=3.12"`。
- Qt 依赖默认 `PySide6-Essentials`；只有用到 Addons 模块（WebEngine、Multimedia、Charts 等）时才换成 `PySide6`。
- 日志固定用 `loguru`。
- `pyinstaller` 放在 `[dependency-groups] dev`，CI 和本地都用 `uv sync --group dev`。

```toml
[project]
name = "__APP_NAME__"
version = "0.1.0"
description = "__TITLE__"
requires-python = ">=3.12"
dependencies = ["PySide6-Essentials>=6.7", "loguru>=0.7"]

[project.scripts]
__APP_NAME__ = "__PKG__.__main__:main"

[dependency-groups]
dev = ["pyinstaller>=6.10"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["__PKG__"]
```

## 3. 程序入口

`__PKG__/__main__.py` 的 `main(argv=None) -> int`，固定顺序：

1. `setup_logging()` —— 最先，之后任何 import 失败都能进日志。
2. 再 import PySide6 / 业务模块（有原生 DLL 顺序要求的库，如 mujoco，先于 Qt import）。
3. 打一行启动横幅：`APP_NAME vX | python | PySide6 | platform | frozen=`。
4. Windows 下 `SetCurrentProcessExplicitAppUserModelID(f"ccbs.{APP_NAME}")`，任务栏才显示自己的图标。
5. `QApplication`，`setOrganizationName("ccbs")`，`setApplicationName(APP_NAME)`，`setApplicationVersion`，`setStyle("Fusion")`，`setFont(QFont("Microsoft YaHei UI", 9))`。
6. `i18n.load()`（必须在 QApplication 之后，QSettings 才有组织/应用名）。
7. `app.setWindowIcon(app_icon())`，创建 `MainWindow`，`show()`，`exec()`，记录退出码。

`run.py` 只有三行，内容见模板。`QSettings` 组织名统一小写 `ccbs`。

## 4. 界面文案（i18n）

所有界面文字集中在 `__PKG__/i18n.py` 的 `_STRINGS`，`en` / `zh` 两张表键必须一致。

```python
_STRINGS = {
    "en": {"app.title": "...", "menu.file": "&File", "status.loaded": "Loaded {name}"},
    "zh": {"app.title": "...", "menu.file": "文件(&F)", "status.loaded": "已加载 {name}"},
}

# 使用
from .i18n import tr, i18n
label.setText(tr("status.loaded", name=path.name))
i18n.languageChanged.connect(self.retranslate)   # 每个含文案的控件类都有 retranslate()
```

- 键名 `模块.含义`：`menu.*`、`tb.*`（工具栏）、`dialog.*`、`status.*`、`panel.*`、`chg.*` / `upd.*`（版本对话框，模板已带）。
- 默认语言跟随系统：`QLocale.system().language() == Chinese` → `zh`，否则 `en`；用户选过的语言存 QSettings 键 `language`。
- 语言菜单中每种语言用自己的名字显示（`English` / `中文（简体）`），不随当前语言翻译。
- 构造函数里只建控件，所有 `setText/setTitle/setToolTip` 放在 `retranslate()` 中，构造末尾调一次。
- 快捷键助记符：英文 `&File`，中文 `文件(&F)`。

## 5. 日志

`__PKG__/log.py`，直接用模板，不要改结构。

- 路径：`%APPDATA%\ccbs\__APP_NAME__\logs\app.log`（无 `APPDATA` 时退到 `~`）。其他运行时文件（配置、缓存）也放 `%APPDATA%\ccbs\__APP_NAME__\` 下。
- 10 MB 轮转，保留 3 个文件；文件 sink `DEBUG`，控制台 sink `INFO`。
- `enqueue=True`（后台线程安全）、`backtrace=False`、`diagnose=False`（不 dump 局部变量，防泄露密钥）。
- `setup_logging()` 幂等，返回日志路径；接管 `sys.excepthook`、Qt 消息（`qInstallMessageHandler`）、stdlib `logging`（第三方库日志并入）。
- PyInstaller `--windowed` 下 `sys.stderr is None`，不加控制台 sink。
- **日志文本一律英文**，不走 i18n；界面文案才分中英。
- 不记录密码、口令、解密后的任何秘密。
- 用 loguru 的 `{}` 占位：`logger.info("loaded {} ({} triangles)", path, n)`。
- 帮助菜单提供「打开日志目录」。

## 6. 版本、变更记录与检查更新

版本号有三处，发版时一起改并保持一致：

1. `__PKG__/__init__.py` 的 `__version__`（程序内显示、检查更新比较用）。
2. `pyproject.toml` 的 `version`（CI 用它命名 zip）。
3. `__PKG__/changelog.py` 的 `RELEASES`：最前面加一条，`notes` 中英文都要写。

```python
RELEASES = (
    {"version": "0.2.0", "date": "2026-11-06",
     "notes": {"zh": ["帮助菜单：版本介绍、检查更新。"],
               "en": ["Help menu: version info and update check."]}},
    ...
)
```

CI 在推 tag 时校验三处一致，不一致直接失败。

检查更新（模板 `changelog.py` 已实现，不要重写）：

- 两种方式并发竞速：HEAD `https://github.com/<repo>/releases/latest` 跟随 302 取 tag（不占 API 配额）；GET `api.github.com/repos/<repo>/releases/latest`（未登录 60 次/小时，共享出口 IP 容易 403）。谁先成功用谁。
- 总预算 `UPDATE_CHECK_TIMEOUT_S = 20`，对话框倒计时与之一致。
- 下载资源名 `ASSET_NAME_FMT = "__APP_NAME__-v{ver}-windows-x64.zip"`，必须和 `build.yml` 的 "Package zip" 一致。
- `RELEASE_REPO` 指向**发 Release 的仓库**：源码公开则就是本仓库；源码私有则是 `ccbs-tools/__APP_NAME__-release`（见 §8）。

帮助菜单固定项：仓库主页、（可选）视频教程、分隔线、版本介绍、检查更新、打开日志目录。

## 7. 打包（PyInstaller）

`main.spec` 用模板，onedir 模式（启动快、杀软误报少）：

- 入口 `run.py`，`hiddenimports=['__PKG__']`，`datas` 带 `assets/icon.ico`、`assets/icon.png`。
- `excludes` 列出用不到的 Qt 模块（WebEngine、Qml/Quick、Multimedia、Pdf、Charts、3D、Bluetooth、Sql、Test、Designer…）和 `tkinter/matplotlib/IPython/pytest`。3D 工具保留 `QtOpenGL`/`QtOpenGLWidgets`，纯 Widgets 工具可一并排除。
- `upx=False`：Qt / mujoco 的 DLL 压缩后容易崩。
- `console=False`。
- `contents_directory='__APP_NAME__-lib'`：PyInstaller 6 默认 `_internal`，改成带应用名的目录，多个工具解压到同一文件夹时不互相覆盖。
- 带原生插件目录的库（mujoco、glfw）用 `PyInstaller.utils.hooks.collect_all` 收齐。
- 本地打包：`uv run pyinstaller main.spec --noconfirm` → `dist/__APP_NAME__/__APP_NAME__.exe`。

## 8. CI 与发布

`.github/workflows/build.yml`（模板），`windows-latest`：

- 触发：`workflow_dispatch`（只打包，产物进 Artifacts 保留 7 天）和 `push tags: v*`（打包并发 Release）。
- 步骤：checkout → `astral-sh/setup-uv`（开缓存）→ `uv sync --group dev` → 解析版本（tag 去 `v`；手动触发用 pyproject 版本 + 短 sha）→ tag 时校验三处版本一致 → `uv run pyinstaller main.spec` → `Compress-Archive` 成 `__APP_NAME__-v<ver>-windows-x64.zip` → 上传 Artifact → tag 时用 `changelog.py` 生成中英双语 `RELEASE_NOTES.md` → `sha256sum` 生成 `SHA256SUMS.txt` → `gh release create`。
- 生成 notes 的步骤设 `PYTHONUTF8=1`，否则 Windows runner 打印中文崩。
- 发布目标二选一：
  - **源码公开**：发到本仓库，`permissions: contents: write`，用 `github.token`。用 `templates/.github/workflows/build.yml`。
  - **源码私有**：发到公开仓库 `ccbs-tools/__APP_NAME__-release`。本仓库 `contents: read`，通过 GitHub App `ccbs-release-bot` 换 token（Secrets：`RELEASE_APP_ID`、`RELEASE_APP_PRIVATE_KEY`；App 安装在组织并勾选该 release 仓库，权限 Contents: Read and write）。空仓库没有默认分支会导致建 Release 失败，工作流先推一个 README 初始化。用 `templates/.github/workflows/build.release-repo.yml`（改名为 `build.yml`）。
- 发版命令：

```powershell
git tag v0.1.1
git push origin v0.1.1
```

## 9. 文档

- `README.md` 英文为主，首行标题，第二行 `**English** | [中文](README.zh.md)`；`README.zh.md` 对应 `[English](README.md) | **中文**`。两份内容对齐。
- 章节顺序：一句话简介 → 两张截图并排表格（`assets/soft-empty-view.png` 空窗口 / `assets/open-xxx-view.png` 加载后）→ `### Demo` 视频链接 → 依赖一行 → Download（Releases 链接 + zip 名 + SHA256SUMS）→ Install（uv）→ Run → Controls / Usage → Package (onedir) → Structure（目录注释）。
- `dev.md`：环境、运行时文件位置表、目录说明、文案规范、发版三处版本号。
- 代码注释与 docstring 用中文；日志英文（§5）。

## 10. 代码风格

- 每个模块 `from __future__ import annotations`；类型注解；模块级 `__all__` 可选。
- 文件顶部 docstring 说明模块职责与用法。
- 后台工作用 `threading.Thread(daemon=True)` 或 `QThread`，结果通过 Qt `Signal` 回主线程；长寿命 worker 不挂 Qt parent，用模块级集合持有引用，避免对话框关闭后 "Signal source has been deleted"。
- 用户可见的错误走 `tr()`；异常细节进日志。
- 不写测试框架依赖进运行时；小工具可不带测试，但要能 `python -m __PKG__` 跑起来。

## 11. 3D / 几何类工具附加约定

适用于处理 STL / URDF / 点云等的工具：

- 原点画 XYZ 三色轴：红 X、绿 Y、蓝 Z；地面网格可开关；Z 轴朝上的转台式相机。
- 鼠标：左键旋转、右键 / 中键平移、滚轮缩放；双击或 `R` 复位。
- 键盘：`F` 适配视图、`W` 线框、`G` 网格、`A` 坐标轴、`Ctrl+O` 打开。
- 支持把文件拖进整个窗口（含菜单栏、状态栏），`MainWindow` 转交给视口控件。
- 状态栏显示：文件名、三角面数、包围盒、推测单位（尺寸 > 5 视为 mm）。
- `QSurfaceFormat` 在 `QApplication` 之前设置：4x MSAA、24 位深度、CompatibilityProfile。

## 12. 新建项目清单

详细步骤由 Skill `ccbs-new-tool` 执行；人工操作时：

1. 复制 `templates/` 到新目录，重命名 `__PKG__/`，全局替换占位符（§0）。
2. 决定发布目标（§8），选对 `build.yml`，填 `RELEASE_REPO`。
3. 放 `assets/icon.ico` + `icon.png`（没有就先用模板画的回退图标）。
4. `uv sync --group dev` → `uv run python -m __PKG__` 能弹出空窗口并能切换语言。
5. `uv run pyinstaller main.spec --noconfirm` 能出 exe。
6. 写 `RELEASES` 第一条 `0.1.0`，补 README 截图与 Controls。
7. `git init`，首个提交，推到 `ccbs-tools/__APP_NAME__`。

## 13. 老项目与本规范的已知差异

修改老项目时不要求一次性对齐，但新增代码按本规范写；遇到下列差异以本规范为准：

- `mstsc-manager`：根目录 `main.py` 入口、`[tool.uv] package = false`（规范：`run.py` + hatchling）；日志目录 `%APPDATA%\mstsc-manager\`（规范多一层 `ccbs\`）；中文 README 叫 `README_zh.md`。
- `stl-frame-editor`：日志目录 `~/.ccbs/stl-frame-editor/`；日志文本中文；截图目录 `assert/`；CI 用 pip 而非 uv；`requires-python >=3.10`；默认语言固定英文。
- `urdf-inspector`：已对齐（2026-11-08）。

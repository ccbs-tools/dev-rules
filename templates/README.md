# __APP_TITLE_EN__ (__APP_NAME__)

**English** | [中文](README.zh.md)

One-paragraph description: what the tool does, who it is for, the main workflow.
The menu bar switches between English and Chinese at runtime.

| Empty window | After loading |
|---|---|
| ![Empty view](assets/soft-empty-view.png) | ![Loaded view](assets/open-xxx-view.png) |

### Demo

(Upload the video as a GitHub issue/PR attachment and paste the URL here.)

Dependencies: PySide6, loguru.

## Download

Grab the latest `__APP_NAME__-vX.Y.Z-windows-x64.zip` from [Releases](../../releases), unzip anywhere and run
`__APP_NAME__.exe`. No installation required; `SHA256SUMS.txt` next to it lets you verify the download.

Requirements: Windows 10/11 x64.

## Run from source

Needs [uv](https://docs.astral.sh/uv/) (it will fetch Python itself):

```powershell
git clone https://github.com/__GH_ORG__/__APP_NAME__.git
cd __APP_NAME__
uv sync
uv run python -m __PKG__
```

## Usage

1. ...
2. ...

Keyboard: `Ctrl+O` open · ...

## Package (onedir)

```powershell
uv sync --group dev
uv run pyinstaller main.spec --noconfirm
# Output: dist/__APP_NAME__/__APP_NAME__.exe, with dependencies alongside it
```

## Structure

```
__PKG__/
  __main__.py        entry point main()
  main_window.py     main window, menus
  i18n.py            language strings and runtime switching
  log.py             loguru logging
  changelog.py       version history + update check
run.py               PyInstaller entry
main.spec            PyInstaller config
```

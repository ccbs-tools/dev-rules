# __APP_TITLE_ZH__（__APP_NAME__）

[English](README.md) | **中文**

一段话说明：工具做什么、给谁用、主要流程。菜单栏支持中英文实时切换。

| 空窗口 | 加载后 |
|---|---|
| ![空视图](assets/soft-empty-view.png) | ![加载视图](assets/open-xxx-view.png) |

### 演示

（把视频作为 GitHub issue/PR 附件上传，把得到的地址贴在这里。）

依赖：PySide6、loguru。

## 下载

到 [Releases](../../releases) 下载最新的 `__APP_NAME__-vX.Y.Z-windows-x64.zip`，解压到任意位置运行
`__APP_NAME__.exe`。免安装；旁边的 `SHA256SUMS.txt` 可用来校验。

要求：Windows 10/11 x64。

## 源码运行

需要 [uv](https://docs.astral.sh/uv/)（会自动下载 Python）：

```powershell
git clone https://github.com/__GH_ORG__/__APP_NAME__.git
cd __APP_NAME__
uv sync
uv run python -m __PKG__
```

## 使用

1. ...
2. ...

快捷键：`Ctrl+O` 打开 · ...

## 打包（onedir）

```powershell
uv sync --group dev
uv run pyinstaller main.spec --noconfirm
# 输出 dist/__APP_NAME__/__APP_NAME__.exe，依赖在同目录下
```

## 结构

```
__PKG__/
  __main__.py        入口 main()
  main_window.py     主窗口、菜单
  i18n.py            多语言字符串与运行时切换
  log.py             loguru 日志
  changelog.py       版本历史 + 检查更新
run.py               PyInstaller 入口
main.spec            PyInstaller 配置
```

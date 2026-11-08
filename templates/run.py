"""PyInstaller 打包入口（等价于 python -m __PKG__）。"""

from __PKG__.__main__ import main

if __name__ == "__main__":
    raise SystemExit(main())

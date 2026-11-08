# dev-rules

`ccbs-tools` 组织下 Python + PySide6 桌面小工具的统一开发规范、项目模板，以及给 Cursor 用的规则与 Skill。

```
CONVENTIONS.md                      规范正文（规则 + 理由 + 最小示例）
templates/                          新项目模板；占位符见 CONVENTIONS.md §0
  __PKG__/                          包目录（重命名）
  .github/workflows/build.yml       CI：源码公开，Release 发本仓库
  .github/workflows/build.release-repo.yml
                                    CI：源码私有，Release 发到 <name>-release 公开仓库
cursor/
  rules/ccbs-conventions.mdc        Cursor 规则（alwaysApply，很薄，指向 CONVENTIONS.md）
  skills/ccbs-new-tool/SKILL.md     Cursor Skill：按模板新建项目
install.ps1                         在工作区根创建 .cursor/rules、.cursor/skills 到 cursor/ 的目录联接
```

## 安装（每台机器一次）

把本仓库 clone 到各工具仓库的同级目录（例如 `D:\code\projects\ccbs-tools\dev-rules`），然后：

```powershell
cd dev-rules
.\install.ps1
```

脚本在父目录创建 `.cursor\rules` → `dev-rules\cursor\rules`、`.cursor\skills` → `dev-rules\cursor\skills` 两个目录联接（junction，不需要管理员权限）。以父目录为工作区打开 Cursor 时，规则对所有子项目生效，Skill 可用 `ccbs-new-tool` 触发。

各工具仓库里的 `AGENTS.md`（模板已带）指向 `../dev-rules/CONVENTIONS.md`，单独 clone 一个仓库时 AI 也知道去哪找规范。

## 维护

- 规则正文只改 `CONVENTIONS.md`；`cursor/rules/ccbs-conventions.mdc` 保持薄，只放索引和要点。
- 模板文件改动后，在 `/tmp` 下按 Skill 的第 9 步跑一遍验证。
- 老项目与规范的差异记录在 `CONVENTIONS.md` §13，对齐后从那里删掉。

---
name: docx-generation
description: 生成 .docx（Word）文档。当用户要一份 Word 文档、报告、讲义、论文初稿、实验报告，或说"帮我生成/导出 docx/word"时使用。方法：python-docx 跑在 uv 临时 venv 里（纯库、无系统依赖、零污染），模型整理好内容后写脚本拼装成文件。含已验证的生成器模板与全套踩坑解决方案（系统 python 是 Store 占位、脚本须 UTF-8 写盘）。模型本身不能直接吐 .docx 二进制，一律走"文本内容 + python-docx 拼装"这条路。
whenToUse: 用户要求生成/导出 Word 文档（.docx/.doc），或需要报告/讲义/论文/表格等结构化文档落盘时。
---

# docx 生成（python-docx + uv 临时环境）

模型本人**不能**直接输出 `.docx`（只能吐文本）。所有 docx 落地都走同一条路：
**先理清内容结构 → 写一个 python 脚本 → python-docx 拼装 → 存成 .docx**。

## 0. 一句话结论（先看这个）
- 纯库方案：`python-docx`（`lxml` 自动带），跑在 **uv 临时 venv**，不污染全局，用完可删。
- 环境事实（Windows 已验证）：系统 `python` 常指向 WindowsApps 的 Store 占位版，`python -c` 可能 exit 1；**用 `py` 启动器或 uv 管理的 python**。需要 `uv`（`uv --version` 自检）与 Python 3.11+。

## 1. 标准流程（照做一次就成）

```powershell
# 1) 建临时 venv（3.11 更稳）
$d = "$env:TEMP\<临时名>"
uv venv $d --python 3.11

# 2) 装库
uv pip install --python "$d\Scripts\python.exe" python-docx

# 3) 跑生成脚本（注意用 venv 里的 python，别用系统的 python）
$py = "$d\Scripts\python.exe"
& $py "<脚本路径>" "<输出.docx 路径>"

# 4) 读回验证（可选）
$env:PYTHONIOENCODING = 'utf-8'
& $py -c "from docx import Document; d=Document(r'<输出>'); print(len(d.paragraphs), len(d.tables))" "<输出>"
```

## 2. 关键坑（必须记住，否则中文必坏）

**坑 A：写 .py 脚本要显式 UTF-8。**
PowerShell 默认按 GBK 写盘，Python 默认按 UTF-8 读 → 源码里的中文字面量在源头上就变乱码，
生成出来的 docx 中文全坏。解法：
```powershell
# 不要用 Out-File / Set-Content 默认编码，用这个：
[IO.File]::WriteAllText($script, $code, (New-Object Text.UTF8Encoding $false))
```
（脚本文件本身加 `# -*- coding: utf-8 -*-` 首行更保险。）

**坑 B：系统 `python` 是 Store 占位版。**
`python -c` 会 exit 1 且无输出。改用 `py` 启动器或 uv venv 里的 python.exe。

**坑 C：读回中文要在控制台设 UTF-8。**
`$env:PYTHONIOENCODING='utf-8'` 再跑读回，否则 print 中文会乱（这只是控制台显示问题，不是文件坏）。

## 3. 生成器模板

模板源码在 `templates\docx_builder.py`（标题/章节/正文/加粗/斜体/强调块/列表/表格全覆盖）。
用法：复制到临时脚本，往 `build()` 里填内容；或直接改模板里的占位文字。

核心 API 速查：
```python
from docx import Document
doc = Document()
doc.add_heading("标题", 0)                      # 0=Title, 1~9=Heading 级别
doc.add_heading("1.1 小节", level=2)
doc.add_paragraph("正文")                        # 普通段落
p = doc.add_paragraph(); r = p.add_run("加粗"); r.bold = True
doc.add_paragraph("要点", style="Intense Quote") # 强调块
doc.add_paragraph("条目", style="List Bullet")   # 无序列表
t = doc.add_table(rows=2, cols=2); t.style="Table Grid"
t.cell(0,0).text = "值"                          # 单元格赋值
doc.save(out)
```

## 4. 更多控制（按需）
```python
from docx.shared import Pt, RGBColor
run.font.size = Pt(12); run.font.name = "宋体"
run.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)
# 中文正文建议：run.font.name = "宋体"; 并用 r.font._element 设 eastAsia 字体（复杂，一般不必）
```

## 5. 什么时候换更重的工具
- 大量 md → docx、要目录/脚注/交叉引用：走 **pandoc**（Windows 可 `winget install pandoc`）。
- 已有固定模板要填内容：用 `python-docx` 打开模板 `Document("模板.docx")` 后改。
- 只是想看内容不想排版：直接给用户 markdown 文本，让用户自己粘 Word。

## 6. 产出建议路径
生成的 .docx 和脚本输出到用户指定目录（未指定时用工作区下的产出目录）。完成说明里给出文件绝对路径。
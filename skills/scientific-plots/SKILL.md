---
name: scientific-plots
description: 生成学术/科研图表：实验数据曲线+拟合、误差棒、双轴、热图等高线、多面板对比、论文流程示意图。matplotlib+scienceplots 出版级风格、中文不乱码、离线出 PNG/PDF。当用户要画数据图、实验曲线、论文插图、报告配图、流程框图，或提到 matplotlib/科研绘图/学术图表时使用。AI 生图类插画/海报请用 poster-prompt-craft，不要用本技能。
whenToUse: 需要"画图/出图/图表/曲线/拟合/热图/流程图框图"且要求精确数据或学术风格时；实验报告、论文、答辩 PPT 配图时。
---

# 学术图表（matplotlib + scienceplots 出版级管线）

> 出版级科研绘图实战配方（论文与实验报告场景验证，经第三方复现核验）。

## 环境（Windows 实测可用）

- 解释器：**`py` 启动器**或 uv 管理的 Python（3.11+）。**别用系统 `python`**（Windows 上常是 Store 占位版，exit 1）。
- 已装库：matplotlib 3.11.1、scienceplots、numpy 2.5.2、scipy、pandas、openpyxl。**离线可用**。
- 缺库时：`py -m pip install <包名>`。

## 标准文件头（逐行都有理由，别删）

```python
# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use("Agg")            # 无 GUI，纯出文件（批处理/服务必用）
import matplotlib.pyplot as plt
import scienceplots

plt.style.use(["science", "no-latex"])   # 学术风格；no-latex = 不需要装 LaTeX
plt.rcParams["font.family"] = ["sans-serif"]        # 必须覆盖 science 默认的 serif/STIX（不含中文）
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]  # 中文不乱码的关键
plt.rcParams["mathtext.fontset"] = "dejavusans"     # 数学符号用 dejavu，防缺字
plt.rcParams["axes.unicode_minus"] = False          # 不加这条：负号渲染成方块
plt.rcParams["font.size"] = 10
```

## 输出纪律

- `fig.savefig(path, dpi=200)`；草稿出 PNG，**定稿加出 PDF/SVG**（矢量，印刷不糊）。
- 每个 fig 用完立刻 `plt.close(fig)`（防内存泄漏）。
- `fig.tight_layout()` 防标签被裁；仍被裁用 `savefig(..., bbox_inches="tight")`。
- 图例统一 `fontsize=8, frameon=False`。

## 配方 1：数据曲线 + 阈值线 + 事件标注（实验报告核心图）

```python
fig, ax = plt.subplots(figsize=(5.6, 3.8))
ax.plot(t_h, c_center, label="实验组", color="#1f77b4")
ax.plot(t_h2, c_center2, label="对照组", color="#d62728")
ax.axhline(0.15, color="k", ls=":", lw=1, label="判定阈值 0.15")
ax.axvline(t_end, color="#1f77b4", ls="--", lw=0.8, alpha=0.6)
ax.annotate(f"t = {t_end:.2f} h", xy=(t_end, 1.4), fontsize=8, color="#1f77b4", ha="right")
ax.set_xlabel("时间 / h"); ax.set_ylabel("浓度 / (kg/kg)")
ax.legend(fontsize=8, frameon=False)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig_curve.png"), dpi=200); plt.close(fig)
```

## 配方 2：多面板对比（1×2 / 2×1）

```python
fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.6, 3.4))
a1.plot(...); a1.set_title("左图标题", fontsize=9)
a2.plot(...); a2.set_title("右图标题", fontsize=9)
fig.tight_layout(); fig.savefig(..., dpi=200); plt.close(fig)
```

## 配方 3：拟合 + 误差棒

```python
from scipy.optimize import curve_fit
popt, pcov = curve_fit(model, x, y, p0=[初值])
xf = np.linspace(x.min(), x.max(), 300)
ax.plot(xf, model(xf, *popt), "r-", label=f"拟合: k={popt[0]:.3f}")
ax.errorbar(x, y, yerr=err, fmt="o", ms=3, capsize=2, label="实验数据")
```

## 配方 4：热图 / 等高线

```python
im = ax.imshow(Z, extent=[x0, x1, y0, y1], origin="lower", aspect="auto", cmap="viridis")
fig.colorbar(im, ax=ax, label="浓度 / (kg/kg)")
# 或 ax.contourf(X, Y, Z, levels=20, cmap="viridis")
```

## 配方 5：论文流程示意图（FancyBboxPatch 框图，"论文脸"）

低饱和学术配色 + 圆角框 + 箭头。实战验证的 helpers：

```python
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

C_INPUT = ("#eef3fa", "#3b6ea5")   # 输入: 浅蓝
C_MODEL = ("#f5f0e8", "#8a6d3b")   # 模型: 浅暖
C_SOLVE = ("#eef7ee", "#3f7d4e")   # 处理: 浅绿
C_OUTPUT = ("#f2eef7", "#6a4d8f")  # 输出: 浅紫
C_VERIF = ("#fdf0ef", "#a04a44")   # 验证: 浅红

def make_ax(w, h, xlim, ylim):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.axis("off"); ax.set_xlim(0, xlim); ax.set_ylim(0, ylim)
    return fig, ax

def box(ax, x, y, w, h, text, style=C_INPUT, fs=9.4, lw=1.0, ls="-"):
    fc, ec = style
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3",
                                fc=fc, ec=ec, lw=lw, linestyle=ls))
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=fs, linespacing=1.35)

def arrow(ax, x1, y1, x2, y2, color="#555555", ls="-", lw=1.0):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=14, color=color, lw=lw, linestyle=ls))
```

画布用"虚拟坐标"（如 132×78）而非英寸，坐标好算。文字可混排 `$数学$`。

## 读 Excel 实验数据（openpyxl，轻量不引 pandas）

```python
import openpyxl
wb = openpyxl.load_workbook(path, read_only=True)
ws = wb.worksheets[0]
data = [tuple(map(float, row[:2])) for row in ws.iter_rows(min_row=2, values_only=True) if row[0] is not None]
wb.close()
```

## 运行与验收（缺一不可）

1. `py 脚本.py` 运行；脚本开头加 `sys.stdout.reconfigure(encoding="utf-8", errors="replace")`
   （PowerShell 控制台默认 GBK，中文 print 会报错）。
2. **DSH 用 PowerShell 写 .py 文件必须显式 UTF-8**：
   `[IO.File]::WriteAllText($path, $code, (New-Object Text.UTF8Encoding $false))`——
   here-string/Set-Content 默认按 GBK 写盘，Python 按 UTF-8 读 → 中文全成乱码字面量。
3. 出图后 **read_image 目检**：中文是否乱码、负号是否方块、标签是否被裁、图例是否遮挡数据。
4. 数据不许编造：没有数据就明确说"这是占位示例"，让用户提供真实数据。

## 边界

- AI 生图类（插画/海报/梗图/手账）→ skill `poster-prompt-craft` 或 TokenRhythm 生图管线。
- 插入 Word → skill `docx-generation`（插图宽度：单栏 ~3.5in、双栏 ~7in，dpi 200 够用）。
- 本技能模板：`templates/starter.py`（自包含可运行，产出 2 张示例图自证管线）。

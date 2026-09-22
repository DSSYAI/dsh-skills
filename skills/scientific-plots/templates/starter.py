# -*- coding: utf-8 -*-
"""scientific-plots 技能自检模板：不依赖外部数据，跑一遍产出 2 张示例图。

用法：py starter.py [输出目录]
验证点：fig1 中文标签/负号正常、拟合曲线合理；fig2 框图布局整齐、箭头到位。
"""
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import scienceplots
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUT, exist_ok=True)

# ---- 标准风格头（见 SKILL.md） ----
plt.style.use(["science", "no-latex"])
plt.rcParams["font.family"] = ["sans-serif"]
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["mathtext.fontset"] = "dejavusans"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["font.size"] = 10

# ============ fig1: 数据曲线 + 指数拟合 + 阈值线 ============
rng = np.random.default_rng(42)
t = np.linspace(0, 10, 40)
y = 5.0 * np.exp(-0.35 * t) + 0.15 + 0.12 * rng.normal(size=t.size)   # 占位示例数据
noise_scale = np.full_like(y, 0.12)

# 指数拟合 y = a*exp(-k t) + c
from scipy.optimize import curve_fit
model = lambda x, a, k, c: a * np.exp(-k * x) + c
popt, _ = curve_fit(model, t, y, p0=[5.0, 0.3, 0.15])

fig, ax = plt.subplots(figsize=(5.6, 3.8))
ax.errorbar(t, y, yerr=noise_scale, fmt="o", ms=3, capsize=2, color="#1f77b4",
            label="实验数据（示例）")
xf = np.linspace(0, 10, 300)
ax.plot(xf, model(xf, *popt), "r-", lw=1.2,
        label=f"拟合: {popt[0]:.2f}·exp(-{popt[1]:.2f}t)+{popt[2]:.2f}")
ax.axhline(0.15, color="k", ls=":", lw=1, label="判定阈值 0.15")
ax.set_xlabel("时间 / h")
ax.set_ylabel("剩余水分 / (kg/kg)")
ax.set_ylim(0, 6)
ax.legend(fontsize=8, frameon=False)
fig.tight_layout()
p1 = os.path.join(OUT, "fig1_数据曲线示例.png")
fig.savefig(p1, dpi=200)
plt.close(fig)
print("fig1 完成:", p1)

# ============ fig2: 流程示意图（论文脸框图） ============
C_INPUT = ("#eef3fa", "#3b6ea5")
C_SOLVE = ("#eef7ee", "#3f7d4e")
C_OUTPUT = ("#f2eef7", "#6a4d8f")

def make_ax(w, h, xlim, ylim):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.axis("off")
    ax.set_xlim(0, xlim)
    ax.set_ylim(0, ylim)
    return fig, ax

def box(ax, x, y, w, h, text, style, fs=9.4):
    fc, ec = style
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3",
                                fc=fc, ec=ec, lw=1.0))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, linespacing=1.35)

def arrow(ax, x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=14, color="#555555", lw=1.0))

fig, ax = make_ax(7.2, 3.6, 100, 50)
box(ax, 5, 36, 90, 10, "输入：实验数据（xlsx / 手动录入）\nopenpyxl 读取 → numpy 数组", C_INPUT, fs=10)
arrow(ax, 50, 36, 50, 31)
box(ax, 5, 20, 90, 11,
    "处理：$matplotlib$ + scienceplots 学术风格\n"
    "曲线/拟合/误差棒 ｜ 热图等高线 ｜ 多面板对比", C_SOLVE, fs=10)
arrow(ax, 50, 20, 50, 15)
box(ax, 5, 4, 90, 11,
    "输出：PNG（dpi=200 草稿）＋ PDF/SVG（矢量定稿）\n"
    "负号不缺字 · 中文 SimHei · tight_layout 防裁切", C_OUTPUT, fs=10)

p2 = os.path.join(OUT, "fig2_流程示意图.png")
fig.savefig(p2, dpi=200)
plt.close(fig)
print("fig2 完成:", p2)
print("全部完成，输出目录:", OUT)

# DSH 技能包（4 个自建技能）

给 DSH（DeepSeek Harness）用的技能。把这几个目录复制进 DSH 的技能目录，新开一个会话即可按技能名调用。

包内**已清除个人与机器特有信息**（绝对路径、项目记录、工作区专有目录名）；技能内不含任何固定绝对路径，产出目录由调用方指定。

## 安装

把 `skills\` 下各技能目录**整体**复制到：

```text
%USERPROFILE%\.dsh\skills\
```

复制后的结构应为 `%USERPROFILE%\.dsh\skills\<技能名>\SKILL.md`。DSH 会在新会话开始时重新扫描技能目录。

## 技能清单

| 技能 | 用途 | 依赖 |
|---|---|---|
| `docx-generation` | 生成 .docx（Word）：报告、讲义、论文初稿、实验报告 | `uv`（脚本内自动建临时 venv 装 python-docx）；Python 3.11+ |
| `scientific-plots` | 学术科研图表：曲线拟合、误差棒、热图等高线、多面板、论文流程框图 | Python 3.11+ 且装有 matplotlib、scienceplots、numpy、scipy、pandas、openpyxl；中文显示需系统有 SimHei 或 Microsoft YaHei |
| `poster-prompt-craft` | 知识卡片／手账海报类提示词，含全自动出图流程 | 一个图像生成 API（默认按 TokenRhythm 的 `images/generations` 写） |
| `reverse-engineering-and-patching` | 接手陌生软件/项目并做逆向分析与功能改造的通用工作流：环境侦察、入口定位、全量审计、机制求证、最小改动实施、产物验证、交付记录 | 无（纯方法论，配合语言/框架自身的工具链使用） |

## 使用前请注意

- **文档类技能**之所以走 `uv` 临时 venv：纯库、无系统依赖、不污染机器上的 Python；模型本身不能直接吐 .docx 二进制，一律走"文本内容 + python-docx 拼装"。
- **图像服务商**：`poster-prompt-craft` 内默认写死了 TokenRhythm 的接口与模型名（qwen-image-2.0 / wan2.7-image）。
  目标机器若没有该服务，需把 SKILL.md 里的 endpoint、模型名、鉴权方式换成自有渠道；API key 按 DSH 惯例放 `~/.dsh/.credentials.yaml`。
- **字体**：`scientific-plots` 的中文渲染依赖 SimHei / Microsoft YaHei（Windows 自带）。非 Windows 机器需改 `plt.rcParams["font.sans-serif"]`。
- **Python 解释器**：Windows 上系统 `python` 常是应用商店占位版（`python -c` 直接失败），技能里统一用 `py` 启动器或 uv 管理的解释器。

## 不在本仓库里的那个技能

`image-prompt-reverse`（从参考图反推生图提示词）是**第三方作品**，作者 [LunarXuan](https://github.com/LunarXuan/image-prompt-reverse)，许可 **GPL-3.0**。
本仓库不再分发它，需要请去上游取。其 README 里的安装路径写的是 Codex（`.codex\skills\`），装到 DSH 请改用 `~/.dsh/skills/`。

## 许可

本仓库四个技能均为自建，MIT 许可，见 [LICENSE](LICENSE)。
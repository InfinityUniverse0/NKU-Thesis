# 南开大学本科毕业论文 LaTeX 模板

本项目为南开大学本科毕业论文 LaTeX 模板，主要参考：

- 《南开大学本科毕业论文（设计）指导手册（2025）》
- 《本科生论文格式要求补充规定2023V2》

模板专门针对**计算机学院**和**密码与网络空间安全学院**的本科毕业论文格式要求定制，**不一定符合其他学院的要求**。其他学院使用时，可能需要进行对应修改；具体格式请以所在学院当年发布的要求为准。

当前示例中的个人信息均为占位内容，正文为简短使用说明，正式提交前请替换。

> [!NOTE]
>
> 最新模板可前往 GitHub [NKU-Thesis](https://github.com/InfinityUniverse0/NKU-Thesis) 获取。

## 目录结构

```text
NKU-Thesis/
├── main.tex                 # 编译入口、宏包配置和封面信息
├── NKUThesis.sty            # 页面、字体、标题等排版设置
├── NKUThesis.bbx            # 参考文献样式
├── NKUThesis.cbx            # 文中引用样式
├── references.bib           # 参考文献数据库
├── fonts/                   # 模板所需字体
├── assets/
│   └── NankaiUniv.pdf       # 校名视觉资源（本科论文封面无需引用）
├── figures/                 # 论文插图
└── tex/
    ├── abstract.tex         # 中英文摘要和关键词
    ├── body.tex             # 正文
    ├── appendix.tex         # 附录
    └── acknowledgements.tex # 致谢
```

## 编译

使用 **XeLaTeX + Biber**，建议安装较新的完整版 TeX Live 或 MacTeX。字体直接从 `fonts/` 读取，请保留文件名大小写。

在项目根目录运行：

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error main.tex
```

生成的文件为 `main.pdf`。也可以手动编译：

```bash
xelatex main.tex
biber main
xelatex main.tex
xelatex main.tex
```

参考文献由 Biber 处理。若更换文件名或文献后仍出现旧的目录、引用，可清理辅助文件后重新编译：

```bash
latexmk -c main.tex
```

在 Overleaf 中上传整个项目，将主文档设为 `main.tex`、编译器设为 **XeLaTeX**。

## 开始撰写

1. 修改 `main.tex` 中的 `\NKTsetup{...}`，填写题目、姓名、学号、学院、导师及日期。示例中的 `0000000`、`0000` 等占位信息及完成月份均需按实际情况修改。不需要第二行标题或校外导师时填“无”。
2. 修改 `tex/abstract.tex` 的中英文摘要及关键词。
3. 在 `tex/body.tex` 撰写正文，使用 `\chapter`、`\section`、`\subsection` 组织标题；示例展示了图、表、公式、定义和程序代码。
4. 将插图放入 `figures/`，将文献条目写入 `references.bib`，用 `\cite{条目键}` 或 `\upcite{条目键}` 引用，推荐用 `\upcite{条目键}` 作上标引用，例如 `\upcite{ZW-AQTZ}`（中文）和 `\upcite{BERT}`（英文）。多个条目可写为 `\upcite{ZW-AQTZ,BERT}`。
5. 修改附录 `tex/appendix.tex` 和致谢 `tex/acknowledgements.tex`；不需要附录时，注释 `main.tex` 中的 `\include{tex/appendix}`。

当前编排顺序为：**封面与声明、摘要、目录、正文、附录、参考文献、致谢**。本模板的附录用法为 `\appendix{附录标题}`，直接在 `tex/appendix.tex` 中使用；页码接续正文。

普通程序代码使用 `lstlisting`，默认为五号字、单倍行距，带浅色背景、边框、左侧行号和语法高亮。用 `language=Python`、`language=C++` 或 `language=bash` 指定语言；外部代码可通过 `\lstinputlisting[language=Python]{文件路径}` 引入。代码外观在 `main.tex` 的 `\lstset` 中统一设置。

算法伪代码使用 `algorithm` 和 `algorithmic`，使用的模型提示词可使用 `promptbox` 和 `verbatim`，这些内容保留小四号字。一般无需在正文中手动修改字号、行距或页码。

## 许可

Copyright (c) 2026 **InfinityUniverse0**，适用于本改编版的原创内容及修改；上游内容保留原版权归属和许可声明。

模板源码及配套说明按 **LaTeX Project Public License（LPPL）1.3 或后续版本**分发和修改，仓库中的 [LICENSE](LICENSE) 为 LPPL **1.3c** 全文。

本改编版的维护状态为 `maintained`，当前维护者为 **InfinityUniverse0**。问题反馈与修改建议请提交至[本项目 Issues](https://github.com/InfinityUniverse0/NKU-Thesis/issues)，不应将本改编版的问题默认交由上游作者处理。

`fonts/` 中的第三方字体和 `assets/` 中的校名资源**不在本项目的 LPPL 授权范围内**；其再分发授权仍需单独确认。使用本模板撰写的论文不会仅因使用模板而自动采用 LPPL。

## 致谢

本模板在 [NKThesis by Tr0py](https://tr0py.github.io/NKU-thesis-template-2020/) 的基础上，按照南开大学毕业论文最新要求以及计算机学院和密码与网络空间安全学院的本科毕业论文格式要求修改而来。在此对开源并维护 [NKThesis by Tr0py](https://tr0py.github.io/NKU-thesis-template-2020/) 项目的学长学姐表示感谢。

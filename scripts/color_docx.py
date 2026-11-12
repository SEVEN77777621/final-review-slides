#!/usr/bin/env python3
"""五色记忆编码 Word(.docx) 样式辅助库。

复刻儿科学彩色速记讲义的配色语义，供 final-review-slides 生成可在
Microsoft Word 直接打开、编辑的 .docx 讲义：

  蓝 concept   基础概念   绿 number    必背数字
  橙 mechanism 机制逻辑   红 trap      高频坑点
  黄 conclusion 核心结论

用法（作为模块）：
    from color_docx import build_document, COLORS
    doc = build_document("讲义标题")
    add_tag(doc, "concept", "胎儿期：受精卵到出生。", label="概念")
    add_box(doc, "trap", "坑点", ["围生期：孕28周～产后1周，死亡率最高。"])
    doc.save("review.docx")

直接运行：生成一份带样例内容的 color-handout-sample.docx。
"""

from __future__ import annotations
import sys
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# kind -> (深色文字/边框, 浅色底纹)；与 color-style.tex、HTML 模板共用同一组 hex
COLORS = {
    "concept":    ("3A6EA5", "EAF2FA"),
    "number":     ("2E9E6B", "E7F4EC"),
    "mechanism":  ("E08A3C", "FBEFE1"),
    "trap":       ("CF5148", "FBECEA"),
    "conclusion": ("A8842A", "FCF4DB"),
}

DEFAULT_LABEL = {
    "concept": "概念",
    "number": "数字",
    "mechanism": "机制",
    "trap": "坑点",
    "conclusion": "结论",
}


def _hex(kind: str) -> tuple[str, str]:
    if kind not in COLORS:
        raise ValueError(f"未知颜色类型: {kind}（可选 {list(COLORS)}）")
    return COLORS[kind]


def _shade_pr(pr_element, fill: str) -> None:
    """给 pPr / tcPr 元素加底纹。"""
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    pr_element.append(shd)


def shade_paragraph(paragraph, fill: str) -> None:
    _shade_pr(paragraph._p.get_or_add_pPr(), fill)


def shade_cell(cell, fill: str) -> None:
    _shade_pr(cell._tc.get_or_add_tcPr(), fill)


def set_cell_border(cell, color: str, sz: str = "8") -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), sz)
        e.set(qn("w:space"), "0")
        e.set(qn("w:color"), color)
        borders.append(e)
    tc_pr.append(borders)


def _styled_run(paragraph, text: str, dark: str, bold: bool = True, size: int = 11):
    run = paragraph.add_run(text)
    run.bold = bold
    run.font.size = Pt(size)
    run.font.color.rgb = RGBColor.from_string(dark)
    run.font.name = "Microsoft YaHei"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")
    return run


def set_default_font(doc: Document) -> None:
    style = doc.styles["Normal"]
    style.font.name = "Microsoft YaHei"
    style.font.size = Pt(11)
    style.element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")


def add_tag(doc: Document, kind: str, text: str, label: str | None = None,
            size: int = 11):
    """单条彩色标签段落：浅底纹 + 深色加粗标签 + 正文。"""
    dark, bg = _hex(kind)
    label = label or DEFAULT_LABEL[kind]
    p = doc.add_paragraph()
    shade_paragraph(p, bg)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.left_indent = Cm(0.2)
    _styled_run(p, f"{label} ", dark, bold=True, size=size)
    body = p.add_run(text)
    body.font.size = Pt(size)
    body.font.name = "Microsoft YaHei"
    body._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")
    return p


def badge(paragraph, text: str) -> None:
    """在段落末尾追加绿色数字徽章。"""
    dark, bg = COLORS["number"]
    run = _styled_run(paragraph, f" {text} ", dark, bold=True, size=10.5)
    # 徽章底纹挂在 run 上（w:shd in rPr）
    rpr = run._element.get_or_add_rPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), bg)
    rpr.append(shd)


def add_box(doc: Document, kind: str, title: str, lines: list[str],
            size: int = 11) -> None:
    """彩色框（坑点红框 / 结论黄条 / 机制橙框），用单格表格实现边框。"""
    dark, bg = _hex(kind)
    table = doc.add_table(rows=1, cols=1)
    table.autofit = True
    cell = table.cell(0, 0)
    shade_cell(cell, bg)
    set_cell_border(cell, dark)
    cell.paragraphs[0].text = ""
    head = cell.paragraphs[0]
    _styled_run(head, f"{title}  ", dark, bold=True, size=size)
    head.add_run(lines[0] if lines else "")
    for line in lines[1:]:
        p = cell.add_paragraph()
        p.add_run(line).font.size = Pt(size)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def add_heading(doc: Document, text: str, color_kind: str | None = None) -> None:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(6)
    if color_kind:
        dark, _ = _hex(color_kind)
        _styled_run(p, text, dark, bold=True, size=14)
    else:
        _styled_run(p, text, "1F2730", bold=True, size=14)


def build_document(title: str) -> Document:
    doc = Document()
    set_default_font(doc)
    sec = doc.sections[0]
    sec.top_margin = Cm(2.0)
    sec.bottom_margin = Cm(2.0)
    sec.left_margin = Cm(2.0)
    sec.right_margin = Cm(2.0)
    h = doc.add_paragraph()
    _styled_run(h, title, "1F2730", bold=True, size=18)
    # 图例
    legend = doc.add_paragraph()
    for kind, label in DEFAULT_LABEL.items():
        dark, bg = COLORS[kind]
        r = _styled_run(legend, f" {label} ", dark, bold=True, size=10)
        rpr = r._element.get_or_add_rPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), bg)
        rpr.append(shd)
        legend.add_run("  ")
    return doc


def _sample() -> Document:
    doc = build_document("儿科学 · 前20页彩色速记（Word 样例）")
    add_heading(doc, "一、小儿年龄七期", "concept")
    add_tag(doc, "concept", "胎儿期：受精卵到出生；前12周易流产、畸形。")
    p = add_tag(doc, "number", "婴儿期（0–1岁）：生长发育第一高峰，母体 IgG 消耗易感染。")
    badge(p, "0–1 岁")
    add_box(doc, "trap", "坑点", [
        "围生期：孕28周～产后1周，发病率与死亡率最高，是衡量地区医疗水平的指标。",
    ])
    add_heading(doc, "二、维生素D缺乏性佝偻病", "mechanism")
    add_box(doc, "mechanism", "机制", [
        "VD不足 → 肠钙吸收下降 → 血钙下降 → 甲状旁腺代偿溶骨保钙 → 骨骼软化变形。",
    ])
    add_box(doc, "conclusion", "结论", [
        "初期闹惊汗痒秃、无骨骼改变；激期出现方颅、手镯脚镯、鸡胸/OX腿，X线杯口毛刷状。",
    ])
    return doc


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "color-handout-sample.docx"
    _sample().save(out)
    print(f"saved: {out}")

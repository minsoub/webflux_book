#!/usr/bin/env python3
"""
Spring Boot WebFlux + MongoDB 책 DOCX 빌드 스크립트

B5(46배판) 부크크 서식으로 books.md → DOCX 변환

사용법:
    python3 build_docx.py

필수 의존성:
    pip3 install lxml
    pandoc (시스템에 설치되어 있어야 함)

빌드 과정:
    1. pandoc 기본 reference.docx 추출
    2. 테마 폰트를 부크크 폰트로 변경
    3. 스타일 수정 (본문 10pt, 코드 7.5pt, 제목 부크크 고딕)
    4. B5 페이지 크기 및 여백 설정
    5. pandoc으로 markdown → docx 변환
    6. 테이블 후처리 (테두리, 컬럼 너비, 고정 레이아웃)
    7. 앞부분 추가 (속표지, 판권, 목차)
"""

import zipfile
import shutil
import os
import re
import subprocess
import tempfile
from pathlib import Path
from lxml import etree

# ============================================================
# 설정 (필요에 따라 수정)
# ============================================================
BOOK_TITLE = "Spring Boot WebFlux + MongoDB"
BOOK_SUBTITLE = "리액티브 프로그래밍으로 구현하는 고성능 웹 애플리케이션"
AUTHOR = "정민섭"
PUB_DATE = "2026년 02월"

# 경로 설정 - 스크립트 위치 기준 상대 경로
SCRIPT_DIR = Path(__file__).resolve().parent
BOOKS_MD = SCRIPT_DIR / "books.md"
OUTPUT_DOCX = SCRIPT_DIR / "SpringBoot_WebFlux_MongoDB_B5.docx"

# 임시 작업 디렉토리 (빌드 중 사용, 빌드 후 자동 삭제)
WORK_DIR = SCRIPT_DIR / ".build_tmp"
REF_UNPACKED = WORK_DIR / "unpacked_ref"
OUTPUT_REF = WORK_DIR / "bookk_ref.docx"

# 폰트 설정
BODY_FONT = "부크크 명조 Light"
HEAD_FONT = "부크크 고딕 Light"
INFO_FONT = "바탕"

# 페이지 설정 (B5 46배판 + 3mm 재단 여백)
PAGE_W = "10660"      # 188mm in DXA
PAGE_H = "14912"      # 263mm in DXA
MARGIN_TOP = "1418"
MARGIN_RIGHT = "1418"
MARGIN_BOTTOM = "2268"
MARGIN_LEFT = "1418"
MARGIN_HEADER = "851"
MARGIN_FOOTER = "907"
MARGIN_GUTTER = "284"
# 콘텐츠 너비: 10660 - 1418 - 1418 - 284 = 7540 DXA
PAGE_CONTENT_WIDTH = 7540

# ============================================================
# XML 네임스페이스
# ============================================================
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def qn(ns, tag):
    """Create qualified XML name."""
    return f"{{{ns}}}{tag}"


# ============================================================
# Step 1: pandoc 기본 reference.docx 추출
# ============================================================
def extract_pandoc_reference():
    """Extract pandoc's default reference.docx for modification."""
    if WORK_DIR.exists():
        shutil.rmtree(str(WORK_DIR))
    WORK_DIR.mkdir(parents=True)
    REF_UNPACKED.mkdir()

    # Export pandoc default reference
    default_ref = WORK_DIR / "default_ref.docx"
    result = subprocess.run(
        ["pandoc", "--print-default-data-file", "reference.docx"],
        capture_output=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to extract pandoc reference: {result.stderr.decode()}")
    default_ref.write_bytes(result.stdout)

    # Unpack
    with zipfile.ZipFile(str(default_ref), 'r') as zf:
        zf.extractall(str(REF_UNPACKED))

    print("✓ Pandoc default reference extracted")


# ============================================================
# Step 2: 테마 폰트 수정
# ============================================================
def modify_theme():
    """Change theme fonts to 부크크 fonts."""
    theme_path = REF_UNPACKED / "word/theme/theme1.xml"
    tree = etree.parse(str(theme_path))
    root = tree.getroot()
    nsmap = {"a": A_NS}

    # Major font (headings) -> 부크크 고딕 Light
    major = root.find(".//a:fontScheme/a:majorFont", nsmap)
    if major is not None:
        latin = major.find("a:latin", nsmap)
        if latin is not None:
            latin.set("typeface", HEAD_FONT)
        ea = major.find("a:ea", nsmap)
        if ea is not None:
            ea.set("typeface", HEAD_FONT)
        for font in major.findall("a:font", nsmap):
            if font.get("script") == "Hang":
                font.set("typeface", HEAD_FONT)

    # Minor font (body) -> 부크크 명조 Light
    minor = root.find(".//a:fontScheme/a:minorFont", nsmap)
    if minor is not None:
        latin = minor.find("a:latin", nsmap)
        if latin is not None:
            latin.set("typeface", BODY_FONT)
        ea = minor.find("a:ea", nsmap)
        if ea is not None:
            ea.set("typeface", BODY_FONT)
        for font in minor.findall("a:font", nsmap):
            if font.get("script") == "Hang":
                font.set("typeface", BODY_FONT)

    tree.write(str(theme_path), xml_declaration=True, encoding="UTF-8", standalone=True)
    print("✓ Theme fonts updated to 부크크")


# ============================================================
# Step 3: 스타일 수정
# ============================================================
def modify_styles():
    """Modify styles.xml for B5 book formatting."""
    styles_path = REF_UNPACKED / "word/styles.xml"
    tree = etree.parse(str(styles_path))
    root = tree.getroot()
    nsmap = {"w": W_NS}

    # 1. Default font size 10pt, Korean language
    doc_defaults = root.find(".//w:docDefaults/w:rPrDefault/w:rPr", nsmap)
    if doc_defaults is not None:
        sz = doc_defaults.find("w:sz", nsmap)
        if sz is not None:
            sz.set(qn(W_NS, "val"), "20")  # 10pt
        szCs = doc_defaults.find("w:szCs", nsmap)
        if szCs is not None:
            szCs.set(qn(W_NS, "val"), "20")
        lang = doc_defaults.find("w:lang", nsmap)
        if lang is not None:
            lang.set(qn(W_NS, "eastAsia"), "ko-KR")

    # 2. Default paragraph spacing
    ppr_default = root.find(".//w:docDefaults/w:pPrDefault/w:pPr", nsmap)
    if ppr_default is not None:
        spacing = ppr_default.find("w:spacing", nsmap)
        if spacing is not None:
            spacing.set(qn(W_NS, "after"), "120")
            spacing.set(qn(W_NS, "line"), "276")  # 1.15x
            spacing.set(qn(W_NS, "lineRule"), "auto")

    # 3~6. Update individual styles
    for style in root.findall("w:style", nsmap):
        style_id = style.get(qn(W_NS, "styleId"))

        if style_id == "BodyText":
            ppr = style.find("w:pPr", nsmap)
            if ppr is not None:
                spacing = ppr.find("w:spacing", nsmap)
                if spacing is not None:
                    spacing.set(qn(W_NS, "before"), "60")
                    spacing.set(qn(W_NS, "after"), "60")

        elif style_id == "Heading1":
            _set_heading_style(style, nsmap, sz="32", page_break=True)

        elif style_id == "Heading2":
            _set_heading_style(style, nsmap, sz="26")

        elif style_id == "Heading3":
            _set_heading_style(style, nsmap, sz="22")

        elif style_id == "Heading4":
            _set_heading_style(style, nsmap, sz="20")

        elif style_id == "Title":
            rpr = style.find("w:rPr", nsmap)
            if rpr is not None:
                sz = rpr.find("w:sz", nsmap)
                if sz is not None:
                    sz.set(qn(W_NS, "val"), "36")
                rfonts = rpr.find("w:rFonts", nsmap)
                if rfonts is not None:
                    rfonts.set(qn(W_NS, "ascii"), HEAD_FONT)
                    rfonts.set(qn(W_NS, "hAnsi"), HEAD_FONT)
                    rfonts.set(qn(W_NS, "eastAsia"), HEAD_FONT)

        elif style_id == "VerbatimChar":
            rpr = style.find("w:rPr", nsmap)
            if rpr is not None:
                rfonts = rpr.find("w:rFonts", nsmap)
                if rfonts is not None:
                    rfonts.set(qn(W_NS, "ascii"), "Consolas")
                    rfonts.set(qn(W_NS, "hAnsi"), "Consolas")
                    rfonts.set(qn(W_NS, "eastAsia"), "Consolas")
                sz = rpr.find("w:sz", nsmap)
                if sz is not None:
                    sz.set(qn(W_NS, "val"), "16")  # 8pt
                else:
                    etree.SubElement(rpr, qn(W_NS, "sz")).set(qn(W_NS, "val"), "16")
                shd = rpr.find("w:shd", nsmap)
                if shd is None:
                    shd = etree.SubElement(rpr, qn(W_NS, "shd"))
                shd.set(qn(W_NS, "val"), "clear")
                shd.set(qn(W_NS, "color"), "auto")
                shd.set(qn(W_NS, "fill"), "F0F0F0")

    # 7. Add SourceCode paragraph style
    _add_source_code_style(root, nsmap)

    # 8. Update Table style
    _update_table_style(root, nsmap)

    # 9. Update BlockText for blockquotes
    _update_blocktext_style(root, nsmap)

    tree.write(str(styles_path), xml_declaration=True, encoding="UTF-8", standalone=True)
    print("✓ Styles updated")


def _set_heading_style(style, nsmap, sz="32", page_break=False):
    """Helper to set heading font and size."""
    rpr = style.find("w:rPr", nsmap)
    if rpr is not None:
        for tag in ["sz", "szCs"]:
            el = rpr.find(f"w:{tag}", nsmap)
            if el is not None:
                el.set(qn(W_NS, "val"), sz)
        rfonts = rpr.find("w:rFonts", nsmap)
        if rfonts is not None:
            rfonts.set(qn(W_NS, "ascii"), HEAD_FONT)
            rfonts.set(qn(W_NS, "hAnsi"), HEAD_FONT)
            rfonts.set(qn(W_NS, "eastAsia"), HEAD_FONT)
    if page_break:
        ppr = style.find("w:pPr", nsmap)
        if ppr is not None:
            pb = ppr.find("w:pageBreakBefore", nsmap)
            if pb is None:
                etree.SubElement(ppr, qn(W_NS, "pageBreakBefore"))


def _add_source_code_style(root, nsmap):
    """Add SourceCode paragraph style for code blocks."""
    for style in root.findall("w:style", nsmap):
        if style.get(qn(W_NS, "styleId")) == "SourceCode":
            return  # Already exists

    sc = etree.SubElement(root, qn(W_NS, "style"))
    sc.set(qn(W_NS, "type"), "paragraph")
    sc.set(qn(W_NS, "customStyle"), "1")
    sc.set(qn(W_NS, "styleId"), "SourceCode")
    etree.SubElement(sc, qn(W_NS, "name")).set(qn(W_NS, "val"), "Source Code")
    etree.SubElement(sc, qn(W_NS, "basedOn")).set(qn(W_NS, "val"), "Normal")
    etree.SubElement(sc, qn(W_NS, "qFormat"))

    ppr = etree.SubElement(sc, qn(W_NS, "pPr"))
    spacing = etree.SubElement(ppr, qn(W_NS, "spacing"))
    spacing.set(qn(W_NS, "before"), "60")
    spacing.set(qn(W_NS, "after"), "60")
    spacing.set(qn(W_NS, "line"), "240")
    spacing.set(qn(W_NS, "lineRule"), "auto")
    etree.SubElement(ppr, qn(W_NS, "ind")).set(qn(W_NS, "left"), "284")
    shd = etree.SubElement(ppr, qn(W_NS, "shd"))
    shd.set(qn(W_NS, "val"), "clear")
    shd.set(qn(W_NS, "color"), "auto")
    shd.set(qn(W_NS, "fill"), "F5F5F5")
    pBdr = etree.SubElement(ppr, qn(W_NS, "pBdr"))
    for side in ["top", "left", "bottom", "right"]:
        bdr = etree.SubElement(pBdr, qn(W_NS, side))
        bdr.set(qn(W_NS, "val"), "single")
        bdr.set(qn(W_NS, "sz"), "4")
        bdr.set(qn(W_NS, "space"), "4")
        bdr.set(qn(W_NS, "color"), "DDDDDD")

    rpr = etree.SubElement(sc, qn(W_NS, "rPr"))
    rfonts = etree.SubElement(rpr, qn(W_NS, "rFonts"))
    for attr in ["ascii", "hAnsi", "eastAsia", "cs"]:
        rfonts.set(qn(W_NS, attr), "Consolas")
    etree.SubElement(rpr, qn(W_NS, "sz")).set(qn(W_NS, "val"), "15")   # 7.5pt
    etree.SubElement(rpr, qn(W_NS, "szCs")).set(qn(W_NS, "val"), "15")
    print("  + Added SourceCode style")


def _update_table_style(root, nsmap):
    """Update Table style with borders."""
    for style in root.findall("w:style", nsmap):
        if style.get(qn(W_NS, "styleId")) == "Table":
            tblPr = style.find("w:tblPr", nsmap)
            if tblPr is None:
                tblPr = etree.SubElement(style, qn(W_NS, "tblPr"))
            tblBorders = tblPr.find("w:tblBorders", nsmap)
            if tblBorders is None:
                tblBorders = etree.SubElement(tblPr, qn(W_NS, "tblBorders"))
            for side in ["top", "left", "bottom", "right", "insideH", "insideV"]:
                bdr = tblBorders.find(f"w:{side}", nsmap)
                if bdr is None:
                    bdr = etree.SubElement(tblBorders, qn(W_NS, side))
                bdr.set(qn(W_NS, "val"), "single")
                bdr.set(qn(W_NS, "sz"), "4")
                bdr.set(qn(W_NS, "space"), "0")
                bdr.set(qn(W_NS, "color"), "999999")
            semi = style.find("w:semiHidden", nsmap)
            if semi is not None:
                style.remove(semi)
            print("  + Updated Table style")
            break


def _update_blocktext_style(root, nsmap):
    """Update BlockText style for blockquotes."""
    for style in root.findall("w:style", nsmap):
        if style.get(qn(W_NS, "styleId")) == "BlockText":
            ppr = style.find("w:pPr", nsmap)
            if ppr is None:
                ppr = etree.SubElement(style, qn(W_NS, "pPr"))
            pBdr = ppr.find("w:pBdr", nsmap)
            if pBdr is None:
                pBdr = etree.SubElement(ppr, qn(W_NS, "pBdr"))
            left_bdr = etree.SubElement(pBdr, qn(W_NS, "left"))
            left_bdr.set(qn(W_NS, "val"), "single")
            left_bdr.set(qn(W_NS, "sz"), "12")
            left_bdr.set(qn(W_NS, "space"), "8")
            left_bdr.set(qn(W_NS, "color"), "CCCCCC")
            shd = ppr.find("w:shd", nsmap)
            if shd is None:
                shd = etree.SubElement(ppr, qn(W_NS, "shd"))
            shd.set(qn(W_NS, "val"), "clear")
            shd.set(qn(W_NS, "color"), "auto")
            shd.set(qn(W_NS, "fill"), "F9F9F9")


# ============================================================
# Step 4: B5 페이지 크기 및 여백 설정
# ============================================================
def modify_document_settings():
    """Set B5 page size and margins in document.xml."""
    doc_path = REF_UNPACKED / "word/document.xml"

    if not doc_path.exists():
        doc_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<w:document xmlns:w="{W_NS}" xmlns:r="{R_NS}">
  <w:body>
    <w:sectPr>
      <w:pgSz w:w="{PAGE_W}" w:h="{PAGE_H}"/>
      <w:pgMar w:top="{MARGIN_TOP}" w:right="{MARGIN_RIGHT}" w:bottom="{MARGIN_BOTTOM}" w:left="{MARGIN_LEFT}" w:header="{MARGIN_HEADER}" w:footer="{MARGIN_FOOTER}" w:gutter="{MARGIN_GUTTER}"/>
      <w:cols w:space="720"/>
    </w:sectPr>
  </w:body>
</w:document>'''
        doc_path.write_text(doc_content, encoding="utf-8")
    else:
        tree = etree.parse(str(doc_path))
        root = tree.getroot()
        nsmap = {"w": W_NS}
        body = root.find("w:body", nsmap)
        if body is not None:
            sectPr = body.find("w:sectPr", nsmap)
            if sectPr is None:
                sectPr = etree.SubElement(body, qn(W_NS, "sectPr"))
            pgSz = sectPr.find("w:pgSz", nsmap)
            if pgSz is None:
                pgSz = etree.SubElement(sectPr, qn(W_NS, "pgSz"))
            pgSz.set(qn(W_NS, "w"), PAGE_W)
            pgSz.set(qn(W_NS, "h"), PAGE_H)
            pgMar = sectPr.find("w:pgMar", nsmap)
            if pgMar is None:
                pgMar = etree.SubElement(sectPr, qn(W_NS, "pgMar"))
            for attr, val in [("top", MARGIN_TOP), ("right", MARGIN_RIGHT), ("bottom", MARGIN_BOTTOM),
                              ("left", MARGIN_LEFT), ("header", MARGIN_HEADER), ("footer", MARGIN_FOOTER),
                              ("gutter", MARGIN_GUTTER)]:
                pgMar.set(qn(W_NS, attr), val)
            cols = sectPr.find("w:cols", nsmap)
            if cols is None:
                cols = etree.SubElement(sectPr, qn(W_NS, "cols"))
            cols.set(qn(W_NS, "space"), "720")
        tree.write(str(doc_path), xml_declaration=True, encoding="UTF-8", standalone=True)
    print(f"✓ Page: B5 ({PAGE_W}x{PAGE_H} DXA)")


# ============================================================
# Step 5: Reference doc 패킹 및 pandoc 실행
# ============================================================
def repack_docx():
    """Pack modified reference directory into DOCX."""
    if OUTPUT_REF.exists():
        OUTPUT_REF.unlink()
    with zipfile.ZipFile(str(OUTPUT_REF), 'w', zipfile.ZIP_DEFLATED) as zf:
        for root_dir, dirs, files in os.walk(str(REF_UNPACKED)):
            for file in files:
                file_path = Path(root_dir) / file
                arcname = file_path.relative_to(REF_UNPACKED)
                zf.write(str(file_path), str(arcname))
    print(f"✓ Reference doc: {OUTPUT_REF.stat().st_size / 1024:.1f} KB")


def run_pandoc():
    """Convert books.md to DOCX using modified reference."""
    cmd = [
        "pandoc", str(BOOKS_MD),
        "-o", str(OUTPUT_DOCX),
        f"--reference-doc={OUTPUT_REF}",
        "--highlight-style=tango",
        "--toc", "--toc-depth=3", "--wrap=none",
        "-f", "markdown+smart+pipe_tables+fenced_code_blocks+backtick_code_blocks+header_attributes",
    ]
    print(f"\n  pandoc: {BOOKS_MD.name} → {OUTPUT_DOCX.name}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"✗ Pandoc error:\n{result.stderr}")
        return False
    if result.stderr:
        print(f"  Warnings: {result.stderr[:300]}")
    print(f"✓ DOCX generated: {OUTPUT_DOCX.stat().st_size / 1024:.0f} KB")
    return True


# ============================================================
# Step 6: 테이블 후처리
# ============================================================
def postprocess_tables():
    """Fix table widths, column grids, and add explicit cell borders."""
    BORDER_COLOR = "999999"
    tmp_dir = Path(tempfile.mkdtemp())

    with zipfile.ZipFile(str(OUTPUT_DOCX), 'r') as zf:
        zf.extractall(str(tmp_dir))

    doc_path = tmp_dir / "word" / "document.xml"
    tree = etree.parse(str(doc_path))
    root = tree.getroot()
    nsmap = {"w": W_NS}

    def make_border(parent, side, color=BORDER_COLOR, sz="4"):
        bdr = etree.SubElement(parent, qn(W_NS, side))
        bdr.set(qn(W_NS, "val"), "single")
        bdr.set(qn(W_NS, "sz"), sz)
        bdr.set(qn(W_NS, "space"), "0")
        bdr.set(qn(W_NS, "color"), color)
        return bdr

    tables = root.findall(".//w:tbl", nsmap)
    fixed = 0

    for tbl in tables:
        tblPr = tbl.find("w:tblPr", nsmap)
        if tblPr is None:
            continue

        # Table width (absolute DXA)
        tblW = tblPr.find("w:tblW", nsmap)
        if tblW is None:
            tblW = etree.SubElement(tblPr, qn(W_NS, "tblW"))
        tblW.set(qn(W_NS, "w"), str(PAGE_CONTENT_WIDTH))
        tblW.set(qn(W_NS, "type"), "dxa")

        # Fixed layout
        tblLayout = tblPr.find("w:tblLayout", nsmap)
        if tblLayout is None:
            tblLayout = etree.SubElement(tblPr, qn(W_NS, "tblLayout"))
        tblLayout.set(qn(W_NS, "type"), "fixed")

        # Table borders
        tblBorders = tblPr.find("w:tblBorders", nsmap)
        if tblBorders is not None:
            tblPr.remove(tblBorders)
        tblBorders = etree.SubElement(tblPr, qn(W_NS, "tblBorders"))
        for side in ["top", "left", "bottom", "right", "insideH", "insideV"]:
            make_border(tblBorders, side)

        # Cell margins
        tblCellMar = tblPr.find("w:tblCellMar", nsmap)
        if tblCellMar is not None:
            tblPr.remove(tblCellMar)
        tblCellMar = etree.SubElement(tblPr, qn(W_NS, "tblCellMar"))
        for sn, val in [("top", "40"), ("left", "80"), ("bottom", "40"), ("right", "80")]:
            m = etree.SubElement(tblCellMar, qn(W_NS, sn))
            m.set(qn(W_NS, "w"), val)
            m.set(qn(W_NS, "type"), "dxa")

        # Remove tblLook
        tblLook = tblPr.find("w:tblLook", nsmap)
        if tblLook is not None:
            tblPr.remove(tblLook)

        # Column grid
        first_tr = tbl.find("w:tr", nsmap)
        if first_tr is None:
            continue
        num_cols = len(first_tr.findall("w:tc", nsmap))
        if num_cols == 0:
            continue
        col_width = PAGE_CONTENT_WIDTH // num_cols

        tblGrid = tbl.find("w:tblGrid", nsmap)
        if tblGrid is not None:
            tbl.remove(tblGrid)
        new_grid = etree.Element(qn(W_NS, "tblGrid"))
        for _ in range(num_cols):
            etree.SubElement(new_grid, qn(W_NS, "gridCol")).set(qn(W_NS, "w"), str(col_width))
        tbl.insert(list(tbl).index(tblPr) + 1, new_grid)

        # Fix each cell
        for row_idx, tr in enumerate(tbl.findall("w:tr", nsmap)):
            trPr = tr.find("w:trPr", nsmap)
            if trPr is not None:
                cnf = trPr.find("w:cnfStyle", nsmap)
                if cnf is not None:
                    trPr.remove(cnf)

            for tc in tr.findall("w:tc", nsmap):
                tcPr = tc.find("w:tcPr", nsmap)
                if tcPr is None:
                    tcPr = etree.SubElement(tc, qn(W_NS, "tcPr"))
                    tc.remove(tcPr)
                    tc.insert(0, tcPr)

                tcW = tcPr.find("w:tcW", nsmap)
                if tcW is None:
                    tcW = etree.SubElement(tcPr, qn(W_NS, "tcW"))
                tcW.set(qn(W_NS, "w"), str(col_width))
                tcW.set(qn(W_NS, "type"), "dxa")

                tcBorders = tcPr.find("w:tcBorders", nsmap)
                if tcBorders is not None:
                    tcPr.remove(tcBorders)
                tcBorders = etree.SubElement(tcPr, qn(W_NS, "tcBorders"))
                for side in ["top", "left", "bottom", "right"]:
                    make_border(tcBorders, side)

                if row_idx == 0:
                    bottom = tcBorders.find("w:bottom", nsmap)
                    if bottom is not None:
                        bottom.set(qn(W_NS, "sz"), "8")
                        bottom.set(qn(W_NS, "color"), "666666")
                    shd = tcPr.find("w:shd", nsmap)
                    if shd is None:
                        shd = etree.SubElement(tcPr, qn(W_NS, "shd"))
                    shd.set(qn(W_NS, "val"), "clear")
                    shd.set(qn(W_NS, "color"), "auto")
                    shd.set(qn(W_NS, "fill"), "E8E8E8")

                vAlign = tcPr.find("w:vAlign", nsmap)
                if vAlign is not None:
                    tcPr.remove(vAlign)

        fixed += 1

    tree.write(str(doc_path), xml_declaration=True, encoding="UTF-8", standalone=True)
    _repack_output(tmp_dir)
    shutil.rmtree(str(tmp_dir))
    print(f"✓ Fixed {fixed} tables")


# ============================================================
# Step 7: 앞부분 추가 (속표지, 판권, 목차)
# ============================================================
def add_front_matter():
    """Add title page, copyright page, and TOC."""

    def p(text, font=BODY_FONT, sz="20", bold=False, center=False,
          spacing_before="0", spacing_after="0"):
        jc = f'<w:jc w:val="center"/>' if center else ''
        b_tag = '<w:b/>' if bold else ''
        sp = f'<w:spacing w:before="{spacing_before}" w:after="{spacing_after}"/>'
        return (f'<w:p><w:pPr>{sp}{jc}<w:rPr><w:rFonts w:ascii="{font}" w:eastAsia="{font}" '
                f'w:hAnsi="{font}"/><w:sz w:val="{sz}"/>{b_tag}</w:rPr></w:pPr>'
                f'<w:r><w:rPr><w:rFonts w:ascii="{font}" w:eastAsia="{font}" w:hAnsi="{font}"/>'
                f'<w:sz w:val="{sz}"/>{b_tag}</w:rPr>'
                f'<w:t xml:space="preserve">{text}</w:t></w:r></w:p>')

    def empty_p(count=1):
        return ''.join([f'<w:p><w:pPr><w:rPr><w:rFonts w:ascii="{BODY_FONT}" '
                        f'w:eastAsia="{BODY_FONT}" w:hAnsi="{BODY_FONT}"/>'
                        f'<w:sz w:val="20"/></w:rPr></w:pPr></w:p>'] * count)

    def page_break():
        return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

    def info_line(label, value):
        return (f'<w:p><w:pPr><w:spacing w:before="24" w:line="276" w:lineRule="auto"/></w:pPr>'
                f'<w:r><w:rPr><w:rFonts w:ascii="{INFO_FONT}" w:eastAsia="{INFO_FONT}" '
                f'w:hAnsi="{INFO_FONT}"/><w:b/><w:sz w:val="18"/></w:rPr>'
                f'<w:t xml:space="preserve">{label}</w:t></w:r>'
                f'<w:r><w:rPr><w:rFonts w:ascii="{INFO_FONT}" w:eastAsia="{INFO_FONT}" '
                f'w:hAnsi="{INFO_FONT}"/><w:sz w:val="18"/></w:rPr>'
                f'<w:t xml:space="preserve">｜{value}</w:t></w:r></w:p>')

    # --- Title Page ---
    parts = [
        empty_p(12),
        p(BOOK_TITLE, font=HEAD_FONT, sz="40", bold=True, center=True, spacing_after="200"),
        p(BOOK_SUBTITLE, font=HEAD_FONT, sz="24", center=True, spacing_after="400"),
        empty_p(4),
        p(AUTHOR, font=BODY_FONT, sz="24", center=True, spacing_after="100"),
        page_break(),
    ]

    # --- Copyright Page ---
    parts.append(empty_p(20))
    parts.append(p(BOOK_TITLE, font=INFO_FONT, sz="20", bold=True))
    parts.append(empty_p(1))
    parts.append(info_line("발 행", PUB_DATE))
    parts.append(info_line("저 자", AUTHOR))
    parts.append(info_line("펴낸이", "한건희"))
    parts.append(info_line("펴낸곳", "주식회사 부크크"))
    parts.append(info_line("출판사등록", "2014.07.15(제2014-16호)"))
    parts.append(info_line("주 소", "서울특별시 금천구 가산디지털1로 119 SK트윈테크타워 A동 305호"))
    parts.append(info_line("전 화", "1670-8316"))
    parts.append(info_line("이메일", "info@bookk.co.kr"))
    parts.append(empty_p(1))
    parts.append(p("ISBN 979-11-XXX-XXXX-X", font=INFO_FONT, sz="16"))
    parts.append(p("이 책의 판권은 저자에게 있습니다. 무단 전재 및 복제를 금합니다.", font=INFO_FONT, sz="16"))
    parts.append(page_break())

    # --- TOC ---
    toc_items = _get_toc_items()
    parts.append(p("목  차", font=HEAD_FONT, sz="28", bold=True, center=True, spacing_after="300"))
    parts.append(empty_p(1))
    for level, title in toc_items:
        if level == 0:
            parts.append(p(title, font=HEAD_FONT, sz="20", bold=True,
                          spacing_before="120", spacing_after="40"))
        else:
            parts.append(
                f'<w:p><w:pPr><w:spacing w:before="20" w:after="20"/><w:ind w:left="480"/></w:pPr>'
                f'<w:r><w:rPr><w:rFonts w:ascii="{BODY_FONT}" w:eastAsia="{BODY_FONT}" '
                f'w:hAnsi="{BODY_FONT}"/><w:sz w:val="18"/></w:rPr>'
                f'<w:t xml:space="preserve">{title}</w:t></w:r></w:p>')
    parts.append(page_break())

    # --- Insert into DOCX ---
    tmp_dir = Path(tempfile.mkdtemp())
    with zipfile.ZipFile(str(OUTPUT_DOCX), 'r') as zf:
        zf.extractall(str(tmp_dir))

    doc_path = tmp_dir / "word" / "document.xml"
    content = doc_path.read_text(encoding='utf-8')
    front_xml = '\n'.join(parts)
    content = content.replace('<w:body>', f'<w:body>\n{front_xml}\n', 1)
    doc_path.write_text(content, encoding='utf-8')

    _repack_output(tmp_dir)
    shutil.rmtree(str(tmp_dir))
    print(f"✓ Added front matter ({len(toc_items)} TOC items)")


def _get_toc_items():
    """Return list of (level, title) for table of contents."""
    return [
        (0, "Chapter 1. 리액티브 프로그래밍 소개"),
        (1, "1.1 리액티브 프로그래밍이란?"), (1, "1.2 명령형 프로그래밍 vs 리액티브 프로그래밍"),
        (1, "1.3 리액티브 스트림(Reactive Streams) 표준"), (1, "1.4 배압(Backpressure)의 개념"),
        (1, "1.5 왜 리액티브가 필요한가?"),
        (0, "Chapter 2. Spring WebFlux 개요"),
        (1, "2.1 Spring MVC와 Spring WebFlux 비교"), (1, "2.2 WebFlux의 내부 구조와 Netty"),
        (1, "2.3 논블로킹 I/O의 원리"), (1, "2.4 WebFlux를 선택해야 하는 경우"),
        (1, "2.5 WebFlux의 두 가지 프로그래밍 모델"),
        (0, "Chapter 3. Project Reactor 핵심"),
        (1, "3.1 Mono와 Flux 이해하기"), (1, "3.2 Reactor의 주요 연산자"),
        (1, "3.3 에러 처리 전략"), (1, "3.4 스케줄러와 스레드 모델"),
        (1, "3.5 Cold vs Hot Publisher"), (1, "3.6 Reactor 디버깅 기법"),
        (0, "Chapter 4. MongoDB 소개"),
        (1, "4.1 NoSQL과 MongoDB의 특징"), (1, "4.2 도큐먼트 모델과 컬렉션"),
        (1, "4.3 MongoDB 설치 및 기본 CRUD"), (1, "4.4 인덱싱과 쿼리 최적화 기초"),
        (1, "4.5 MongoDB와 리액티브 드라이버"),
        (0, "Chapter 5. 개발 환경 구성"),
        (1, "5.1 JDK, IDE, Docker 설치"), (1, "5.2 Spring Initializr로 프로젝트 생성"),
        (1, "5.3 주요 의존성 설정"), (1, "5.4 application.yml 설정"),
        (1, "5.5 MongoDB Docker 컨테이너 구성"), (1, "5.6 프로젝트 구조 설계"),
        (0, "Chapter 6. 어노테이션 기반 REST API 구현"),
        (1, "6.1 도메인 모델 정의"), (1, "6.2 ReactiveMongoRepository 활용"),
        (1, "6.3 서비스 계층 구현"), (1, "6.4 @RestController로 CRUD API"),
        (1, "6.5 요청/응답 DTO 설계"), (1, "6.6 API 테스트"),
        (0, "Chapter 7. 함수형 엔드포인트 (Router Functions)"),
        (1, "7.1 HandlerFunction과 RouterFunction"), (1, "7.2 RouterFunction으로 라우팅 정의"),
        (1, "7.3 HandlerFunction 구현"), (1, "7.4 요청 파라미터 및 바디 처리"),
        (1, "7.5 어노테이션 방식과 함수형 방식 비교"),
        (0, "Chapter 8. MongoDB 리액티브 데이터 접근 심화"),
        (1, "8.1 ReactiveMongoTemplate 활용"), (1, "8.2 커스텀 쿼리와 Criteria API"),
        (1, "8.3 Aggregation Pipeline"), (1, "8.4 변경 스트림(Change Streams)"),
        (1, "8.5 트랜잭션 처리"), (1, "8.6 인덱스 관리와 쿼리 성능 최적화"),
        (0, "Chapter 9. 데이터 검증과 예외 처리"),
        (1, "9.1 Bean Validation"), (1, "9.2 커스텀 Validator"),
        (1, "9.3 글로벌 예외 처리"), (1, "9.4 ErrorWebExceptionHandler"),
        (1, "9.5 에러 응답 표준화"),
        (0, "Chapter 10. WebFlux 필터와 인터셉터"),
        (1, "10.1 WebFilter 구현"), (1, "10.2 HandlerFilterFunction 활용"),
        (1, "10.3 요청/응답 로깅"), (1, "10.4 CORS 설정"),
        (1, "10.5 요청 속도 제한(Rate Limiting)"),
        (0, "Chapter 11. 리액티브 보안 (Spring Security WebFlux)"),
        (1, "11.1 Spring Security Reactive 설정"), (1, "11.2 SecurityWebFilterChain 구성"),
        (1, "11.3 인증과 인가 구현"), (1, "11.4 JWT 기반 인증"),
        (1, "11.5 SecurityContext 관리"), (1, "11.6 OAuth2 / OpenID Connect"),
        (0, "Chapter 12. Server-Sent Events (SSE)"),
        (1, "12.1 SSE란 무엇인가?"), (1, "12.2 Flux를 활용한 SSE 엔드포인트"),
        (1, "12.3 실시간 알림 시스템 구축"), (1, "12.4 MongoDB Change Streams + SSE"),
        (0, "Chapter 13. WebSocket"),
        (1, "13.1 WebSocket 프로토콜 이해"), (1, "13.2 WebSocket 핸들러 구현"),
        (1, "13.3 실시간 채팅 애플리케이션"), (1, "13.4 WebSocket 세션 관리"),
        (0, "Chapter 14. WebClient: 리액티브 HTTP 클라이언트"),
        (1, "14.1 WebClient 설정과 기본 사용법"), (1, "14.2 요청/응답 처리"),
        (1, "14.3 에러 핸들링과 재시도"), (1, "14.4 타임아웃 설정"),
        (1, "14.5 외부 API 연동"), (1, "14.6 WebClient 필터와 인터셉터"),
        (0, "Chapter 15. R2DBC와의 통합"),
        (1, "15.1 R2DBC란?"), (1, "15.2 멀티 데이터소스 구성"),
        (1, "15.3 여러 데이터소스 조합하기"),
        (0, "Chapter 16. 리액티브 테스트 전략"),
        (1, "16.1 StepVerifier 단위 테스트"), (1, "16.2 WebTestClient 통합 테스트"),
        (1, "16.3 Embedded MongoDB 테스트"), (1, "16.4 Testcontainers"),
        (1, "16.5 MockWebServer 외부 API 모킹"), (1, "16.6 테스트 슬라이스"),
        (0, "Chapter 17. 문서화와 API 관리"),
        (1, "17.1 SpringDoc OpenAPI 연동"), (1, "17.2 API 문서 자동 생성"),
        (1, "17.3 API 버전 관리 전략"),
        (0, "Chapter 18. 모니터링과 관측 가능성"),
        (1, "18.1 Spring Boot Actuator"), (1, "18.2 Micrometer와 Prometheus"),
        (1, "18.3 Grafana 대시보드"), (1, "18.4 리액티브 스트림 메트릭"),
        (1, "18.5 분산 추적"), (1, "18.6 구조화된 로깅"),
        (0, "Chapter 19. 성능 최적화"),
        (1, "19.1 성능 측정"), (1, "19.2 MongoDB 커넥션 풀 튜닝"),
        (1, "19.3 Netty 이벤트 루프 최적화"), (1, "19.4 캐싱 전략"),
        (1, "19.5 블로킹 코드 탐지 (BlockHound)"), (1, "19.6 부하 테스트"),
        (0, "Chapter 20. 컨테이너화와 배포"),
        (1, "20.1 Docker 이미지 빌드"), (1, "20.2 Docker Compose 전체 스택"),
        (1, "20.3 Kubernetes 배포"), (1, "20.4 MongoDB Atlas 연동"),
        (1, "20.5 CI/CD 파이프라인"), (1, "20.6 GraalVM Native Image"),
        (0, "Chapter 21. 종합 프로젝트: 리액티브 게시판"),
        (1, "21.1 요구사항 분석 및 설계"), (1, "21.2 사용자 관리"),
        (1, "21.3 게시글 CRUD API"), (1, "21.4 댓글 시스템"),
        (1, "21.5 실시간 알림 (SSE)"), (1, "21.6 페이징과 검색"),
        (1, "21.7 파일 업로드 (GridFS)"), (1, "21.8 전체 테스트"),
        (1, "21.9 Docker Compose로 배포"),
        (0, "부록 A. Reactor 주요 연산자 레퍼런스"),
        (0, "부록 B. MongoDB 쿼리 연산자 정리"),
        (0, "부록 C. 자주 발생하는 문제와 해결 방법 (FAQ)"),
        (0, "부록 D. 참고 자료 및 추천 학습 경로"),
    ]


# ============================================================
# 유틸리티
# ============================================================
def _repack_output(tmp_dir):
    """Repack tmp_dir into OUTPUT_DOCX."""
    if OUTPUT_DOCX.exists():
        OUTPUT_DOCX.unlink()
    with zipfile.ZipFile(str(OUTPUT_DOCX), 'w', zipfile.ZIP_DEFLATED) as zf:
        for root_dir, dirs, files in os.walk(str(tmp_dir)):
            for file in files:
                file_path = Path(root_dir) / file
                arcname = file_path.relative_to(tmp_dir)
                zf.write(str(file_path), str(arcname))


def cleanup():
    """Remove temporary build directory."""
    if WORK_DIR.exists():
        shutil.rmtree(str(WORK_DIR))


# ============================================================
# 메인 실행
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print(f"  {BOOK_TITLE}")
    print(f"  B5 부크크 DOCX 빌드")
    print("=" * 60)

    try:
        print("\n[1/7] Extracting pandoc reference...")
        extract_pandoc_reference()

        print("\n[2/7] Modifying theme fonts...")
        modify_theme()

        print("\n[3/7] Modifying styles...")
        modify_styles()

        print("\n[4/7] Setting page size...")
        modify_document_settings()

        print("\n[5/7] Running pandoc...")
        repack_docx()
        success = run_pandoc()

        if success:
            print("\n[6/7] Post-processing tables...")
            postprocess_tables()

            print("\n[7/7] Adding front matter...")
            add_front_matter()

            print("\n" + "=" * 60)
            size = OUTPUT_DOCX.stat().st_size / 1024
            print(f"  ✓ 빌드 완료: {OUTPUT_DOCX.name} ({size:.0f} KB)")
            print("=" * 60)
        else:
            print("\n✗ 빌드 실패!")
    finally:
        cleanup()

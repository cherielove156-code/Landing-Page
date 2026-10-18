"""Restyle the Beauty Business Blueprint webinar deck to the Rie Artistry brand.

Only colors, fonts, and backgrounds change. Slides, order, images, click-builds
(duplicated slides with hidden lines), and speaker notes are untouched.

usage: python3 restyle.py <unpacked_dir> <slides.json>
"""
import json
import re
import sys
from pathlib import Path

from lxml import etree

A = "http://schemas.openxmlformats.org/drawingml/2006/main"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS = {"a": A, "p": P}

# Brand palette
CREAM, IVORY, ESPRESSO, SOFT = "FBF7F1", "FFFDFA", "2A201B", "5A4A42"
ROSE, ROSE_TEXT, BLUSH, SAND = "AD5A6E", "94415A", "FBE6EB", "E4D6C7"
DARK_INK, DARK_BLUSH = "F7EEE5", "F5C6D2"

SERIF, SANS = "Cormorant Garamond", "Jost"
SERIF_SCALE = 1.15  # Cormorant reads smaller than Montserrat at the same point size

DARK_TYPES_FIRST = {"TITLE"}           # first TITLE slide (opening) and program reveal
DARK_SLIDES_BY_TYPE = {"COMPONENT", "Q&A"}

FILL_MAP_LIGHT = {"FFD60A": ROSE, "F2F2F2": BLUSH, "FFFFFF": IVORY, "9E2B4F": ROSE,
                  "141414": ESPRESSO, "DDDDDD": "F4EBE1", "F7E9EE": BLUSH}
LINE_MAP = {"FFD60A": ROSE, "D0D0D0": "D9C4B4", "9E2B4F": ROSE, "FFFFFF": IVORY,
            "141414": ROSE, "F2F2F2": "F2C9D3", "DDDDDD": SAND}
DARK_FILLS = {"9E2B4F", "141414"}       # original fills that carry real white text


def q(tag):
    pre, name = tag.split(":")
    return "{%s}%s" % (NS[pre], name)


def solid_color(el):
    """srgbClr val of a direct <a:solidFill> child of el, or None."""
    if el is None:
        return None
    sf = el.find("a:solidFill", NS)
    if sf is None:
        return None
    c = sf.find("a:srgbClr", NS)
    return c.get("val").upper() if c is not None else None


def set_solid(el, val):
    sf = el.find("a:solidFill", NS)
    c = sf.find("a:srgbClr", NS)
    c.set("val", val)


def bbox(sp):
    off = sp.find(".//a:xfrm/a:off", NS)
    ext = sp.find(".//a:xfrm/a:ext", NS)
    if off is None or ext is None:
        return None
    x, y = int(off.get("x")), int(off.get("y"))
    return x, y, x + int(ext.get("cx")), y + int(ext.get("cy"))


def para_is_heading(p):
    runs = [r for r in p.findall("a:r", NS) if (r.findtext("a:t", default="", namespaces=NS)).strip()]
    if not runs:
        return False
    text = "".join(r.findtext("a:t", default="", namespaces=NS) for r in runs)
    if re.search(r"\d", text):
        return False  # numbers stay in the sans for easy reading
    for r in runs:
        rpr = r.find("a:rPr", NS)
        if rpr is None or rpr.get("b") != "1" or int(rpr.get("sz", "0")) < 3200:
            return False
    return True


def set_font(rpr, face):
    for tag in ("a:latin", "a:ea", "a:cs"):
        el = rpr.find(tag, NS)
        if el is not None:
            el.set("typeface", face)
            for attr in ("pitchFamily", "charset"):
                if attr in el.attrib:
                    del el.attrib[attr]


def map_text_color(orig, *, dark, on_bar, own_dark_fill, bg_behind, size):
    if orig == "FFFFFF":
        return "FFFFFF" if own_dark_fill else bg_behind  # hidden click-build lines stay hidden
    if on_bar:
        return "FFFFFF" if orig in ("141414", "9E2B4F") else orig
    if orig == "141414":
        return DARK_INK if dark else ESPRESSO
    if orig == "9E2B4F":
        if dark:
            return DARK_BLUSH
        return ROSE if size >= 2400 else ROSE_TEXT
    if orig == "8A8A8A":
        return "D9CBBE" if dark else SOFT
    if orig == "BBBBBB":
        return "6B5A50" if dark else "C9B6A6"
    if orig == "BDBDBD":
        return "8F7B6E"
    return orig


def restyle_slide(path, dark):
    tree = etree.parse(str(path))
    root = tree.getroot()
    slide_bg = ESPRESSO if dark else CREAM

    bg = root.find(".//p:bg/p:bgPr", NS)
    if bg is not None and solid_color(bg):
        set_solid(bg, slide_bg)

    sptree = root.find(".//p:spTree", NS)
    bars = []
    for sp in sptree.findall("p:sp", NS):
        sppr = sp.find("p:spPr", NS)
        if solid_color(sppr) == "FFD60A":
            if bbox(sp): bars.append(bbox(sp))

    def on_a_bar(sp):
        b = bbox(sp)
        if not b or not bars:
            return False
        cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
        return any(x0 <= cx <= x1 and y0 <= cy <= y1 for x0, y0, x1, y1 in bars)

    for sp in root.iter(q("p:sp"), q("p:cxnSp"), q("p:pic")):
        sppr = sp.find("p:spPr", NS)
        own = solid_color(sppr)
        own_new = None
        if own:
            own_new = FILL_MAP_LIGHT.get(own, own)
            if own == "FFFFFF":
                own_new = slide_bg  # white-on-white shapes are click-builds waiting to appear: keep them invisible
            set_solid(sppr, own_new)
        if sppr is not None:
            ln = sppr.find("a:ln", NS)
            lc = solid_color(ln)
            if lc:
                set_solid(ln, slide_bg if lc == "FFFFFF" else LINE_MAP.get(lc, lc))

        if sp.tag != q("p:sp"):
            continue
        bar = on_a_bar(sp) and own != "FFD60A"
        behind = own_new if own_new else (ROSE if bar else slide_bg)
        own_dark = own in DARK_FILLS

        for p in sp.iter(q("a:p")):
            heading = para_is_heading(p)
            for rpr in list(p.iter(q("a:rPr"))) + list(p.iter(q("a:endParaRPr"))):
                size = int(rpr.get("sz", "1800"))
                if heading and rpr.get("sz"):
                    rpr.set("sz", str(int(round(size * SERIF_SCALE / 100.0)) * 100))
                c = solid_color(rpr)
                if c:
                    set_solid(rpr, map_text_color(c, dark=dark, on_bar=bar, own_dark_fill=own_dark,
                                                  bg_behind=behind, size=size))
                set_font(rpr, SERIF if heading else SANS)

    tree.write(str(path), xml_declaration=True, encoding="UTF-8", standalone=True)


def restyle_theme(unpacked):
    th = unpacked / "ppt/theme/theme1.xml"
    x = th.read_text(encoding="utf-8")
    x = re.sub(r'(<a:majorFont><a:latin typeface=")[^"]*(")', r"\g<1>%s\g<2>" % SERIF, x)
    x = re.sub(r'(<a:minorFont><a:latin typeface=")[^"]*(")', r"\g<1>%s\g<2>" % SANS, x)
    th.write_text(x, encoding="utf-8")
    for f in list((unpacked / "ppt/slideMasters").glob("*.xml")) + list((unpacked / "ppt/slideLayouts").glob("*.xml")):
        x = f.read_text(encoding="utf-8")
        x = x.replace('typeface="Montserrat"', 'typeface="%s"' % SANS)
        f.write_text(x, encoding="utf-8")


def reword_yellow_bar(unpacked):
    """The CTA bar is rose now, so slides and notes can't call it yellow."""
    for f in list((unpacked / "ppt/slides").glob("slide*.xml")) + list((unpacked / "ppt/notesSlides").glob("*.xml")):
        x = f.read_text(encoding="utf-8")
        y = x.replace("Or use the link in the yellow bar.", "Or use the link at the bottom of the screen.")
        y = y.replace("Yellow bar at bottom:", "Rose bar at bottom:")
        if y != x:
            f.write_text(y, encoding="utf-8")


def main():
    unpacked = Path(sys.argv[1])
    info = json.load(open(sys.argv[2]))
    first_title = min(r["n"] for r in info if r["type"] == "TITLE")
    reveal = [r["n"] for r in info if r["type"] == "TITLE" and "Beauty Business Blueprint" in r["text"]
              and "Guarantee" not in r["text"]]
    dark_ns = {first_title, *reveal} | {r["n"] for r in info if r["type"] in DARK_SLIDES_BY_TYPE}
    for r in info:
        restyle_slide(unpacked / "ppt/slides" / r["file"], r["n"] in dark_ns)
    restyle_theme(unpacked)
    reword_yellow_bar(unpacked)
    print("dark slides:", sorted(dark_ns))


if __name__ == "__main__":
    main()

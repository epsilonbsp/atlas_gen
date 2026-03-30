import json
import subprocess
import xml.etree.ElementTree as ET

from .config import *
from .image import *

def atlas_generate_fonts():
    for font_path in INPUT_FONTS_DIR_PATH.glob("*.ttf"):
        name = font_path.stem
        out_dir = TEMP_FONTS_DIR_PATH / name
        out_dir.mkdir(parents = True, exist_ok = True)

        subprocess.run([
            str(MSDF_ATLAS_GEN_EXE_PATH),
            "-font", str(font_path),
            "-type", "mtsdf",
            "-pxrange", str(ATLAS_PXRANGE),
            "-format", "rgba",
            "-imageout", str(out_dir / "font.rgba"),
            "-json", str(out_dir / "font.json"),
        ], check = True)

        print(f"Generated: {out_dir}/")

def atlas_generate_icons():
    TEMP_ICONS_DIR_PATH.mkdir(parents = True, exist_ok = True)

    for svg_path in INPUT_ICONS_DIR_PATH.glob("*.svg"):
        name = svg_path.stem
        root = ET.parse(svg_path).getroot()
        w = int(float(root.get("width")))
        h = int(float(root.get("height")))

        subprocess.run([
            str(MSDF_GEN_EXE_PATH),
            "mtsdf",
            "-svg", str(svg_path),
            "-autoframe",
            "-o", str(TEMP_ICONS_DIR_PATH / f"{name}.rgba"),
            "-size", str(w), str(h),
            "-pxrange", str(ATLAS_PXRANGE),
            "-format", "rgba",
        ], check = True)

        print(f"Generated: {TEMP_ICONS_DIR_PATH / name}.rgba")

def atlas_shelf_pack(items, size, start_y = ATLAS_PADDING):
    shelf_x = ATLAS_PADDING
    shelf_y = start_y
    shelf_h = 0

    for item in items:
        if shelf_x + item["w"] > size - ATLAS_PADDING:
            shelf_y = shelf_y + shelf_h + ATLAS_PADDING
            shelf_x = ATLAS_PADDING
            shelf_h = 0

        item["x"] = shelf_x
        item["y"] = shelf_y
        shelf_x = shelf_x + item["w"] + ATLAS_PADDING
        shelf_h = max(shelf_h, item["h"])

    return items

def atlas_build():
    OUTPUT_DIR_PATH.mkdir(parents = True, exist_ok = True)
    (OUTPUT_DIR_PATH / "fonts").mkdir(parents = True, exist_ok = True)
    (OUTPUT_DIR_PATH / "icons").mkdir(parents = True, exist_ok = True)

    items = []

    for font_path in INPUT_FONTS_DIR_PATH.glob("*.ttf"):
        name = font_path.stem

        with open(TEMP_FONTS_DIR_PATH / name / "font.json") as f:
            font_json = json.load(f)

        w = font_json["atlas"]["width"]
        h = font_json["atlas"]["height"]
        items.append({"type": "font", "name": name, "w": w, "h": h, "font_json": font_json})

    for svg_path in INPUT_ICONS_DIR_PATH.glob("*.svg"):
        name = svg_path.stem
        root = ET.parse(svg_path).getroot()
        w = int(float(root.get("width")))
        h = int(float(root.get("height")))
        items.append({"type": "icon", "name": name, "w": w, "h": h})

    items = sorted(items, key = lambda x: x["h"], reverse = True)

    start_y = ATLAS_PADDING + 2 + ATLAS_PADDING
    min_w = max(item["w"] for item in items) + 2 * ATLAS_PADDING
    max_w = sum(item["w"] for item in items) + (len(items) + 1) * ATLAS_PADDING

    best_w, best_h, best_area = None, None, float("inf")

    for w in range(min_w, max_w + 1):
        for item in items:
            item.pop("x", None)
            item.pop("y", None)

        atlas_shelf_pack(items, w, start_y = start_y)

        h = max(item["y"] + item["h"] for item in items) + ATLAS_PADDING

        if w > ATLAS_MAX_SIZE or h > ATLAS_MAX_SIZE:
            break

        area = w * h * (max(w, h) / min(w, h))

        if area < best_area:
            best_w, best_h, best_area = w, h, area

    if best_w is None:
        raise RuntimeError(f"Items exceed maximum atlas size ({ATLAS_MAX_SIZE})")

    for item in items:
        item.pop("x", None)
        item.pop("y", None)

    atlas_shelf_pack(items, best_w, start_y = start_y)

    atlas_w, atlas_h = best_w, best_h
    print(f"Atlas size: {atlas_w}x{atlas_h}")
    atlas = bytearray(atlas_w * atlas_h * 4)

    for item in items:
        dx = item["x"]
        dy = item["y"]
        w = item["w"]
        h = item["h"]

        if item["type"] == "font":
            name = item["name"]
            rgba = (TEMP_FONTS_DIR_PATH / name / "font.rgba").read_bytes()[12:]
            image_blit(atlas, atlas_w, rgba, w, h, dx, dy)

            font_json = item["font_json"]
            y_shift = atlas_h - h - dy

            for glyph in font_json["glyphs"]:
                if "atlasBounds" in glyph:
                    glyph["atlasBounds"]["left"] += dx
                    glyph["atlasBounds"]["right"] += dx
                    glyph["atlasBounds"]["bottom"] += y_shift
                    glyph["atlasBounds"]["top"] += y_shift

            font_json["atlas"]["width"] = atlas_w
            font_json["atlas"]["height"] = atlas_h

            with open(OUTPUT_DIR_PATH / "fonts" / f"{name}.json", "w") as f:
                json.dump(font_json, f, separators = (',', ':'))

            print(f"JSON: {OUTPUT_DIR_PATH / 'fonts' / name}.json")

    icons_json = {}

    for item in items:
        if item["type"] == "icon":
            name = item["name"]
            rgba = (TEMP_ICONS_DIR_PATH / f"{name}.rgba").read_bytes()[12:]
            image_blit(atlas, atlas_w, rgba, item["w"], item["h"], item["x"], item["y"])
            icons_json[name] = {"x": item["x"], "y": item["y"], "w": item["w"], "h": item["h"]}

    if icons_json:
        with open(OUTPUT_DIR_PATH / "icons" / "icons.json", "w") as f:
            json.dump(icons_json, f, separators = (',', ':'))

        print(f"JSON: {OUTPUT_DIR_PATH / 'icons' / 'icons.json'}")

    image_write_png(OUTPUT_DIR_PATH / "atlas.png", atlas_w, atlas_h, atlas)
    print(f"Atlas: {OUTPUT_DIR_PATH / 'atlas.png'}")

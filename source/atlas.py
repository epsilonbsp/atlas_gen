import json
import subprocess

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

def atlas_shelf_pack(items, start_y = ATLAS_PADDING):
    shelf_x = ATLAS_PADDING
    shelf_y = start_y
    shelf_h = 0

    for item in items:
        if shelf_x + item["w"] > ATLAS_SIZE - ATLAS_PADDING:
            shelf_y = shelf_y + shelf_h + ATLAS_PADDING
            shelf_x = ATLAS_PADDING
            shelf_h = 0

        if shelf_y + item["h"] > ATLAS_SIZE - ATLAS_PADDING:
            raise RuntimeError(f"Atlas full, cannot fit {item['w']}x{item['h']}")

        item["x"] = shelf_x
        item["y"] = shelf_y
        shelf_x = shelf_x + item["w"] + ATLAS_PADDING
        shelf_h = max(shelf_h, item["h"])

    return items

def atlas_build():
    OUTPUT_DIR_PATH.mkdir(parents = True, exist_ok = True)
    (OUTPUT_DIR_PATH / "fonts").mkdir(parents = True, exist_ok = True)

    items = []

    for font_path in INPUT_FONTS_DIR_PATH.glob("*.ttf"):
        name = font_path.stem

        with open(TEMP_FONTS_DIR_PATH / name / "font.json") as f:
            font_json = json.load(f)

        w = font_json["atlas"]["width"]
        h = font_json["atlas"]["height"]
        items.append({"type": "font", "name": name, "w": w, "h": h, "font_json": font_json})

    items = sorted(items, key = lambda x: x["h"], reverse = True)
    atlas_shelf_pack(items, start_y = ATLAS_PADDING + 2 + ATLAS_PADDING)

    atlas = bytearray(ATLAS_SIZE * ATLAS_SIZE * 4)

    for item in items:
        dx = item["x"]
        dy = item["y"]
        w = item["w"]
        h = item["h"]

        if item["type"] == "font":
            name = item["name"]
            rgba = (TEMP_FONTS_DIR_PATH / name / "font.rgba").read_bytes()
            image_blit(atlas, ATLAS_SIZE, rgba, w, h, dx, dy)

            font_json = item["font_json"]
            y_shift = ATLAS_SIZE - h - dy

            for glyph in font_json["glyphs"]:
                if "atlasBounds" in glyph:
                    glyph["atlasBounds"]["left"] += dx
                    glyph["atlasBounds"]["right"] += dx
                    glyph["atlasBounds"]["bottom"] += y_shift
                    glyph["atlasBounds"]["top"] += y_shift

            font_json["atlas"]["width"] = ATLAS_SIZE
            font_json["atlas"]["height"] = ATLAS_SIZE

            with open(OUTPUT_DIR_PATH / "fonts" / f"{name}.json", "w") as f:
                json.dump(font_json, f, separators = (',', ':'))

            print(f"JSON: {OUTPUT_DIR_PATH / 'fonts' / name}.json")

    image_write_png(OUTPUT_DIR_PATH / "atlas.png", ATLAS_SIZE, ATLAS_SIZE, atlas)
    print(f"Atlas: {OUTPUT_DIR_PATH / 'atlas.png'}")

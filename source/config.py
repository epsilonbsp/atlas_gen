from pathlib import Path
import shutil

from .download import *
from .unpack import *

# General
BUILD_DIR_PATH = Path("build")
DOWNLOADS_DIR_PATH = BUILD_DIR_PATH / "downloads"
BIN_DIR_PATH = BUILD_DIR_PATH / "bin"
TEMP_DIR_PATH = BUILD_DIR_PATH / "temp"
TEMP_FONTS_DIR_PATH = TEMP_DIR_PATH / "fonts"

INPUT_DIR_PATH = Path("input")
INPUT_FONTS_DIR_PATH = INPUT_DIR_PATH / "fonts"
OUTPUT_DIR_PATH = Path("output")

# MSDF Atlas Gen
MSDF_ATLAS_GEN_NAME = "MSDF Atlas Generator"
MSDF_ATLAS_DOWNLOAD_URL = "https://github.com/Chlumsky/msdf-atlas-gen/releases/download/v1.4/msdf-atlas-gen-1.4-win64.zip"
MSDF_ATLAS_GEN_DOWNLOAD_PATH = DOWNLOADS_DIR_PATH / "msdf-atlas-gen.zip"
MSDF_ATLAS_GEN_INSTALL_PATH = BIN_DIR_PATH
MSDF_ATLAS_GEN_EXE_PATH = MSDF_ATLAS_GEN_INSTALL_PATH / "msdf-atlas-gen.exe"

# Sample font
SAMPLE_FONT_NAME = "Space Mono"
SAMPLE_FONT_DOWNLOAD_URL = "https://github.com/googlefonts/spacemono/archive/refs/tags/f5ebc1e1c0.zip"
SAMPLE_FONT_DOWNLOAD_PATH = DOWNLOADS_DIR_PATH / "spacemono.zip"
SAMPLE_FONT_INSTALL_PATH = BUILD_DIR_PATH / "spacemono"
SAMPLE_FONT_FILES = {
    SAMPLE_FONT_INSTALL_PATH / "fonts" / "SpaceMono-Bold.ttf": INPUT_FONTS_DIR_PATH / "bold.ttf",
    SAMPLE_FONT_INSTALL_PATH / "fonts" / "SpaceMono-BoldItalic.ttf": INPUT_FONTS_DIR_PATH / "bold_italic.ttf",
    SAMPLE_FONT_INSTALL_PATH / "fonts" / "SpaceMono-Italic.ttf": INPUT_FONTS_DIR_PATH / "italic.ttf",
    SAMPLE_FONT_INSTALL_PATH / "fonts" / "SpaceMono-Regular.ttf": INPUT_FONTS_DIR_PATH / "regular.ttf"
}

# Atlas
ATLAS_MAX_SIZE = 8192
ATLAS_PADDING = 2
ATLAS_PXRANGE = 8

# Downloads
def download_msdf_atlas_gen():
    download_file_and_log(
        MSDF_ATLAS_GEN_NAME,
        MSDF_ATLAS_DOWNLOAD_URL,
        MSDF_ATLAS_GEN_DOWNLOAD_PATH
    )

    unpack_file_and_log(
        MSDF_ATLAS_GEN_NAME,
        MSDF_ATLAS_GEN_DOWNLOAD_PATH,
        MSDF_ATLAS_GEN_INSTALL_PATH,
        True
    )

def download_sample_font():
    download_file_and_log(
        SAMPLE_FONT_NAME,
        SAMPLE_FONT_DOWNLOAD_URL,
        SAMPLE_FONT_DOWNLOAD_PATH
    )

    unpack_file_and_log(
        SAMPLE_FONT_NAME,
        SAMPLE_FONT_DOWNLOAD_PATH,
        SAMPLE_FONT_INSTALL_PATH,
        True
    )

    INPUT_FONTS_DIR_PATH.mkdir(parents = True, exist_ok = True)

    for src, dst in SAMPLE_FONT_FILES.items():
        shutil.copy(src, dst)

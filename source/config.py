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
TEMP_ICONS_DIR_PATH = TEMP_DIR_PATH / "icons"

INPUT_DIR_PATH = Path("input")
INPUT_FONTS_DIR_PATH = INPUT_DIR_PATH / "fonts"
INPUT_ICONS_DIR_PATH = INPUT_DIR_PATH / "icons"
OUTPUT_DIR_PATH = Path("output")

# MSDF Gen
MSDF_GEN_NAME = "MSDF Generator"
MSDF_GEN_DOWNLOAD_URL = "https://github.com/Chlumsky/msdfgen/releases/download/v1.13/msdfgen-1.13-win64.zip"
MSDF_GEN_DOWNLOAD_PATH = DOWNLOADS_DIR_PATH / "msdfgen.zip"
MSDF_GEN_INSTALL_PATH = BIN_DIR_PATH
MSDF_GEN_EXE_NAME = "msdfgen.exe"
MSDF_GEN_EXE_PATH = MSDF_GEN_INSTALL_PATH / MSDF_GEN_EXE_NAME

# MSDF Atlas Gen
MSDF_ATLAS_GEN_NAME = "MSDF Atlas Generator"
MSDF_ATLAS_GEN_DOWNLOAD_URL = "https://github.com/Chlumsky/msdf-atlas-gen/releases/download/v1.4/msdf-atlas-gen-1.4-win64.zip"
MSDF_ATLAS_GEN_DOWNLOAD_PATH = DOWNLOADS_DIR_PATH / "msdf-atlas-gen.zip"
MSDF_ATLAS_GEN_INSTALL_PATH = BIN_DIR_PATH
MSDF_ATLAS_GEN_EXE_NAME = "msdf-atlas-gen.exe"
MSDF_ATLAS_GEN_EXE_PATH = MSDF_ATLAS_GEN_INSTALL_PATH / MSDF_ATLAS_GEN_EXE_NAME

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
def download_msdf_gen():
    if not MSDF_GEN_DOWNLOAD_PATH.exists():
        download_file_and_log(
            MSDF_GEN_NAME,
            MSDF_GEN_DOWNLOAD_URL,
            MSDF_GEN_DOWNLOAD_PATH
        )

    if not MSDF_GEN_EXE_PATH.exists():
        unpack_file_and_log(
            MSDF_GEN_NAME,
            MSDF_GEN_DOWNLOAD_PATH,
            MSDF_GEN_INSTALL_PATH,
            True
        )

        os.remove(BIN_DIR_PATH / "example.bat")

def download_msdf_atlas_gen():
    if not MSDF_ATLAS_GEN_DOWNLOAD_PATH.exists():
        download_file_and_log(
            MSDF_ATLAS_GEN_NAME,
            MSDF_ATLAS_GEN_DOWNLOAD_URL,
            MSDF_ATLAS_GEN_DOWNLOAD_PATH
        )

    if not MSDF_ATLAS_GEN_EXE_PATH.exists():
        unpack_file_and_log(
            MSDF_ATLAS_GEN_NAME,
            MSDF_ATLAS_GEN_DOWNLOAD_PATH,
            MSDF_ATLAS_GEN_INSTALL_PATH,
            True
        )

def download_sample_font():
    if not DOWNLOADS_DIR_PATH.exists():
        download_file_and_log(
            SAMPLE_FONT_NAME,
            SAMPLE_FONT_DOWNLOAD_URL,
            SAMPLE_FONT_DOWNLOAD_PATH
        )

    if not SAMPLE_FONT_INSTALL_PATH.exists():
        unpack_file_and_log(
            SAMPLE_FONT_NAME,
            SAMPLE_FONT_DOWNLOAD_PATH,
            SAMPLE_FONT_INSTALL_PATH,
            True
        )

    INPUT_FONTS_DIR_PATH.mkdir(parents = True, exist_ok = True)

    for src, dst in SAMPLE_FONT_FILES.items():
        shutil.copy(src, dst)

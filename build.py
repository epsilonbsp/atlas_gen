import os
import sys

sys.pycache_prefix = os.path.join("build", "pycache")

from source.atlas import *
from source.config import *
from source.download import *
from source.unpack import *

argc = len(sys.argv)

if argc < 2:
    print("No arguments specified")
    sys.exit(1)
elif argc > 3:
    print("Too many arguments")
    sys.exit(1)

command = sys.argv[1]
arg0 = sys.argv[2] if argc > 2 else ""

if command == "install":
    download_msdf_atlas_gen()
    download_sample_font()
elif command == "generate":
    atlas_generate_fonts()
    atlas_build()

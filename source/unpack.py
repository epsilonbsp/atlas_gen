from enum import auto, IntEnum
import os
from pathlib import Path
import shutil
import sys
import tarfile
import zipfile

class Unpack_Status(IntEnum):
    SUCCESS = auto()
    FAILURE = auto()

def unpack_file(archive_path: str|Path, unpack_path: str|Path, strip_top_level: bool = False) -> tuple[Unpack_Status, Exception | None]:
    try:
        top_level_name = None

        if zipfile.is_zipfile(archive_path):
            with zipfile.ZipFile(archive_path, "r") as archive:
                if strip_top_level:
                    top_level_name = Path(archive.namelist()[0]).parts[0]

                archive.extractall(unpack_path)
        elif tarfile.is_tarfile(archive_path):
            with tarfile.open(archive_path, "r:*") as archive:
                if strip_top_level:
                    top_level_name = Path(archive.getnames()[0]).parts[0]

                archive.extractall(unpack_path)
        else:
            raise Exception("Unsupported archive type")

        if strip_top_level and top_level_name:
            top_folder = os.path.join(unpack_path, top_level_name)

            if os.path.isdir(top_folder):
                for item in os.listdir(top_folder):
                    shutil.move(
                        os.path.join(top_folder, item),
                        unpack_path
                    )

                os.rmdir(top_folder)

        return Unpack_Status.SUCCESS, None
    except Exception as e:
        return Unpack_Status.FAILURE, e

def unpack_file_and_log(name: str, archive_path: str|Path, unpack_path: str|Path, strip_top_level: bool = False) -> None:
    print(f"Unpacking {name}...")
    print(f"From: {os.path.abspath(archive_path)}")
    print(f"To: {os.path.abspath(unpack_path)}")

    status, e = unpack_file(archive_path, unpack_path, strip_top_level)

    if status == Unpack_Status.SUCCESS:
        print("Unpacking success!")
    else:
        print(f"Unpacking failure: {e}")
        sys.exit(1)

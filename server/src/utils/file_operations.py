from fastapi import status

from datetime import datetime
import typing
import os
import pathlib

from utils.exceptions import TagAmountError, TagContentError, NotSuchFileError
from settings import OS

STEP = 1024 if OS == "windows" else 1000

TB = STEP ** 4
GB = TB / 1000
MB = GB / 1000
KB = MB / 1000


def check_file(path: str):
    try:
        path = os.path.abspath(pathlib.Path(path))
    
        if os.path.isdir(path):
            return path, "dir"
        elif os.path.isfile(path):
            return path, "file"
    except:
        pass
    
    raise NotSuchFileError(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"cannot find file: {path}"
    )


def get_information_about_file(
    path: pathlib.Path | str,
    format: str = "%d.%m.%y %H:%M:%S"
) -> dict[str, typing.Any]:
    try:
        stat = os.stat(path)
    except FileNotFoundError:
        raise NotSuchFileError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"cannot find file: {path}"
        )

    size = stat.st_size

    if size > TB:
        size = f"{size / TB:.2f} TB"
    elif size > GB:
        size = f"{size / GB:.2f} GB"
    elif size > MB:
        size = f"{size / MB:.2f} MB"
    elif size > KB:
        size = f"{size / KB:.2f} KB"
    else:
        size = f"{size} B"

    _, file_type = check_file(path)
    result = {
        "path": path,
        "size": size,
        "created": datetime.fromtimestamp(stat.st_ctime).strftime(format),
        "updated": datetime.fromtimestamp(stat.st_mtime).strftime(format),
        "worked": datetime.fromtimestamp(stat.st_atime).strftime(format),
        "file_type": file_type
    }

    if file_type == "dir":
        files = os.listdir(path)
        result |= {"files": files}

    return result


def check_tags(tags: list[str]) -> list[str]:
    l = len(tags)
    if l < 3 or l > 100:
        raise TagAmountError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=">2 and <100"
        )

    for tag in tags:
        l = len(tag)
        if l < 1 or l > 50:
            raise TagContentError(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="no more than 50 words"
            )

    return tags
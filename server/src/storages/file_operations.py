from fastapi import status

import typing

from storages import Storage
from storages.local import LocalStorage
from storages.drive import DriveStorage
from storages.remote import RemoteStorage
from utils.exceptions import TagAmountError, TagContentError
from settings import OS

STEP = 1024 if OS == "windows" else 1000

TB = STEP ** 4
GB = TB / STEP
MB = GB / STEP
KB = MB / STEP


# def check_file(path: str):
#     try:
#         path = os.path.abspath(pathlib.Path(path))
    
#         if os.path.isdir(path):
#             return path, "dir"
#         elif os.path.isfile(path):
#             return path, "file"
#     except:    
#         raise NotSuchFileError(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"cannot find file: {path}"
#         )


def form_size(size: int):
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

    return size


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


def get_storage(storage_type, *args, **kwargs) -> Storage:
    return {
        "local": LocalStorage,
        "drive": DriveStorage,
        "remote": RemoteStorage
    }[storage_type](*args, **kwargs)
    


def save_file(
    storage: Storage, 
    path: str, 
    data: bytes, 
    file_type: typing.Literal["dir", "file"] = "file",
    *args,
    **kwargs
) -> str | None:
    return storage.save_file(
        path=path, data=data, file_type=file_type, *args, **kwargs
    )


def remove_file(storage: Storage, *args, **kwargs):
    storage.remove_file(*args, **kwargs)


def load_file(storage: Storage, *args, **kwargs) -> bytes:
    return storage.load_file(*args, **kwargs)


def get_file_information(
    storage: Storage, *args, **kwargs
) -> dict[str, typing.Any]:
    return storage.load_file(*args, **kwargs)
from fastapi import status

from datetime import datetime
import typing
import pathlib
import os

from storages import Storage
from storages.file_operations import form_size
from utils.exceptions import NotSuchFileError, DirectoryIsNotEmpty,\
    FileTypeError

class LocalStorage(Storage):
    def __init__(self, *args, **kwargs) -> None:
        pass


    @staticmethod
    def save_file(
        path: str, 
        data: bytes | None = None, 
        file_type: typing.Literal["file", "dir"] = "file", 
        *args, 
        **kwargs
    ):
        path: pathlib.Path = pathlib.Path(path)
        
        if not path.parent.exists():
            raise FileNotFoundError(f"Directory {path.parent} doesn't exists")
            # raise NotSuchFileError(
            #     status_code=status.HTTP_404_NOT_FOUND,
            #     detail=f"Directory {path.parent} doesn't exists"
            # )

        if file_type == "file":
            with path.open("wb") as file:
                file.write(data | b"")
        elif file_type == "dir":
            path.mkdir()


    @staticmethod
    def remove_file(path: str, *args, **kwargs):
        path: pathlib.Path = pathlib.Path(path)

        try:
            if path.is_dir():
                path.rmdir()
            else:
                os.remove(path)
        except FileNotFoundError as ex_:
            raise NotSuchFileError(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"cannot find file: {path}"
            )
        except OSError:
            files = os.listdir(path)
            raise DirectoryIsNotEmpty(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"directory is not empty: {', '.join(files)}"
            )


    @staticmethod
    def load_file(path: str, *args, **kwargs) -> bytes:
        path: pathlib.Path = pathlib.Path(path)

        if path.is_dir():
            raise FileTypeError(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"cannot load directory: {path}"
            )
        
        try:
            with open(path, "rb") as file:
                data = file.read()
        except FileNotFoundError:
            raise NotSuchFileError(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"cannot find file: {path}"
            )
    
        return data


    @staticmethod
    def get_file_information(
        path: str,
        format: str = "%d.%m.%y %H:%M:%S", 
        *args, 
        **kwargs
    ) -> dict[str, typing.Any]:
        try:
            path: pathlib.Path = pathlib.Path(path)
            stat = path.stat()
        except FileNotFoundError:
            raise NotSuchFileError(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"cannot find file: {path}"
            )

        size = form_size(stat.st_size)
        file_type = "dir" if path.is_dir() else "file"
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
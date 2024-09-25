from fastapi import UploadFile
from pydantic import BaseModel, Field, BeforeValidator

from typing import Annotated, Literal, Optional


class FileModel(BaseModel):
    path: str
    description: str
    tags: list[str]
    file_type: Literal["file", "dir"]
    storage: Literal["local", "drive", "remote"]
    mimetype: str
    storage_id: Optional[str]


class UpdateFileInfoModel(BaseModel):
    description: Optional[str]
    tags: Optional[list[str]]


class FileInfoModel(FileModel):
    id: Annotated[str, BeforeValidator(str)] = Field(alias="_id")
    # path: Optional[str]
    # description: Optional[str]
    # tags: Optional[list[str]]
    # file_type: Optional[str]
    size: Optional[str]
    created: Optional[str]
    updated: Optional[str]
    worked: Optional[str]
    files: Optional[list[str]]


class FilesInfoModel(BaseModel):
    files: list[FileInfoModel]


class StorageModel(BaseModel):
    name: str
    storage: Literal["local", "drive", "remote"]
    credentials: dict[str, str]
    description: Optional[str]


class StorageInfoModel(StorageModel):
    id: Annotated[str, BeforeValidator(str)] = Field(alias="_id")


class UpdateStorageModel(BaseModel):
    name: str[Optional]
    credentials: Optional[dict[str, str]]
    description: Optional[str]
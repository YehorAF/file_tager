from typing import Annotated
from pydantic import BaseModel, Field, BeforeValidator

class FileModel(BaseModel):
    path: str
    tags: list[str]


class TagsModel(BaseModel):
    tags: list[str]


class FileInfoModel(FileModel):
    id: Annotated[str, BeforeValidator(str)] = Field(alias="_id")
    size: str
    created: str
    updated: str
    worked: str
    file_type: str
    files: list[str] | None = None


class FilesInfoModel(BaseModel):
    files: list[FileInfoModel]
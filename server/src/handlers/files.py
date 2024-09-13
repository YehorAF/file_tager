from fastapi import APIRouter, status, Query
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from typing import Annotated
from pymongo.errors import DuplicateKeyError

from databases import crud
from databases.schemas import FileModel, TagsModel, FilesInfoModel,\
    FileInfoModel
from utils.dependencies import objectid_validation
from utils.exceptions import CannotInsertFileInfoError,\
    CannotUpdateFileInfoError, CannotDeleteFileInfoError
from utils.file_operations import check_file, get_information_about_file,\
    check_tags

files_router = APIRouter()


@files_router.post("/files")
async def add_file(data: FileModel):
    tags = check_tags(data.tags)
    path, _ = check_file(data.path)

    try:
        res = await crud.insert_file({"path": path, "tags": tags})
    except DuplicateKeyError as ex_:
        raise CannotInsertFileInfoError(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(ex_)
        )

    return JSONResponse({"file_id": str(res.inserted_id)})


@files_router.get("/files", response_model=FilesInfoModel)
async def get_files(
    tags: Annotated[list[str] | None, Query()] = None, 
    limit: int = 20, 
    skip: int = 0
):
    files = await crud.find_files(tags, limit, skip)
    res_files = []

    for file in files:
        file_info = get_information_about_file(file["path"])
        res_files.append(FileInfoModel.model_validate(
            file_info | file, from_attributes=True
        ))

    return FilesInfoModel(files=res_files)


@files_router.get("/files/{file_id}", response_model=FileInfoModel)
async def get_file(file_id: str):
    file_id = objectid_validation(file_id)
    file = await crud.find_file(file_id)

    if not file:
        raise HTTPException(404, f"file not found: {file_id}")

    file_info = get_information_about_file(file["path"])

    return FileInfoModel.model_validate(
        file_info | file, from_attributes=True
    )


@files_router.put("/files/{file_id}")
async def update_file(file_id: str, data: TagsModel):
    check_tags(data.tags)
    file_id = objectid_validation(file_id)
    res = await crud.update_file_tags(file_id, data.tags)

    if res.modified_count < 1:
        raise CannotUpdateFileInfoError(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"cannot update fle by id: {file_id}"
        )

    return JSONResponse({"file_id": str(file_id)})


@files_router.delete("/files/{file_id}")
async def delete_file(file_id: str):
    file_id = objectid_validation(file_id)
    res = await crud.delete_file(file_id)

    if res.deleted_count < 1:
        raise CannotDeleteFileInfoError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"cannot delete file by id: {file_id}"
        )

    return JSONResponse({"file_id": str(file_id)})
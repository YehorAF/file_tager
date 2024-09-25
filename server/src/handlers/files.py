from fastapi import APIRouter, status, Query, File
from fastapi.exceptions import HTTPException
from fastapi.responses import Response
from pymongo.errors import DuplicateKeyError

import bson
from typing import Annotated
import pathlib

from databases import crud
from databases.schemas import FileModel, UpdateFileInfoModel, FilesInfoModel,\
    FileInfoModel
from utils.dependencies import objectid_validation
from utils.exceptions import CannotInsertFileInfoError,\
    CannotUpdateFileInfoError
from storages.file_operations import check_tags, get_storage, save_file, remove_file, load_file,\
    get_file_information

files_router = APIRouter()


@files_router.post("/files")
async def add_file(
    data: FileModel, 
    file: Annotated[bytes, File()]
):
    tags = check_tags(data.tags)
    path = pathlib.Path(data.path)
    storage_id = data.storage_id

    if data.storage == "local" and not data.storage_id:
        raise
    else:
        storage_id = bson.ObjectId(storage_id)

    ins_data = data.model_dump() | {
        "path": path, "storage_id": storage_id, "tags": tags
    }

    try:
        storage_res = await crud.find_storage(storage_id)
        
        if not storage_res:
            raise ValueError("Cannot find such storage")
        
        storage = get_storage(data.storage, **storage_res)
        file_id = save_file(
            storage, 
            path=path, 
            data=file, 
            file_type=data.file_type, 
            mimetype=data.mimetype
        )

        if file_id:
            ins_data |= {"drive_file_id": file_id}

        file_res = await crud.insert_file(ins_data)
    except DuplicateKeyError as ex_:
        remove_file(storage, path=path, file_id=file_id)
        raise CannotInsertFileInfoError(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(ex_)
        )

    return FileInfoModel(id=str(file_res.inserted_id))


@files_router.get("/files", response_model=FilesInfoModel)
async def get_files(
    tags: Annotated[list[str] | None, Query()] = None, 
    limit: int = 20, 
    skip: int = 0
):
    files = await crud.find_files(tags, limit, skip)
    
    return FilesInfoModel(files=files)


@files_router.get("/files/{file_id}", response_model=FileInfoModel)
async def get_file(file_id: str):
    file_id = objectid_validation(file_id)
    file_res = await crud.find_file(file_id)

    if not file_res:
        raise HTTPException(404, f"file not found: {file_id}")
    
    if file_res["storage"] == "local":
        storage = get_storage("local")
        file_info = get_file_information(storage, file_res["path"])
        file_res |= file_info

    return FileInfoModel.model_validate(file_res, from_attributes=True)


@files_router.get("/files/{file_id}/upload")
async def send_file(file_id: str):
    file_id = objectid_validation(file_id)
    file_res = await crud.find_file(file_id)

    if not file_res:
        raise HTTPException(404, f"file not found: {file_id}")

    if file_res["storage"] == "local":
        storage = get_storage("local")
    else:
        storage_id = objectid_validation(file_res["storage_id"])
        storage_res = await crud.find_storage(storage_id)
        storage = get_storage("local", **storage_res)
    
    file = load_file(
        storage, path=file_res, file_id=file_res.get("drive_file_id")
    )
    return Response(content=file, media_type=file_res["mimetype"])


@files_router.put("/files/{file_id}")
async def update_file(file_id: str, data: UpdateFileInfoModel):
    check_tags(data.tags)
    file_id = objectid_validation(file_id)
    res = await crud.update_file(file_id, data.model_dump())

    if res.modified_count < 1:
        raise CannotUpdateFileInfoError(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"cannot update fle by id: {file_id}"
        )

    return FileInfoModel(id=file_id)


@files_router.delete("/files/{file_id}")
async def delete_file(file_id: str):
    file_id = objectid_validation(file_id)
    file_res = await crud.find_file(file_id)

    if not file_res:
        raise HTTPException(404, f"file not found: {file_id}")
    
    if file_res["storage"] == "local":
        storage = get_storage("local")
    else:
        storage_id = objectid_validation(file_res["storage_id"])
        storage_res = await crud.find_storage(storage_id)
        storage = get_storage("local", **storage_res)

    remove_file(
        storage, path=file_res["path"], file_id=file_res.get("drive_file_id")
    )
    await crud.delete_file(file_id)
    
    return FileInfoModel(id=file_id)
from fastapi import APIRouter, status, Query, File
from fastapi.exceptions import HTTPException
from fastapi.responses import Response
from pymongo.errors import DuplicateKeyError

import bson
from typing import Annotated
import pathlib

from databases import crud
from databases.schemas import StorageModel, StorageInfoModel,\
    UpdateStorageModel, StoragesInfoModel
from utils.dependencies import objectid_validation
from utils.exceptions import CannotInsertFileInfoError,\
    CannotUpdateFileInfoError

storages_router = APIRouter()


@storages_router.post("/storages")
async def create_storage(data: StorageModel):
    try:
        storage_res = await crud.insert_storage(data.model_dump())
    except DuplicateKeyError as ex_:
        raise CannotInsertFileInfoError(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(ex_)
        )
    
    return StorageInfoModel(id=storage_res.inserted_id)


@storages_router.get("/storages")
async def get_storages( 
    limit: int = 20,
    skip: int = 0
):
    storage_res = await crud.find_storages(limit, skip)

    return StoragesInfoModel(storages=storage_res)


@storages_router.get("/storages/{storage_id}")
async def get_storage(storage_id: str):
    storage_id = objectid_validation(storage_id)
    storage_res = await crud.find_storage({"_id": storage_id})

    return StorageInfoModel.model_validate(storage_res, from_attributes=True)


@storages_router.put("/storages/{storage_id}")
async def update_storage(storage_id: str, data: UpdateStorageModel):
    storage_id = objectid_validation(storage_id)
    storage_res = await crud.update_storage(storage_id, data.model_dump())

    if storage_res.matched_count < 1:
        raise CannotUpdateFileInfoError(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"cannot update storage by id: {storage_id}"
        )

    return StorageInfoModel(id=storage_id)


@storages_router.delete("/storages/{storage_id}")
async def delete_storage(storage_id: str):
    storage_id = objectid_validation(storage_id)
    await crud.delete_storage(storage_id)

    return StorageInfoModel(id=storage_id)
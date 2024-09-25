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

storages_router = APIRouter()


@storages_router.post("/storages")
async def create_storage():
    pass


@storages_router.get("/storages")
async def get_storages():
    pass


@storages_router.get("/storages/{storage_id}")
async def get_storage(storage_id: str):
    pass


@storages_router.put("/storages/{storage_id}")
async def update_storage(storage_id: str):
    pass


@storages_router.delete("/storages/{storage_id}")
async def delete_storage(storage_id: str):
    pass
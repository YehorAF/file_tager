import bson
import typing

from databases import db


async def find_files(
    tags: list[str], limit: int, skip: int
) -> list[dict[str, typing.Any]]:
    query = {}

    if tags:
        query |= {"tags": {"$in": tags}}

    return await db.files.find(query).skip(skip).to_list(limit)


async def find_file(file_id: bson.ObjectId):
    return await db.files.find_one({"_id": file_id})


async def insert_file(data: dict):
    return await db.files.insert_one(data)


async def update_file(file_id: bson.ObjectId, data: dict):
    return await db.files.update_one({"_id": file_id}, {"$set": data})


async def delete_file(file_id: bson.ObjectId):
    return await db.files.delete_one({"_id": file_id})


async def find_storages(
    limit: int, skip: int
) -> list[dict[str, typing.Any]]:
    return await db.storages.find({}).skip(skip).to_list(limit)


async def find_storage(storage_id: bson.ObjectId):
    return await db.storages.find_one({"_id": storage_id})


async def insert_storage(data: dict):
    return await db.storages.insert_one(data)


async def update_storage(storage_id: bson.ObjectId, data: dict):
    return await db.storages.update_one({"_id": storage_id}, {"$set": data})


async def delete_storage(storage_id: bson.ObjectId):
    return await db.storages.delete_one({"_id": storage_id})
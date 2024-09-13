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


async def update_file_tags(file_id: bson.ObjectId, tags: list[str]):
    return await db.files.update_one(
        {"_id": file_id}, {"$set": {"tags": tags}}
    )


async def delete_file(file_id: bson.ObjectId):
    return await db.files.delete_one({"_id": file_id})
from fastapi import status
from fastapi.exceptions import HTTPException

import bson


def objectid_validation(id_: str):
    if not bson.ObjectId.is_valid(id_):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "invalid id")
    
    return bson.ObjectId(id_)
from fastapi import FastAPI

import settings
from handlers.files import files_router
from handlers.storages import storages_router

app = FastAPI()

app.include_router(files_router)
app.include_router(storages_router)
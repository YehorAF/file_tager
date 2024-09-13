from fastapi import FastAPI

import settings
from handlers.files import files_router

app = FastAPI()

app.include_router(files_router)
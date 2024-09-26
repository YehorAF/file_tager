from fastapi import status

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload,\
    MediaIoBaseUpload
from google.oauth2 import service_account

import io
import typing
import pathlib

from utils.exceptions import NotSuchFileError


class DriveStorage:
    def __init__(self, credentials: dict, *args, **kwargs) -> None:
        self._creds = service_account.Credentials.from_service_account_info(
            filename=credentials,
            scopes=['https://www.googleapis.com/auth/drive']
        )


    def save_file(
        self, 
        path: str, 
        data: bytes,
        mimetype: str,
        file_type: typing.Literal["file", "dir"] = "file", 
        *args, 
        **kwargs
    ) -> str:
        path: pathlib.Path = pathlib.Path(path)
        body = {
            "name": path.name
        }
        media = None

        if file_type == "dir":
            body |= {
                "mimeType": "application/vnd.google-apps.folder"
            }
        else:
            media = MediaIoBaseUpload(io.BytesIO(data), mimetype)

        try:
            with build("drive", "v3", credentials=self._creds) as service:
                file = service.files().create(
                    body=body, media_body=media, fields="id"
                ).execute()

            return file.get("id")
        except HttpError as ex_:
            raise NotSuchFileError(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"cannot save file: {ex_.error_details}"
            )
    

    def remove_file(self, file_id: str, *args, **kwargs):
        try:
            with build("drive", "v3", credentials=self._creds) as service:
                service.files().delete(fileId=file_id).execute()
        except HttpError as ex_:
            raise NotSuchFileError(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"cannot remove file: {ex_.error_details}"
            )


    def load_file(self, file_id: str, *args, **kwargs) -> bytes:
        try:
            with build("drive", "v3", credentials=self._creds) as service:
                req = service.files().get_media(fileId=file_id)
                file = io.BytesIO()
                downloader = MediaIoBaseDownload(file, req)
                done = False

                while not done:
                    _, done = downloader.next_chunk()

                return file.getvalue()
        except HttpError as ex_:
            raise NotSuchFileError(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"cannot load file: {ex_.error_details}"
            )
        

    def get_file_information(self, use_exceptions = False):
        if use_exceptions:
            raise AttributeError(
                "DriveStorage doesn't use get_file_information"
            )
        
        return None
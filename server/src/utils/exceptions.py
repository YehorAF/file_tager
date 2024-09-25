from fastapi.exceptions import HTTPException


class TagAmountError(HTTPException):
    pass


class TagContentError(HTTPException):
    pass


class CannotInsertFileInfoError(HTTPException):
    pass


class CannotUpdateFileInfoError(HTTPException):
    pass


class CannotDeleteFileInfoError(HTTPException):
    pass


class NotSuchFileError(HTTPException):
    pass


class DirectoryIsNotEmpty(HTTPException):
    pass


class FileTypeError(HTTPException):
    pass
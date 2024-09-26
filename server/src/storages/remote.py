from fabric import Connection, Config

import io
import typing
import pathlib


class RemoteStorage:
    def __init__(
        self, 
        host: str, 
        port: int | str, 
        user: str, 
        path: str, 
        *args, 
        **kwargs
    ) -> None:
        self._config = Config(runtime_ssh_path=path)
        self._host = host
        self._port = port
        self._user = user


    def save_file(
        self, 
        path: str, 
        data: bytes,
        file_type: typing.Literal["file", "dir"] = "file", 
        *args, 
        **kwargs
    ):
        path: pathlib.Path = pathlib.Path(path)
        with Connection(
            self._host, self._user, self._port, self._config
        ) as connection:
            if file_type == "dir":
                res = connection.run(f"mkdir {path}")
            else:
                res = connection.put(io.BytesIO(data), path)


    def remove_file(
        self, 
        path: str,
        file_type: typing.Literal["file", "dir"] = "file", 
        *args, 
        **kwargs
    ):
        path: pathlib.Path = pathlib.Path(path)
        
        if file_type == "dir":
            command = f"rmdir {path}"
        else:
            command = f"rm {path}"

        with Connection(
            self._host, self._user, self._port, self._config
        ) as connection:
            connection.run(command)


    def load_file(
        self,
        path: str, 
        *args, 
        **kwargs
    ) -> bytes:
        path: pathlib.Path = pathlib.Path(path)
        
        with Connection(
            self._host, self._user, self._port, self._config
        ) as connection:
            buff = io.BytesIO()
            connection.get(path, buff)

            return buff.getvalue()
        

    def get_file_information(self, use_exceptions = False):
            if use_exceptions:
                raise AttributeError(
                    "DriveStorage doesn't use get_file_information"
                )

            return None
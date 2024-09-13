import pathlib
import urllib3

from settings import HOST


class API:
    def __init__(self) -> None:
        self._pm = urllib3.PoolManager()


    def get_files(
        self, 
        tags: list[str] | None = None,
        limit: int = 20,
        skip: int = 0
    ) -> list[dict]:
        if tags:
            tags_str = "&tags=" + "&tags=".join(tags)
        else:
            tags_str = ""

        res = self._pm.request(
            "GET", HOST + f"/files?limit={limit}&skip={skip}{tags_str}"
        )
        data = res.json()
        if res.status >= 400:
            raise Exception(data["detail"])

        return data["files"]
    

    def get_file(self, file_id: str) -> dict:
        res = self._pm.request("GET", HOST + f"/files/{file_id}")
        data = res.json()
        if res.status >= 400:
            raise Exception(data["detail"])
            
        return data


    def insert_file(self, path: str, tags: list[str]) -> dict:
        res = self._pm.request(
            "POST", HOST + f"/files", json={"path": path, "tags": tags}
        )
        data = res.json()
        if res.status >= 400:
            raise Exception(data["detail"])
            
        return data


    def update_file(self, file_id: str, tags: list[str]):
        res = self._pm.request(
            "PUT", HOST + f"/files/{file_id}", json={"tags": tags}
        )
        data = res.json()
        if res.status >= 400:
            raise Exception(data["detail"])
            
        return data


    def delete_file(self, file_id: str):
        res = self._pm.request(
            "DELETE", HOST + f"/files/{file_id}"
        )
        data = res.json()
        if res.status >= 400:
            raise Exception(data["detail"])
            
        return data
    

api = API()
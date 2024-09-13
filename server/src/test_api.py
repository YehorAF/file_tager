from httpx import ASGITransport, AsyncClient

from main import app

data = {
    "../tests/files/file1.txt": {
        "error": False,
        "tags": [
            "animals", "cat", "dogs", "tree some end"
        ],
        "new_tags": [
            "tag1", "tag2", "tag3"
        ]
    },
    "/home/frog/Документи/programs/python/file_tager/server/tests/files/file1.txt": {
        "error": True,
        "tags": [
            "animals", "cat", "dogs", "tree some end"
        ],
        "new_tags": [
            "tag1", "tag2", "tag3"
        ]
    },
    "../tests/files/file2.md": {
        "error": False,
        "tags": [
            "body", "arm", "leg"
        ],
        "new_tags": [
            "tag1", "tag2", "tag3"
        ]
    },
    "file3.pdf": {
        "error": True,
        "tags": ["abc", "b", "c"]
    },
    "/home/frog/Документи/programs/python/file_tager/server/tests/files/dir": {
        "error": False,
        "tags": ["data", "pricing", "io", "info"],
        "new_tags": [
            "tag1", "tag2", "tag3"
        ]
    },
    "/home/frog/Документи/programs/python/file_tager/server/tests/files/file3.pdf": {
        "error": False,
        "tags": ["abc", "b", "c"],
        "new_tags": [
            "tag1", "tag2", "tag3"
        ]
    },
    "../tests/files/file4.txt": {
        "error": True,
        "tags": ["a", "b"]
    },
    "../tests/files/file5.txt": {
        "error": True,
        "tags": [
            "a", "b", "c"*100
        ]
    },
    "../tests/files/file6.txt": {
        "error": True,
        "tags": ["a"]*110
    }
}


async def test_file_adding():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        for k, v in list(data.items()):
            res = await ac.post("/files", json={"path": k, "tags": v["tags"]})
            resp_data = res.json()

            if v["error"]:
                assert res.status_code >= 400
                del data[k]
            else:
                assert 200 <= res.status_code < 300
                data[k] |= {"file_id": resp_data["file_id"]}


async def test_search_one_file_by_id():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        for k, v in data.items():
            res = await ac.get(f"/files/{v['file_id']}")
            resp_data = res.json()
            assert resp_data.get("_id")


async def test_search_one_file_by_tags():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        for k, v in data.items():
            res = await ac.get(f"/files", params={"tags": v["tags"]})
            resp_data = res.json()
            
            assert len(resp_data["files"]) > 0
            assert resp_data["files"][0].get("_id") == v["file_id"]


async def test_file_updating():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        for k, v in data.items():
            res = await ac.put(
                f"/files/{v['file_id']}", 
                json={"tags": v["new_tags"]}
            )
            res = await ac.get(f"/files/{v['file_id']}")
            tags = res.json().get("tags")
            assert tags == v["new_tags"]


async def test_file_deleting():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        for k, v in data.items():
            res = await ac.delete(f"/files/{v['file_id']}")
            res = await ac.get(f"/files/{v['file_id']}")
            assert res.status_code == 404
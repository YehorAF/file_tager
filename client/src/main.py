import uuid
import streamlit as st

import settings
from utils.api import api


def remove_file(file_id: str, container):
    try:
        api.delete_file(file_id)
    except Exception as ex_:
        container.error(ex_)
    else:
        files = st.session_state.get("files") or []
        files = list(filter(lambda x: x["_id"] != file_id, files))
        st.session_state.update({"files": files})


def print_files(files: list[dict]):
    st.divider()

    for file in files:
        container = st.container()
        container.text("Id: " + file["_id"])
        container.text("Path: " + file["path"])
        container.text("Size: " + file["size"])
        container.text("Created: " + file["created"])
        container.text("Updated: " + file["updated"])
        container.text("Worked: " + file["worked"])
        container.text("File type: " + file["file_type"])
        if file["file_type"] == "dir":
            container.text("File list: " + ", ".join(file["files"]))
        container.text("Tags: " + ", ".join(file["tags"]))
        container.button(
            label="Remove file", 
            key=uuid.uuid4().hex, 
            on_click=remove_file,
            args=(file["_id"], container,)
        )
        st.divider()


def remove_tag(tag: str):
    tags = st.session_state.get("tags") or set()
    try:
        tags.remove(tag)
    except Exception as ex_:
        st.error(f"Not such tags: {ex_}")
    st.session_state.update({"tags": tags})


def print_tags(tags: set[str]):
    for tag in tags:
        c1, c2 = st.columns(2)
        c1.text(tag)
        c2.button(
            "Remove tag", uuid.uuid4().hex, on_click=remove_tag, args=(tag,)
        )


st.title("File Tager")

if not st.session_state.get("files"):
    files = api.get_files()
    st.session_state.update({"files": files})
else:
    files = st.session_state["files"]

print_files(files)

action = st.radio(label="Action", options=["add file", "update file"])

if action == "add file":
    path = st.text_input("Path")
    tag = st.text_input("New tag")
    add_tag_btn = st.button("Add tag")

    if st.session_state.get("tags"):
        tags = st.session_state["tags"]
    else:
        tags = set()

    if add_tag_btn:
        tags.add(tag)
        st.session_state.update({"tags": tags})

    print_tags(tags)

    add_file_btn = st.button("Add file")

    if add_file_btn:
        tags = list(st.session_state.get("tags") or [])
        try:
            res = api.insert_file(path, tags)
        except Exception as ex_:
            st.error(ex_)
        else:
            file = api.get_file(res["file_id"])
            files = st.session_state.get("files") or []
            files.append(file)
            st.session_state.update({"files": files})
            st.rerun()
elif action == "update file":
    id_ = st.text_input("Id", key="id_input")
    tag = st.text_input("New tag")
    add_tag_btn = st.button("Add tag")

    tags = st.session_state.get("tags") or set()

    sfiles = list(filter(lambda x: x["_id"] == id_, files))
    if sfiles and not tags:
        file = sfiles[0]
        tags |= set(file["tags"])
        st.session_state.update({"tags": tags})

    if add_tag_btn:
        tags.add(tag)
        st.session_state.update({"tags": tags})

    print_tags(tags)

    c1, c2 = st.columns(2)
    update_file_btn = c1.button("Update file")
    reset_btn = c2.button("Reset")

    if update_file_btn:
        tags = list(st.session_state.get("tags") or [])
        try:
            res = api.update_file(id_, tags)
        except Exception as ex_:
            st.error(ex_)
        else:
            file = api.get_file(res["file_id"])
            files = st.session_state.get("files") or []
            files.append(file)
            st.session_state.update({"files": files})
            st.rerun()

    if reset_btn:
        try:
            del st.session_state["tags"]
            st.rerun()
        except Exception as ex_:
            pass
# utils/file.py
import os
import uuid
from fastapi import UploadFile
from aiofiles import open

UPLOAD_DIR = "media/uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


async def save_upload_file(upload_file: UploadFile, subdir: str = "") -> str:
    ext = os.path.splitext(upload_file.filename)[1]
    filename = f"{uuid.uuid4().hex}{ext}"
    dir_path = os.path.join(UPLOAD_DIR, subdir)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, filename)

    async with open(file_path, "wb") as f:
        content = await upload_file.read()
        await f.write(content)

    return os.path.join("/uploads", subdir, filename).replace("\\", "/")

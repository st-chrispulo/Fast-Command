from commands.base_command import BaseCommand
from pydantic import BaseModel
from fastapi import UploadFile
from datetime import datetime
import os, uuid, shutil
from auth.db import SessionLocal
from sqlalchemy import text


class UploadUserAvatarPayload(BaseModel):
    pass


class UploadUserAvatarCommand(BaseCommand):
    name = "upload_user_avatar"
    schema = UploadUserAvatarPayload
    require_auth = True
    method = "post"
    type = "file_upload"
    upload_dir = "uploads/avatars"
    static_mount = "/static/avatars"

    async def execute(self, payload: UploadUserAvatarPayload, file: UploadFile, user_id: str):
        MAX_FILE_SIZE_MB = 50
        ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"]

        contents = await file.read()
        file.file.seek(0)

        if file.content_type not in ALLOWED_TYPES:
            raise ValueError("Unsupported file type")

        if len(contents) > MAX_FILE_SIZE_MB * 1024 * 1024:
            raise ValueError("File size exceeds 50MB limit")

        ext = file.filename.split('.')[-1].lower()
        filename = f"{uuid.uuid4()}.{ext}"
        path = os.path.join(self.upload_dir, filename)

        db = SessionLocal()
        try:
            result = db.execute(
                text("SELECT filename FROM tbl_user_avatars WHERE user_id = :user_id"),
                {"user_id": user_id}
            ).fetchone()

            if result and result[0]:
                old_file_path = os.path.join(self.upload_dir, result[0])
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)

            with open(path, "wb") as out:
                shutil.copyfileobj(file.file, out)

            db.execute(text("DELETE FROM tbl_user_avatars WHERE user_id = :user_id"), {"user_id": user_id})
            db.execute(text("""
                INSERT INTO tbl_user_avatars (user_id, filename, uploaded_at)
                VALUES (:user_id, :filename, :uploaded_at)
            """), {
                "user_id": user_id,
                "filename": filename,
                "uploaded_at": datetime.utcnow()
            })
            db.commit()
        finally:
            db.close()

        return {
            "status": "success",
            "filename": filename,
            "url": f"/static/avatars/{filename}"
        }


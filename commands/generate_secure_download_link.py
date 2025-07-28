import os
from typing import List
from pydantic import BaseModel, field_validator
from commands.base_command import BaseCommand
from utils.file_security import create_secure_zip_link


class GenerateDownloadLinkPayload(BaseModel):
    files: List[str]

    @field_validator("files")
    @classmethod
    def check_files_exist(cls, files):
        base_root = os.path.abspath("uploads")
        missing = []

        for f in files:
            full_path = os.path.abspath(f)
            if not full_path.startswith(base_root) or not os.path.exists(full_path):
                missing.append(f)

        if missing:
            raise ValueError(f"The following files do not exist: {', '.join(missing)}")
        return files


class GenerateSecureDownloadLinkCommand(BaseCommand):
    name = "generate_secure_download_link"
    schema = GenerateDownloadLinkPayload
    require_auth = True

    upload_dir = "uploads/secure"
    static_mount = "/secure"

    async def execute(self, payload: GenerateDownloadLinkPayload, user_id: str):
        result = await create_secure_zip_link(payload.files, 'uploads/secure', user_id, self.static_mount)
        return {
            "status": "success",
            "download_url": result
        }

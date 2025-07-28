import os
import uuid
import zipfile


async def create_secure_zip_link(files: list, secure_download_dir: str, user_id: str, static_mount: str):
    zip_id = str(uuid.uuid4())
    zip_filename = f"{zip_id}.zip"
    zip_path = os.path.join(secure_download_dir, zip_filename)

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in files:
            full_path = os.path.abspath(file)
            if os.path.exists(full_path):
                arcname = os.path.basename(file)
                zipf.write(full_path, arcname=arcname)

    return f"{static_mount}/{zip_filename}"


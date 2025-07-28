from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from router import router
from logger import logger
from invoker import command_registry
import os


app = FastAPI(
    title="Fast Command API",
    description="Execute dynamic business commands via FastAPI.",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def register_static_uploads(app: FastAPI):
    mounted_paths = set()

    for command in command_registry:
        upload_dir = getattr(command, "upload_dir", None)
        static_mount = getattr(command, "static_mount", None)

        if upload_dir and static_mount and static_mount not in mounted_paths:
            os.makedirs(upload_dir, exist_ok=True)
            app.mount(static_mount, StaticFiles(directory=upload_dir), name=static_mount.strip("/"))
            mounted_paths.add(static_mount)


register_static_uploads(app)


app.include_router(router)

logger.info("Fast Command API is up.")

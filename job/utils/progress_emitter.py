import json
import os
import socket
from datetime import datetime, timezone, timedelta
from auth.token import create_access_token
import websockets


class ProgressEmitterMixin:
    async def emit_progress(self, job_id: str, status: str, message: str, percent: int = None):
        uid = f"system-{socket.gethostname()}#{os.getpid()}"
        token = create_access_token({
            "user_id": uid,
            "role": "internal"
        }, expires_delta=timedelta(days=365))

        payload = {
            "job_id": job_id,
            "status": status,
            "message": message,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "room": "broadcast",
            "user": uid
        }
        if percent is not None:
            payload["percent"] = percent

        try:
            url = f"ws://localhost:8000/ws/progress?token={token}"
            async with websockets.connect(url) as websocket:
                await websocket.send(json.dumps(payload))
        except Exception as e:
            from logger import logger
            logger.warning(f"[ProgressEmitter] WebSocket send failed: {e}")

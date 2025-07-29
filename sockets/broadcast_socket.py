from sockets.base_socket import BaseSocket


class BroadcastSocket(BaseSocket):
    def __init__(self):
        super().__init__()
        self.room_name = "broadcast"

    async def on_connect(self, socket, user: dict):
        await socket.send_text(f"🔗 Connected to {self.room_name} as {user['user_id']}")
        self.enqueue_event("connect", {"user": user})

    async def on_disconnect(self, socket):
        self.enqueue_event("disconnect", {"note": "client left"})

    async def on_message(self, payload: dict, socket, user: dict):
        msg = payload.get("message", "")
        self.enqueue_event("message", {"user": user, "payload": payload})

        await self.emit({
            "user": user["user_id"],
            "message": msg,
            "room": self.room_name
        })

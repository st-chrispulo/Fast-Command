from sockets.base_socket import BaseSocket


class ProgressSocket(BaseSocket):
    def __init__(self):
        super().__init__()
        self.room_name = "progress"

    def on_connect(self, socket, user: dict):
        socket.send_text(f"Welcome to {self.room_name}, {user['user_id']}")

    async def on_message(self, payload: dict, socket, user: dict):
        msg = payload.get("message", "")
        self.enqueue_event("message", {"user": user, "payload": payload})
        await socket.send_text(f"[{self.room_name}] {user['user_id']} says: {msg}")


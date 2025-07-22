from sockets.socket_event_queue import socket_event_queue
import time


class BaseSocket:
    def __init__(self):
        self.room_name = None

    def get_room_name(self, payload: dict = None) -> str:
        return self.room_name

    def authorize(self, socket, user: dict) -> bool:
        return True

    def on_connect(self, socket, user: dict):
        self.enqueue_event("connect", user)

    def on_disconnect(self, socket):
        self.enqueue_event("disconnect", {"note": "client disconnected"})

    def enqueue_event(self, event_type: str, data: dict):
        event = {
            "timestamp": time.time(),
            "room": self.room_name,
            "event_type": event_type,
            "data": data
        }
        socket_event_queue.put_nowait(event)

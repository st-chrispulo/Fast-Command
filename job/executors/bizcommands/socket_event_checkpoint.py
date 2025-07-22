from job.executors.bizcommands.command_base import Command
from sockets.socket_event_queue import socket_event_queue
from sqlalchemy.orm import Session
from job.models.socket_event_log import SocketEventLog
from datetime import datetime


class SocketEventCheckpointCommand(Command):
    def run(self, payload: dict = None):
        from auth.db import SessionLocal
        db: Session = SessionLocal()

        saved = 0
        try:
            while not socket_event_queue.empty():
                event = socket_event_queue.get_nowait()

                log_entry = SocketEventLog(
                    room=event["room"],
                    event_type=event["event_type"],
                    data=event["data"],
                    timestamp=datetime.utcfromtimestamp(event["timestamp"])
                )
                db.add(log_entry)
                saved += 1

            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

        return {
            "message": f"Saved {saved} socket events",
            "timestamp": datetime.utcnow().isoformat()
        }

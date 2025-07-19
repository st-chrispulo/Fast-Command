from commands.base_command import BaseCommand
from auth.db import SessionLocal
from sqlalchemy import text
from fastapi import HTTPException
from pydantic import BaseModel


class LogoutPayload(BaseModel):
    user_id: str


class LogoutCommand(BaseCommand):
    name = "logout"
    schema = LogoutPayload
    require_auth = False

    def run(self, payload: LogoutPayload):
        db = SessionLocal()
        try:
            user_id = payload.user_id

            result = db.execute(
                text("""
                    UPDATE tbl_tokens
                    SET revoked = true
                    WHERE user_id = :user_id
                    RETURNING id
                """),
                {"user_id": user_id}
            ).fetchone()

            db.commit()

            if not result:
                raise HTTPException(status_code=404, detail="No tokens found for user")

            return {"message": "Logged out successfully"}

        finally:
            db.close()

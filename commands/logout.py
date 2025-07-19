from commands.base_command import BaseCommand
from pydantic import BaseModel
from auth.db import SessionLocal
from sqlalchemy import text
from fastapi import HTTPException


class LogoutPayload(BaseModel):
    refresh_token: str


class LogoutCommand(BaseCommand):
    name = "logout"
    schema = LogoutPayload
    require_auth = False

    def run(self, payload: LogoutPayload):
        db = SessionLocal()
        try:
            result = db.execute(
                text("""
                    UPDATE tbl_tokens
                    SET revoked = true
                    WHERE refresh_token = :refresh_token
                    RETURNING id
                """),
                {"refresh_token": payload.refresh_token}
            ).fetchone()

            db.commit()

            if not result:
                raise HTTPException(status_code=404, detail="Refresh token not found")

            return {"message": "Logged out successfully"}

        finally:
            db.close()

from commands.base_command import BaseCommand
from pydantic import BaseModel
from auth.token import verify_token, create_access_token
from auth.db import SessionLocal
from fastapi import HTTPException
from sqlalchemy import text
from datetime import datetime, timedelta


class RefreshTokenPayload(BaseModel):
    refresh_token: str


class RefreshTokenCommand(BaseCommand):
    name = "refresh_token"
    schema = RefreshTokenPayload
    require_auth = False

    def run(self, payload: RefreshTokenPayload):
        db = SessionLocal()
        try:
            token_data = verify_token(payload.refresh_token)
            user_id = token_data.get("user_id")
            if not user_id:
                raise HTTPException(status_code=401, detail="Invalid refresh token")

            result = db.execute(
                text("""
                    SELECT id FROM tbl_tokens
                    WHERE user_id = :user_id
                    AND refresh_token = :refresh_token
                    AND (refresh_token_expires_at IS NULL OR refresh_token_expires_at > :now)
                    AND revoked = false
                """),
                {
                    "user_id": user_id,
                    "refresh_token": payload.refresh_token,
                    "now": datetime.utcnow()
                }
            ).fetchone()

            if not result:
                raise HTTPException(status_code=401, detail="Refresh token is invalid or expired")

            new_access_token = create_access_token({"user_id": user_id})

            db.execute(
                text("""
                    UPDATE tbl_tokens
                    SET access_token = :new_access_token,
                        expires_at = :expires_at
                    WHERE id = :token_id
                """),
                {
                    "new_access_token": new_access_token,
                    "expires_at": datetime.utcnow() + timedelta(minutes=60),
                    "token_id": result.id
                }
            )
            db.commit()

            return {
                "access_token": new_access_token,
                "token_type": "bearer",
                "expires_in": 3600
            }

        finally:
            db.close()

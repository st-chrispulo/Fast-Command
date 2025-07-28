from commands.base_command import BaseCommand
from auth.db import SessionLocal
from sqlalchemy import text
from fastapi import HTTPException
from pydantic import BaseModel, field_validator
from typing import List


class SyncPermissionPayload(BaseModel):
    user: str
    command_names: List[str]


    @field_validator("user")
    @classmethod
    def validate_user(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Username must not be empty")
        return v


    @field_validator("command_names")
    @classmethod
    def validate_commands(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("At least one command must be assigned")

        db = SessionLocal()
        try:
            result = db.execute(text("SELECT name FROM tbl_commands")).fetchall()
            allowed = set(row.name for row in result)
        finally:
            db.close()

        cleaned = set(v)
        invalid = cleaned - allowed

        if invalid:
            raise ValueError(f"Invalid command(s): {', '.join(invalid)}")

        return list(cleaned)


class SyncPermissionCommand(BaseCommand):
    name = "permission/sync"
    schema = SyncPermissionPayload
    require_auth = True

    def run(self, payload: SyncPermissionPayload):
        db = SessionLocal()
        try:
            user_row = db.execute(
                text("SELECT id FROM tbl_users WHERE username = :username"),
                {"username": payload.user}
            ).fetchone()

            if not user_row:
                raise HTTPException(status_code=404, detail=f"User '{payload.user}' not found.")

            user_id = user_row.id

            current = db.execute(
                text("SELECT command_name FROM tbl_user_permissions WHERE user_id = :user_id"),
                {"user_id": user_id}
            ).fetchall()

            current_permissions = set(row.command_name for row in current)
            new_permissions = set(payload.command_names)

            to_add = new_permissions - current_permissions
            to_remove = current_permissions - new_permissions

            for cmd in to_add:
                db.execute(
                    text("""
                        INSERT INTO tbl_user_permissions (user_id, command_name, granted_by)
                        VALUES (:user_id, :command_name, :granted_by)
                        ON CONFLICT (user_id, command_name) DO NOTHING
                    """),
                    {
                        "user_id": user_id,
                        "command_name": cmd,
                        "granted_by": user_id
                    }
                )

            for cmd in to_remove:
                db.execute(
                    text("""
                        DELETE FROM tbl_user_permissions
                        WHERE user_id = :user_id AND command_name = :command_name
                    """),
                    {
                        "user_id": user_id,
                        "command_name": cmd
                    }
                )

            db.commit()

            return {
                "status": "success",
                "added": list(to_add),
                "removed": list(to_remove)
            }

        finally:
            db.close()

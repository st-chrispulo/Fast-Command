from commands.base_command import BaseCommand
from auth.db import SessionLocal
from fastapi import HTTPException
from sqlalchemy import text
from pydantic import BaseModel, field_validator


class AssignRolePayload(BaseModel):
    user: str  # e.g., username or email
    role_name: str

    @field_validator("user")
    @classmethod
    def validate_user(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("User must not be empty")
        return v

    @field_validator("role_name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Role name must not be empty")
        return v


class AssignRoleToUserCommand(BaseCommand):
    name = "role/assign"
    schema = AssignRolePayload

    def run(self, payload: AssignRolePayload):
        db = SessionLocal()
        try:

            user_row = db.execute(
                text("SELECT id FROM tbl_users WHERE username = :username"),
                {"username": payload.user}
            ).fetchone()

            if not user_row:
                raise HTTPException(status_code=404, detail=f"User '{payload.user}' not found.")

            user_id = user_row.id

            role = db.execute(
                text("SELECT command_names FROM tbl_roles WHERE name = :name"),
                {"name": payload.role_name}
            ).fetchone()

            if not role:
                raise HTTPException(status_code=404, detail=f"Role '{payload.role_name}' not found.")

            command_names = role.command_names or []
            for command in command_names:
                db.execute(
                    text("""
                        INSERT INTO tbl_user_permissions (user_id, command_name, granted_by)
                        VALUES (:user_id, :command_name, :granted_by)
                        ON CONFLICT (user_id, command_name) DO NOTHING
                    """),
                    {
                        "user_id": user_id,
                        "command_name": command,
                        "granted_by": user_id
                    }
                )

            db.commit()
            return {"status": f"Role '{payload.role_name}' assigned to user '{payload.user}'"}
        finally:
            db.close()

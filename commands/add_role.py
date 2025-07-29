from commands.base_command import BaseCommand
from auth.db import SessionLocal
from fastapi import HTTPException
from sqlalchemy import text
from pydantic import BaseModel, field_validator
from typing import List


class AddRolePayload(BaseModel):
    name: str
    description: str
    command_names: List[str]

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Role name must not be empty")
        return v

    @field_validator("command_names")
    @classmethod
    def validate_commands(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("At least one command must be assigned")

        db = SessionLocal()
        try:
            result = db.execute(text("SELECT name FROM tbl_commands")).fetchall()
            allowed_commands = [row.name for row in result]
        finally:
            db.close()

        invalid = [cmd for cmd in v if cmd not in allowed_commands]
        if invalid:
            raise ValueError(f"Invalid command(s): {', '.join(invalid)}")

        return v


class AddRoleCommand(BaseCommand):
    name = "role/add"
    schema = AddRolePayload

    def run(self, payload: AddRolePayload):
        db = SessionLocal()
        try:
            existing = db.execute(
                text("SELECT 1 FROM tbl_roles WHERE name = :name"),
                {"name": payload.name}
            ).fetchone()

            if existing:
                raise HTTPException(status_code=400, detail=f"Role '{payload.name}' already exists.")

            db.execute(
                text("""
                    INSERT INTO tbl_roles (name, description, command_names)
                    VALUES (:name, :description, :command_names)
                """),
                {
                    "name": payload.name,
                    "description": payload.description,
                    "command_names": payload.command_names
                }
            )
            db.commit()
            return {"status": f"Role '{payload.name}' created successfully"}
        finally:
            db.close()

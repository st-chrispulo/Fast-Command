from pydantic import BaseModel, EmailStr, Field
from typing import List, Dict
from commands.base_command import BaseCommand


class GroupOwner(BaseModel):
    name: str
    email: EmailStr


class GroupUser(BaseModel):
    name: str
    role: str = Field(..., pattern="^(admin|member|viewer)$")
    email: EmailStr


class GroupSettings(BaseModel):
    allow_notifications: bool
    max_devices: int
    tags: List[str]


class CreateUserGroupSchema(BaseModel):
    group_name: str
    owner: GroupOwner
    users: List[GroupUser]
    settings: GroupSettings


class CreateUserGroupCommand(BaseCommand):
    name = "create_user_group"
    schema = CreateUserGroupSchema

    def execute(self, payload: CreateUserGroupSchema) -> dict:
        return {
            "status": "created",
            "group": payload.group_name,
            "user_count": len(payload.users),
            "owner": payload.owner.dict(),
            "settings": payload.settings.dict()
        }

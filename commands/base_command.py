from typing import Optional, Type

from fastapi import HTTPException
from pydantic import BaseModel
from auth.guard import check_permission


class BaseCommand:
    name: str
    schema: Optional[Type[BaseModel]] = None
    require_auth: bool = True
    method: str = 'POST'
    type: str = "json"
    multi_file: bool = False

    def run(self, payload: BaseModel) -> dict:
        raise NotImplementedError

    def execute(self, *args, **kwargs) -> dict:
        payload = None
        user_id = None

        if self.type == "file_upload":
            payload = kwargs.get("payload")
            user_id = kwargs.get("user_id")
            if self.require_auth:
                if not user_id:
                    raise HTTPException(status_code=401, detail="Authentication required")
                check_permission(user_id=user_id, command=self.name)

            file_data = kwargs.get("file") or kwargs.get("files")
            return self.run(payload, file_data, user_id)

        if args:
            payload = args[0]

            if isinstance(payload, dict):
                user_id = payload.get("user_id")
            else:
                user_id = getattr(payload, "user_id", None)

        user_id = user_id or kwargs.get("user_id")

        if self.require_auth:
            if not user_id:
                raise HTTPException(status_code=401, detail="Authentication required")
            check_permission(user_id=user_id, command=self.name)

        return self.run(payload)

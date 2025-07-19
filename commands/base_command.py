from pydantic import BaseModel
from auth.guard import check_permission


class BaseCommand:
    name: str
    schema: type[BaseModel]
    require_auth: bool = True

    def run(self, payload: BaseModel) -> dict:
        raise NotImplementedError

    def execute(self, payload: BaseModel) -> dict:
        if self.require_auth and hasattr(payload, "user_id"):
            check_permission(user_id=payload.user_id, command=self.name)
        return self.run(payload)

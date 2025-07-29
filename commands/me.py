from commands.base_command import BaseCommand
from fastapi import HTTPException


class MeCommand(BaseCommand):
    name = "me"
    schema = None
    require_auth = True
    method = 'GET'

    def run(self, payload):
        print(payload)
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"user_id": user_id}

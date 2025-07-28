from commands.base_command import BaseCommand
from auth.db import SessionLocal
from sqlalchemy import text


class GetCommandNamesCommand(BaseCommand):
    name = "system/commands"
    require_auth = True
    schema = None

    def run(self, payload=None):
        db = SessionLocal()
        try:
            result = db.execute(text("SELECT name FROM tbl_commands ORDER BY name")).fetchall()
            command_names = [row.name for row in result]
            return {
                "status": "success",
                "commands": command_names
            }
        finally:
            db.close()

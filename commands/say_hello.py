from pydantic import BaseModel
from commands.base import BaseCommand


class SayHelloSchema(BaseModel):
    name: str


class SayHelloCommand(BaseCommand):
    name = "say_hello"
    schema = SayHelloSchema

    def execute(self, payload: SayHelloSchema) -> dict:
        return {"message": f"Hello, {payload.name}!"}

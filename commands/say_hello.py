from commands.base_command import BaseCommand
from pydantic import BaseModel


class SayHelloPayload(BaseModel):
    name: str


class SayHelloCommand(BaseCommand):
    name = "say_hello"
    schema = SayHelloPayload

    def run(self, payload: SayHelloPayload) -> dict:
        return {"message": f"Hello, {payload.name}!"}

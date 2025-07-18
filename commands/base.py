from pydantic import BaseModel

class BaseCommand:
    name: str
    schema: type[BaseModel]

    def execute(self, payload: BaseModel) -> dict:
        raise NotImplementedError

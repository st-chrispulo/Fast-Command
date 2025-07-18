from fastapi import APIRouter
from invoker import command_registry

router = APIRouter()

for command in command_registry:
    schema = command.schema
    endpoint_name = command.name

    async def endpoint(payload: schema, cmd=command):
        return cmd.execute(payload)

    router.add_api_route(
        path=f"/{endpoint_name}",
        endpoint=endpoint,
        methods=["POST"],
        name=endpoint_name,
        summary=f"{endpoint_name} Command",
        response_model=dict
    )

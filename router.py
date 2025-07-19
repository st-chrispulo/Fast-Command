from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from invoker import command_registry
from auth.token import verify_token

router = APIRouter()
auth_scheme = HTTPBearer()


def get_user_id(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    token_payload = verify_token(credentials.credentials)
    user_id = token_payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_id


for command in command_registry:
    schema = command.schema
    endpoint_name = command.name
    http_method = command.method.upper()


    def generate_endpoint(cmd):
        if cmd.require_auth:
            if cmd.schema is None:
                async def endpoint(user_id: str = Depends(get_user_id)):
                    return cmd.execute({"user_id": user_id})
            else:
                async def endpoint(payload: cmd.schema, user_id: str = Depends(get_user_id)):
                    if hasattr(payload, "user_id"):
                        setattr(payload, "user_id", user_id)
                    return cmd.execute(payload)
        else:
            if cmd.schema is None:
                async def endpoint():
                    return cmd.execute(None)
            else:
                async def endpoint(payload: cmd.schema):
                    return cmd.execute(payload)

        return endpoint


    route_kwargs = {
        "path": f"/{endpoint_name}",
        "endpoint": generate_endpoint(command),
        "methods": [http_method],
        "name": endpoint_name,
        "summary": f"{endpoint_name} Command",
        "response_model": dict,
    }

    if not command.require_auth:
        route_kwargs["openapi_extra"] = {"security": []}

    router.add_api_route(**route_kwargs)

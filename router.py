from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from invoker import command_registry
from fastapi import WebSocket, WebSocketDisconnect
from auth.token import verify_token
from logger import logger
from sockets.socket_registry import socket_registry
from sockets.room_state import get_sockets_in_room


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


for room_name, socket_handler in socket_registry.items():
    route_path = f"/ws/{room_name}"

    def make_emit(room):
        async def emit(payload: dict):
            for ws in get_sockets_in_room(room):
                try:
                    await ws.send_json(payload)
                except Exception:
                    pass
        return emit

    socket_handler.emit = make_emit(room_name)

    # ✅ Define endpoint using bound handler
    async def websocket_endpoint(websocket: WebSocket, room=room_name, handler=socket_handler):
        token = websocket.query_params.get("token")
        if not token:
            await websocket.close(code=1008)
            return

        try:
            payload = verify_token(token)
            user = {"user_id": payload.get("user_id")}

            if not handler.authorize(websocket, user):
                await websocket.close(code=1008)
                return

            await websocket.accept()
            from sockets.room_state import add_socket_to_room, remove_socket_from_room
            add_socket_to_room(room, websocket)

            await handler.on_connect(websocket, user)

            while True:
                raw = await websocket.receive_json()
                await handler.on_message(raw, websocket, user)

        except WebSocketDisconnect:
            logger.info(f"[WebSocket:{room}] disconnected")
        except Exception as e:
            logger.info(f"[WebSocket:{room}] error:", e)
            await websocket.close(code=1008)
        finally:
            from sockets.room_state import remove_socket_from_room
            remove_socket_from_room(room, websocket)
            await handler.on_disconnect(websocket)

    router.add_api_websocket_route(route_path, websocket_endpoint, name=room_name)

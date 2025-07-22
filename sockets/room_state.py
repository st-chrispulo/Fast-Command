from collections import defaultdict

room_connections = defaultdict(list)


def add_socket_to_room(room: str, websocket):
    if websocket not in room_connections[room]:
        room_connections[room].append(websocket)


def remove_socket_from_room(room: str, websocket):
    if websocket in room_connections[room]:
        room_connections[room].remove(websocket)
        if not room_connections[room]:
            del room_connections[room]


def get_sockets_in_room(room: str):
    return room_connections.get(room, [])

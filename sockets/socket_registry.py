from sockets.progress_socket import ProgressSocket
from sockets.broadcast_socket import BroadcastSocket

socket_registry = {
    "progress": ProgressSocket(),
    "broadcast": BroadcastSocket(),
}

from asyncio import create_task, get_event_loop
from socket import socket, AF_INET, SOCK_STREAM, IPPROTO_TCP, TCP_NODELAY

from src.net.debug import debug


class ClientListener(object):
    """Server connection listener for incoming client socket connections

    Parameters
    -----------
    parent: :class:`ServerBase`
        The running server
    connection: Tuple[str, int]
        The connection IP and Port the socket listens on

    Attribtues
    ----------
    is_alive: bool
        The servers current alive status

    """

    def __init__(self, parent, connection):
        self._connection = connection
        self._parent = parent
        self._loop = parent._loop if parent._loop else get_event_loop()

        self._serv_sock = socket(AF_INET, SOCK_STREAM)
        self._serv_sock.setblocking(False)
        self._serv_sock.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
        self._serv_sock.bind(self._connection)
        self._serv_sock.listen(0)

    def is_alive(self):
        return self._parent.is_alive

    async def _listen(self):
        debug.logs(
            f"{self._parent.name} Listening on port {self._connection[1]}")

        while self.is_alive:
            client_sock, _ = await self._loop.sock_accept(self._serv_sock)
            client_sock.setblocking(False)
            client_sock.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)

            create_task(self._parent.on_client_accepted(client_sock))

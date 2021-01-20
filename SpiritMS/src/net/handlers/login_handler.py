from src.net.handlers.packet_handler import packet_handler
from src.net.login.login import Login
from src.net.packets.recv_ops import InPacket
from src.net.packets.send_ops import OutPacket
from src.net.server import server_constants


class LoginHandler:

    @packet_handler(opcode=InPacket.PERMISSION_REQUEST)
    async def handle_permission_request(self, client, packet):
        locale = packet.decode_byte()
        version = packet.decode_short()
        minor_version = packet.decode_string()
        if locale != server_constants.LOCALE or version != server_constants.SERVER_VERSION:
            client.close()

    @packet_handler(opcode=InPacket.USE_AUTH_SERVER)
    async def handle_auth_server(self, client, packet):
        await client.send_packet(Login.send_auth_server(False))

    @packet_handler(opcode=InPacket.CLIENT_START)
    async def handle_client_start(self, client, packet):
        await client.send_packet(Login.send_start_client())

    @packet_handler(opcode=InPacket.PRIVATE_SERVER_PACKET)
    async def handle_private_server_packet(self, client, packet):
        await client.send_packet(Login.send_auth_response(
            OutPacket.PRIVATE_SERVER_PACKET.value ^ packet.decode_int()
        ))
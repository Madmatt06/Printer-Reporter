import asyncio
from typing import Optional, Any
from collections.abc import Callable, Awaitable
import logging

HOST = '0.0.0.0'
PORT = 9153

logger = logging.getLogger(f'printer_manager_server.{__name__}')


async def get_message_dynamic(reader: asyncio.StreamReader) -> Optional[bytes]:
  request = await reader.readexactly(4)
  expected_size:int = int.from_bytes(request)
  # TODO: Determine appropriate max size for message
  request:bytes = await reader.readexactly(expected_size)
  return request


class Server:
  def __init__(self, test:Callable[[str], Awaitable[bool]]):
    self.server:Optional[asyncio.Server] = None
    self.addr:str = ""
    self.test:Callable[[str], Awaitable[bool]] = test

  #TODO: Finish handle connection to be able to execute commands and timeout.
  async def handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    print("received connection request. reading...")
    ip, port = writer.get_extra_info('peername')[:2]
    logger.info(f'Client connected from ip: {ip}, port: {port}')
    received:bytes = await reader.readexactly(1)
    command_received:int = int.from_bytes(received)
    if command_received == 1:
      print("told to send. sending...")
      logger.info(f'{ip} : {port} sent "send". Sending message through discord')
      await self.test('Test')
    logger.info(f'Closing connection with {ip} : {port}')
    writer.close()
    await writer.wait_closed()
    logger.info(f'{ip} : {port} Connection closed')

  async def create_server(self):
    self.server = await asyncio.start_server(self.handle_connection, HOST, PORT)
    self.addr = self.server.sockets[0].getsockname()
    logger.info(f'Serving on address: {self.addr}')
    async with self.server:
      await self.server.serve_forever()
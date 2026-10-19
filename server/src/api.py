import asyncio
from typing import Optional, Any
from collections.abc import Callable, Awaitable
import logging

HOST = '0.0.0.0'
PORT = 9153

logger = logging.getLogger(f'printer_manager_server.{__name__}')

class Server:
  def __init__(self, test:Callable[[int], Awaitable[bool]]):
    self.server:Optional[asyncio.Server] = None
    self.addr:str = ""
    self.test:Callable[[int], Awaitable[bool]] = test

  async def handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    print("received connection request. reading...")
    ip, port = writer.get_extra_info('peername')[:2]
    logger.info(f'Client connected from ip: {ip}, port: {port}')
    request = await reader.readexactly(4)
    if request == b"send":
      print("told to send. sending...")
      logger.info(f'{ip} : {port} sent "send". Sending message through discord')
      await self.test(1151964402103373855)
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
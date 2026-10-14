import asyncio
from typing import Optional, Any
from collections.abc import Callable, Awaitable
HOST = '0.0.0.0'
PORT = 9153
class Server:
  def __init__(self, test:Callable[[int], Awaitable[bool]]):
    self.server:Optional[asyncio.Server] = None
    self.addr:str = ""
    self.test:Callable[[int], Awaitable[bool]] = test

  async def handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    request = await reader.readexactly(4)
    if request == b"send":
      await self.test(1151964402103373855)
    writer.close()
    await writer.wait_closed()

  async def create_server(self):
    self.server = await asyncio.start_server(self.handle_connection, HOST, PORT)
    self.addr = self.server.sockets[0].getsockname()
    print(f'Serving on address: {self.addr}')
    async with self.server:
      await self.server.serve_forever()
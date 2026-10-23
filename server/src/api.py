import asyncio
from typing import Optional, Any
from collections.abc import Callable, Awaitable
import logging
from data_types import Request, DataType, Completion

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
  def __init__(self, test:Callable[[str], Awaitable[bool]], get_connection:Callable[None, Awaitable[int]]):
    self.server:Optional[asyncio.Server] = None
    self.addr:str = ""
    self.test:Callable[[str], Awaitable[bool]] = test
    self.get_connection:Callable[None, Awaitable[int]] = get_connection

  #TODO: Finish handle connection to be able to execute commands and timeout.
  async def handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    ip, port = writer.get_extra_info('peername')[:2]
    logger.info(f'Client connected from ip: {ip}, port: {port}')
    received:bytes = await reader.readexactly(1)
    command_received:int = int.from_bytes(received)
    if command_received == Request.GET.value:
      received = await reader.readexactly(1)
      command_received = int.from_bytes(received)
      if command_received == DataType.CONNECTION_CHECK.value:
        conn_status:int = await self.get_connection()
        writer.write(conn_status.to_bytes())
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        return
      elif command_received == DataType.PRINTER.value:
        writer.write((1).to_bytes())
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        return
      elif command_received == DataType.JOB.value:
        writer.write((1).to_bytes())
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        return
      else:
        writer.write(Completion.ERROR.value.to_bytes())
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        return
    elif command_received == Request.ADD.value:
      if command_received == DataType.PRINTER.value:
        writer.write((1).to_bytes())
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        return
      elif command_received == DataType.JOB.value:
        writer.write((1).to_bytes())
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        return
      else:
        writer.write(Completion.ERROR.value.to_bytes())
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        return
    elif command_received == Request.EDIT.value:
      if command_received == DataType.PRINTER.value:
        writer.write((1).to_bytes())
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        return
      elif command_received == DataType.JOB.value:
        writer.write((1).to_bytes())
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        return
      else:
        writer.write(Completion.ERROR.value.to_bytes())
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        return
    else:
      writer.write(Completion.ERROR.value.to_bytes())
      await writer.drain()
      writer.close()
      await writer.wait_closed()
      return

  async def create_server(self):
    self.server = await asyncio.start_server(self.handle_connection, HOST, PORT)
    self.addr = self.server.sockets[0].getsockname()
    logger.info(f'Serving on address: {self.addr}')
    async with self.server:
      await self.server.serve_forever()
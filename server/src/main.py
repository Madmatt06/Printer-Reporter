import asyncio
import api
import bot
import logging

logger = logging.getLogger('printer_manager_server')
async def main():
  logger.info('Starting Discord Bot')
  discord_bot:bot.BotClient = bot.BotClient()
  logger.info('Starting api server')
  server:api.Server = api.Server(discord_bot.inform)
  await asyncio.gather(server.create_server(), discord_bot.start_bot())

if __name__ == "__main__":
  logger.info('Starting async loop.')
  asyncio.run(main())
import asyncio
import api
import bot
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='printer_manager_server.log',
    filemode='a',
    encoding='utf-8'
)
logger = logging.getLogger('printer_manager_server')
async def main():
  logger.info('Starting Discord Bot')
  discord_bot:bot.BotClient = bot.BotClient()
  logger.info('Starting api server')
  server:api.Server = api.Server(discord_bot.inform, discord_bot.get_connection)
  await asyncio.gather(server.create_server(), discord_bot.start_bot())

if __name__ == "__main__":
  logger.info('Starting async loop.')
  asyncio.run(main())
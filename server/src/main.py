import asyncio
import api
import bot

async def main():
  discord_bot:bot.BotClient = bot.BotClient()
  server:api.Server = api.Server(discord_bot.inform)
  await asyncio.gather(server.create_server(), discord_bot.start_bot())

if __name__ == "__main__":
  asyncio.run(main())
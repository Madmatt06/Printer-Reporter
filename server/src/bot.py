import discord
from discord.ext import commands
from discord import app_commands
import settings
from typing import Optional
import logging

logger = logging.getLogger(f'printer_manager_server.{__name__}')

class BotClient:
  def __init__(self):
    intents = discord.Intents.default()
    intents.members = True
    self.bot = commands.Bot(command_prefix='#', intents=intents)
    self.active_channel:Optional[int] = None
    self.setup_commands()

  async def start_bot(self):
    async with self.bot:
      await self.bot.start(settings.DISCORD_API_SECRET)


  # Function Callbacks to allow external interaction with the discord bot
  async def inform(self, message:str) -> bool:
    logger.info('Sending message through discord bot')
    channel:discord.TextChannel = self.bot.get_channel(self.active_channel)
    if channel is not None:
      try:
        await channel.send(content=f"{message}")
      except (discord.HTTPException, discord.Forbidden, discord.NotFound) as e:
        logger.error(f'Error sending message, got {e}')
        return False
      return True
    return False

  def setup_commands(self):
    @self.bot.tree.command(name="sync")
    async def sync(interaction: discord.Interaction):
      logger.info('Syncing commands')
      await interaction.response.send_message(content='Syncing', ephemeral=True)
      await self.bot.tree.sync()

    @self.bot.tree.command(name="set-channel")
    async def set_channel(interaction: discord.Interaction):
      logger.info('Changing active channel')
      self.active_channel = interaction.channel_id
      await interaction.response.send_message(content='Messages will be sent here now', ephemeral=True)
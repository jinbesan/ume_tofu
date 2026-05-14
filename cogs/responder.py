import discord
from discord.ext import commands
import random
import os
from utils.llm import LLMClient


RESPONSE_CHANCE = float(os.getenv("RESPONSE_CHANCE", "0.01"))
RESPONSE_CHANCE_HELP = float(os.getenv("RESPONSE_CHANCE_HELP", "0.5"))
RESPONSE_CHANCE_SHRIMP = float(os.getenv("RESPONSE_CHANCE_SHRIMP", "0.3"))
RESPONSE_CHANCE_MENTIONED = float(os.getenv("RESPONSE_CHANCE_MENTIONED", "0.5"))
command_prefix = "ume "


class ResponderCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.llm_client = LLMClient()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        if message.author.bot:
            return

        if message.content.startswith(command_prefix):
            return

        msg_lower = message.content.lower()


        if self.bot.user in message.mentions:
            chance = RESPONSE_CHANCE_MENTIONED
        elif msg_lower == "help":
            chance = RESPONSE_CHANCE_HELP
        elif "shrimp" in msg_lower or "pink" in msg_lower:
            chance = RESPONSE_CHANCE_SHRIMP
        else:
            chance = RESPONSE_CHANCE

        if random.random() > chance:
            return

        response = self.llm_client.get_response(message.content)
        if response:
            await message.channel.send(response)


async def setup(bot):
    await bot.add_cog(ResponderCog(bot))
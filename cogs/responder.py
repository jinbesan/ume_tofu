import discord
from discord.ext import commands
import random
import os
from utils.llm import LLMClient


RESPONSE_CHANCE = float(os.getenv("RESPONSE_CHANCE", "0.01"))
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

        if random.random() > RESPONSE_CHANCE:
            return

        response = self.llm_client.get_response(message.content)
        if response:
            await message.channel.send(response)


async def setup(bot):
    await bot.add_cog(ResponderCog(bot))
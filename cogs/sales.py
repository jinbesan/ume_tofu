import discord
from discord.ext import commands
import tracker


command_prefix = "ume "


class SalesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        msg = message.content

        if msg.startswith(command_prefix + "add"):
            content = msg.split(command_prefix + "add ", 1)[1]
            user = message.author.name
            items = tracker.update_sheet(content, user)
            await message.channel.send("\n".join(items))

        if msg.startswith(command_prefix + "undo"):
            user = message.author.name
            items = tracker.undo(user)
            if items:
                await message.channel.send("\n".join(items))
            else:
                await message.channel.send("No items to undo.")


async def setup(bot):
    await bot.add_cog(SalesCog(bot))
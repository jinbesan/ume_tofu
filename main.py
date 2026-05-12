import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from cogs import basic, sales, responder


load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix="ume ")


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await bot.add_cog(basic.BasicCog(bot))
    await bot.add_cog(sales.SalesCog(bot))
    await bot.add_cog(responder.ResponderCog(bot))


token = os.getenv("DISCORD_TOKEN")
if token is None:
    raise ValueError("DISCORD_TOKEN environment variable not set")
bot.run(token)
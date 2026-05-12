import discord
from discord.ext import commands
import requests
import json
import os
from dotenv import load_dotenv


load_dotenv()


command_prefix = "ume "

wandahoi_keywords = ["wandahoi", "wonderhoy", "WANDAHOI", "WONDERHOY"]

data_store = {"responding": True}


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]["q"] + " -" + json_data[0]["a"]
    return quote


class BasicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        msg = message.content

        if msg.startswith(command_prefix + "inspire"):
            quote = get_quote()
            await message.channel.send(quote)

        if msg.startswith(command_prefix + "hello"):
            embed = discord.Embed(title="Hello!", description="ume tofu loves you!", color=0x00ff00)
            file = discord.File("pictures/29612542x.png", filename="29612542x.png")
            embed.set_image(url="attachment://29612542x.png")
            await message.channel.send(file=file, embed=embed)

        if msg.startswith(command_prefix + "responding"):
            value = msg.split(command_prefix + "responding ", 1)[1]
            if value.lower() == "true":
                data_store["responding"] = True
                await message.channel.send("Responding is on.")
            else:
                data_store["responding"] = False
                await message.channel.send("Responding is off.")

        if msg.startswith(command_prefix + "help"):
            help_message = (
                "Available commands:\n"
                f"{command_prefix}inspire - Get an inspirational quote\n"
                f"{command_prefix}hello - Greet the bot\n"
                f"{command_prefix}responding <true/false> - Toggle LLM responding\n"
                f"{command_prefix}add <item1, item2, ...> - Add items to the sheet\n"
                f"{command_prefix}undo - Undo the last transaction\n"
                f"{command_prefix}help - Show this help message\n"
                "-----------------------------------------------------------------------------\n"
                "Link to test sheet: https://docs.google.com/spreadsheets/d/1cu66ZGH9HkBEoLB2FMVyPOXS7PaZ7oxfLg9ba3VwD5E/edit?usp=sharing"
            )
            await message.channel.send(help_message)

        if any(word in msg for word in wandahoi_keywords):
            embed = discord.Embed(title="wandahoi!!!!!", description="ume tofu wandahoi!", color=0xffc0cb)
            embed.set_image(url="attachment://wandahoi.jpg")
            file = discord.File("pictures/wandahoi.jpg", filename="wandahoi.jpg")
            await message.channel.send(file=file, embed=embed)


async def setup(bot):
    await bot.add_cog(BasicCog(bot))
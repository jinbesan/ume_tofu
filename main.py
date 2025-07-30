import discord
import os
import requests
import json
import random
from dotenv import load_dotenv
import tracker  # Import the tracker module to use its functions

# Load environment variables from .env file
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
command_prefix = "ume "


# Initialize our data storage as a regular dictionary
data_store = {}

sad_words = ["sad",
            "depressed",
            "unhappy",
            "angry",
            "miserable",
            "frustrated",
            "upset",
            "disappointed",
            "lonely",
            "hurt",
            "kill myself",
            "help"]
starter_encouragements = [
    "ume tofu loves you!",
    "ume tofu is here for you!",
    "ume tofu is your friend!",
    "ume tofu is always here to help!",
    "ume tofu believes in you!",
    "ume tofu is cheering for you!",
    "ume tofu is rooting for you!",
    "ume tofu is your biggest fan!",
    "ume encourage!"
]
wandahoi = ["wandahoi",
            "wonderhoy",
            "WANDAHOI",
            "WONDERHOY"]

if "responding" not in data_store.keys():
  data_store["responding"] = True


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)

def update_encouragements(encouraging_message):
  if "encouragements" in data_store.keys():
    encouragements = data_store["encouragements"]
    encouragements.append(encouraging_message)
    data_store["encouragements"] = encouragements
  else:
    data_store["encouragements"] = [encouraging_message]

def delete_encouragment(index):
  if "encouragements" in data_store.keys():
    encouragements = data_store["encouragements"]
    if len(encouragements) > index:
      del encouragements[index]
    data_store["encouragements"] = encouragements



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith(command_prefix + 'inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if msg.startswith(command_prefix + 'hello'):
        embed = discord.Embed(title="Hello!", description="ume tofu loves you!", color=0x00ff00) #creates embed
        file = discord.File("pictures/29612542x.png", filename="29612542x.png")
        embed.set_image(url="attachment://29612542x.png")
        await message.channel.send(file=file, embed=embed)

    if data_store["responding"]:
        options = starter_encouragements
        if "encouragements" in data_store.keys():
            options = options + data_store["encouragements"]

        if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(options))

    if any(word in msg for word in wandahoi):
       embed = discord.Embed(title="wandahoi!!!!!", description="ume tofu wandahoi!", color=0xffc0cb)
       embed.set_image(url="attachment://wandahoi.jpg")
       file = discord.File("pictures/wandahoi.jpg", filename="wandahoi.jpg")
       await message.channel.send(file=file, embed=embed)

    if msg.startswith(command_prefix + "responding"):
        value = msg.split(command_prefix + "responding ",1)[1]

        if value.lower() == "true":
            data_store["responding"] = True
            await message.channel.send("Responding is on.")
        else:
            data_store["responding"] = False
            await message.channel.send("Responding is off.")

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

    if msg.startswith(command_prefix + "help"):
        help_message = (
            "Available commands:\n"
            f"{command_prefix}inspire - Get an inspirational quote\n"
            f"{command_prefix}hello - Greet the bot\n"
            f"{command_prefix}responding <true/false> - Toggle responding to sad messages\n"
            f"{command_prefix}add <item1, item2, ...> - Add items to the sheet\n"
            f"{command_prefix}help - Show this help message\n"
            "-----------------------------------------------------------------------------\n"
            "Link to test sheet: https://docs.google.com/spreadsheets/d/1cu66ZGH9HkBEoLB2FMVyPOXS7PaZ7oxfLg9ba3VwD5E/edit?usp=sharing"
        )
        await message.channel.send(help_message)


token = os.getenv('TOKEN')
if token is None:
    raise ValueError("TOKEN environment variable not set")
client.run(token)

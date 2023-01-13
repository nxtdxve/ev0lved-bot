import os
import asyncio
from dotenv import load_dotenv
import openai
import discord
from discord.ext import commands
from discord import app_commands

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)


class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild = discord.Object(id = 1040978541363343471))
            self.synced = True
        print("Logged in as {0.user}".format(self))


client = aclient()
tree = app_commands.CommandTree(client)


@tree.command(name="ping", description="Ping the user", guild=discord.Object(id=1040978541363343471))
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@tree.command(name="openai", description="Generate a response using OpenAI", guild=discord.Object(id=1040978541363343471))
async def openai_response(interaction: discord.Interaction, *, prompt: str):
    try:
        response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt
    )
    except openai.error.RateLimitError as e:
        await interaction.response.send_message("Rate limit exceeded.")
    else:
        await interaction.response.send_message(response["choices"][0]["text"])

client.run(TOKEN)

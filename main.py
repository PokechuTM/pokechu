import discord
from discord.ext import commands
import aiohttp
import os
from asyncdagpi import Client as DagpiClient
from dotenv import load_dotenv
import json
from types import SimpleNamespace
#from config import config
from typing import List, Optional
from disputils import BotEmbedPaginator
import functools

class PokeBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        load_dotenv()
        session_headers = {
            "User-Agent" : "PokeFun | DiscordBot"
        }
        self.session = aiohttp.ClientSession(headers = session_headers)
        self.dagpi = DagpiClient(os.getenv("DAGPI_TOKEN"))
        


        for cog in os.listdir("./cogs"):
            if cog.endswith(".py"):
                ext = cog[:-3]
                try:
                    self.load_extension("cogs." + ext)
                except Exception as e:
                    print(e)

        self.load_extension("jishaku")

    async def build_paginator(self, ctx : commands.Context, embeds : List[discord.Embed], message : Optional[discord.Message] = None):
        partial = functools.partial(BotEmbedPaginator, ctx, embeds, message)
        return await self.loop.run_in_executor(None, partial)

        
    async def on_ready(self):
        print(f"{self.user} Connected to Gateway")
        print(f"User ID: {self.user.id}")
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Pokémon"))


    def run(self, token : str):
        super().run(token)


    

if  __name__ == "__main__":
    intents = discord.Intents.default()
    intents.members = True
    intents.presences = True
    bot = PokeBot(command_prefix = commands.when_mentioned_or("p!", "P!"), intents = intents)
    bot.run(os.getenv("CLIENT_TOKEN"))
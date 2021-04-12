import discord
from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter
import os
import asyncio
import aiohttp
class Heartbeat(commands.Cog):
    def __init__(self, client):
        self.client = client

    """@commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(os.getenv("HEARTBEAT_HOOK"), adapter=AsyncWebhookAdapter(session))
            await webhook.send(error)"""




def setup(client):
    client.add_cog(Heartbeat(client))
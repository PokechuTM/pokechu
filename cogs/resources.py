import discord
from discord.ext import commands
import aiohttp
from config import emojis, colours

class Resources(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(usage = "<berry name>", description = "Returns detailed information about a certain berry!", help = "Returns detailed information about a certain berry!")
    async def berry(self, ctx, *, berry_name : str):
        async with self.client.session.get("https://pokeapi.co/api/v2/berry/{}/".format(berry_name)) as response:
            try:
                data = await response.json()
            except aiohttp.client_exceptions.ContentTypeError:
                return await ctx.send("{} Oops! You've given me an invalid Berry Name/ID".format(emojis.get("ohgodnoduck")))
            
            print(data)
            name = data.get("name")
            growth_time = data.get("growth_time")
            natural_gift_power = data.get("natural_gift_power")
            size = data.get("size")
            smoothness = data.get("smoothness")
            soil_dryness = data.get("soil_dryness")
            max_harvest = data.get("max_harvest")
            item = data.get("item")
            item_url = item.get("url")
            async with self.client.session.get(item_url) as item_response:
                item_data = await item_response.json()
                effect_entries = item_data.get("effect_entries")
                entry = effect_entries[0]
                effect = entry.get("effect").replace(":", "")


            embed = discord.Embed(
                title = name.title(),
                description = effect,
                colour = colours.get("embedcolour")
            )
            embed.add_field(name = "Growth Time", value = growth_time, inline = True)
            embed.add_field(name = "Size", value = size, inline = True)
            embed.add_field(name = "Smoothness", value = smoothness, inline = True)
            embed.add_field(name = "Max Harvest", value = max_harvest, inline = True)
            embed.add_field(name = "Soil Dryness", value = soil_dryness, inline = True)
            embed.add_field(name = "Natural Gift Power", value = natural_gift_power, inline = True)
            await ctx.send(embed = embed)




def setup(client):
    client.add_cog(Resources(client))
import discord
import aiohttp
from config import colours
from datetime import datetime
async def get_poke_data(pokemon_name : str, session : aiohttp.ClientSession) -> discord.Embed:
    pokemon_name = pokemon_name.lower()

    async with session.get("https://pokeapi.co/api/v2/pokemon/{}/".format(pokemon_name)) as response:
        data = await response.json()
    sprites = data.get("sprites")
    sprite = sprites.get("front_default")
    stats = data.get("stats")
    embed = discord.Embed(
        title = "Pokemon Searcher",
        description = "Query: `{}`".format(pokemon_name),
        colour = colours.get("embedcolour"),
        timestamp = datetime.utcnow()
    )
    for stat in stats:
        base_stat = stat.get("base_stat")
        effort = stat.get("effort")
        name = stat.get("stat").get("name")
        if "-" in name:
            name = name.replace("-", " ").title()

        name = name.title()
        print(str(effort))
        if str(effort) == "None":
            effort = 0

        embed.add_field(name = name, value = f"**Base Stat:** {base_stat}\n**Effort:** {effort}", inline = True)

    embed.set_thumbnail(url = sprite)
    #embed.set_footer(text = f"Requested by: {ctx.author}", icon_url = self.client.user.avatar_url)
    return embed
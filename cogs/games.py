import discord
from discord.ext import commands
from config import colours, emojis
import asyncio

class Games(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(usage = "", description = "Play a fun round of What's That Pokemon!", help = "Play a fun round of What's That Pokemon!")
    async def wtp(self, ctx):
        data = await self.client.dagpi.wtp()
        print(dir(data))
        answer = data.answer
        question = data.question
        name = data.name
        print(name)
        embed = discord.Embed(
            colour = colours.get("embedcolour"),
            title = "What's that Pokemon?"
        )
        embed.set_footer(text = "You have 30 seconds to send the correct pokemon name into the chat!", icon_url = ctx.author.avatar_url)
        embed.set_image(url = question)
        question_msg = await ctx.send(embed = embed)
        def check(m):
            if m.author.id == ctx.author.id:
                if m.channel.id == ctx.channel.id:
                    if name.lower() in m.content.lower():
                        return True

        try:
            await self.client.wait_for("message", check = check, timeout = 30.00)
        except asyncio.TimeoutError:
            await question_msg.delete()
            image = discord.Embed(colour = colours.get("embedcolour"))
            image.set_image(url = answer)
            return await ctx.send("{} Oh no! You weren't able to figure out who it was! The answer was: `{}`".format(emojis.get("ohgodnoduck"), name), embed = image)

        await question_msg.delete()
        image = discord.Embed(colour = colours.get("embedcolour"))
        image.set_image(url = answer)
        return await ctx.send("{} Amazing! The answer indeed was `{}`".format(emojis.get("pikaluv"), name), embed = image)



        




def setup(client):
    client.add_cog(Games(client))
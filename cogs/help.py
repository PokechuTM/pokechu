import discord
from discord.ext import commands
from config import colours


ignore_cogs = ["heartbeat", "jishaku"]

class MyHelp(commands.HelpCommand):
    def get_command_signature(self, command):
        return '%s%s %s' % (self.clean_prefix, command.qualified_name, command.signature)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(colour = colours.get("embedcolour"))
        embed.set_author(name = f"Help Panel", icon_url = "https://media.discordapp.net/attachments/773312837623218247/831144072675721226/pokemon-4657023_1280.png?width=673&height=676")
        for cog, commands in mapping.items():
            try:
                if str(cog.qualified_name).lower() in ignore_cogs:
                    continue
            except:
                pass
            filtered = await self.filter_commands(commands, sort=True)
            command_signatures = [self.get_command_signature(c) for c in filtered]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        channel = self.get_destination()
        embed.set_image(url = "https://media.discordapp.net/attachments/830418498353758210/831170515476545556/yRuy1adRSkIfJHXCrgJ9QPxIMW6yVbbuR857MlZXdJfeMnblA0YLRbttRMlnZXSJyYmZ4cCMZX5NPUeMODtJFCNs5Ttw9csy2cnC.png")
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(colour = colours.get("embedcolour"))
        embed.set_author(name = self.get_command_signature(command), icon_url = "https://media.discordapp.net/attachments/773312837623218247/831144072675721226/pokemon-4657023_1280.png?width=673&height=676")
        embed.add_field(name="Help", value=command.help)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)


class MyCog(commands.Cog, name = "Help"):
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        self.bot = bot
        bot.help_command = MyHelp()
        bot.help_command.cog = self
        
    def cog_unload(self):
        self.bot.help_command = self._original_help_command




def setup(client):
    client.add_cog(MyCog(client))
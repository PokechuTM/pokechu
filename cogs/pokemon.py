import discord
from discord.ext import commands
from bs4 import BeautifulSoup as bs
from io import BytesIO
from tools import imagemanip
from config import colours, emojis
import functools
from tools import api
import os
class Pokemon(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.base = "https://pokeapi.co/api/v2"

    @commands.command(usage = "<pokemon name>", description = "Returns detailed stats about a pokemon!", help = "Returns detailed stats about a pokemon!")
    async def pokemon(self, ctx, *, pokemon_name : str):
        url = "https://api.pokemon.com/us/pokedex/{}".format(pokemon_name.lower())
        loading_msg = await ctx.send(f"{emojis.get('loading')} Asking Ash for his PokeDex")
        async with self.client.session.get(url) as response:
            content = await response.text()
            soup = bs(content, "html.parser")
            profile_class = soup.find("div", class_ = "pokedex-pokemon-profile")
            active_image = profile_class.find("div", class_ = "profile-images").find("img", class_ = "active")["src"]
            descriptions = soup.find("div", class_ = "pokedex-pokemon-details-right")
            descriptions = descriptions.find_all("p")
            description = "No Description Found"
            set_desc = False
            for x in descriptions:
                if set_desc:
                    continue
                if "active" in str(x).lower():
                    description = str(x.text)
                    description = description.lstrip()
                    description = description.rstrip()
                    set_desc = True
            ability_class = soup.find("div", class_ = "pokemon-ability-info color-bg color-lightblue match active")
            attrs = ability_class.find_all("li")
            height = "nil"
            gender = "nil"
            abilities = "nil"
            weight = "nil"
            category = "nil"
            #print(attrs[0].find_all("span"))
            keys = ["height", "gender", "weight", "category", "abilities"]
            for attr in attrs:
                spans = attr.find_all("span")
                for span in spans:
                    if span["class"][0] == "attribute-title":
                        if span.text.lower().lstrip().rstrip() not in keys:
                            continue
                        span_text = span.text.lower().lstrip().rstrip()
                        if span_text == "height":
                            value = attr.find("span", class_ = "attribute-value")
                            value = value.text
                            height = value

                        elif span_text == "abilities":
                            value = attr.find("span", class_ = "attribute-value")
                            value = value.text
                            abilities = value

                        elif span_text == "weight":
                            value = attr.find("span", class_ = "attribute-value")
                            value = value.text
                            weight = value

                        elif span_text == "category":
                            value = attr.find("span", class_ = "attribute-value")
                            value = value.text
                            category = value

                        elif span_text == "gender":
                            value = attr.find("span", class_ = "attribute-value")
                            male = False
                            female = False
                            for x in value.find_all("i"):
                                print(x)
                                print(x["class"])
                                if x["class"][1] == "icon_male_symbol":
                                    male = True
                                if x["class"][1] == "icon_female_symbol":
                                    female = True

                            actual_value = ""
                            if male == True and female == True:
                                print("both true")
                                actual_value = "M/F"
                            elif male == True:
                                print("male true")
                                actual_value = "M"
                            elif female == True:
                                print("male true")
                                actual_value = "F"
                            else:
                                actual_value = "???"

                            gender = actual_value
                            print(gender)

                        
            async with self.client.session.get(active_image) as image_data:
                image_bytes = await image_data.read()
                image_io = BytesIO(image_bytes)
                partial = functools.partial(imagemanip.apply_stats, image_io, description, gender = gender, weight = weight, height = height, category = category, abilities = abilities)
                buffer = await self.client.loop.run_in_executor(None, partial)
                f = discord.File(buffer, filename = "pokemon.png")
                info_embed = await api.get_poke_data(pokemon_name, self.client.session)
                await loading_msg.delete()
                await ctx.send(file = f, embed = info_embed)
            
    @pokemon.error
    async def on_pokemon_error(self, ctx, error):
        error = getattr(error, 'original', error)
        if isinstance(error, commands.MissingRequiredArgument):
            param = str(error.param).split(":", 1)[0].lstrip().rstrip()
            await ctx.send("{} Oh no! You seem to have forgotten to given me the `{}` parameter!".format(emojis.get("ohgodnoduck"), param)) 

        else:
            await ctx.send("{} Oh no! Something went wrong while searching up this pokemon! Are you sure this pokemon exists?".format(emojis.get("ohgodnoduck")))          


    @commands.command(usage = "<pokemon name>", description = "Search up Pokemon Cards!", help = "Search up Pokemon Cards!")
    async def card(self, ctx, *, pokemon_name : str):
        headers = {
            "X-Api-Key" : os.getenv("POKETCGKEY")
        }
        async with self.client.session.get("https://api.pokemontcg.io/v2/cards?q=name:{}".format(pokemon_name)) as response:
            data = await response.json()
            data = data.get("data")
            if len(data) == 0:
                return await ctx.send("{} Oh no! Something went wrong while searching up this pokemon! Are you sure this pokemon exists?".format(emojis.get("ohgodnoduck")))    

            embeds = []
            for x in data:  
                name = x.get("name")
                image = x.get("images").get("large")
                embed = discord.Embed(
                    colour = colours.get("embedcolour"),
                    title = name
                )
                embed.set_image(url = image)
                embeds.append(embed)

            paginator = await self.client.build_paginator(ctx, embeds)
            await paginator.run()



            





        

    

def setup(client):
    client.add_cog(Pokemon(client))
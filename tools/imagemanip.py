from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import textwrap
from typing import Union
#450px, 29px
def apply_stats(image_io : BytesIO, description : str = "No Description Provided", height : str = "nil", weight : str = "nil", gender : str = "nil", category : str = "nil", abilities : str = "nil") -> BytesIO:
    template = Image.open("./assets/template.png", formats = ("PNG",))
    wrapped_description = textwrap.wrap(description, width = 40)
    description = ""
    for x in wrapped_description:
        description += f"{x}\n"
    pokemon_picture = Image.open(image_io, formats = ("PNG",))
    pokemon_picture = pokemon_picture.resize((420, 452))
    template.paste(pokemon_picture, (9, 18), pokemon_picture)
    template_draw = ImageDraw.Draw(template)
    description_font = ImageFont.truetype("./assets/font2.otf", 20)
    attr_font = ImageFont.truetype("./assets/font2.otf", 16)
    template_draw.multiline_text((450, 29), description, (0, 0, 0), font = description_font)
    template_draw.text((470, 222), height, (0, 0, 0), font = attr_font)
    template_draw.text((688, 221), category, (0, 0, 0), font = attr_font)
    template_draw.text((470, 292), weight, (0, 0, 0), font = attr_font)
    template_draw.text((688, 292), abilities, (0, 0, 0), font = attr_font)
    template_draw.text((470, 364), gender, (0, 0, 0), font = attr_font)
    #template.show()
    buffer = BytesIO()
    template.save(buffer, format = "PNG")
    buffer.seek(0)
    return buffer
    


def parse_news(image_io : BytesIO, date : str, type : str, title : str, description : str):
    pass



    

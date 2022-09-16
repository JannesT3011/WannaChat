from config import EMBED_COLOR
import discord

async def get_color(db, userid):
    data = await db.find_one({"_id": str(userid)})
    try:
        if data["color"] == "":
            return EMBED_COLOR
        else:
            return discord.Colour.from_str(data["color"])
    except:
        return EMBED_COLOR
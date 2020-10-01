import math
import time
import json
import asyncio
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from thebot import dankbot
from thebot.helpers.sauce import airing, anime, character, manga



def shorten(description, info='anilist.co'):
    ms_g = ""
    if len(description) > 700:
        description = description[0:500] + '....'
        ms_g += f"\n**Description**: __{description}__[Read More]({info})"
    else:
        ms_g += f"\n**Description**: __{description}__"
    return (
        ms_g.replace("<br>", "")
        .replace("</br>", "")
        .replace("<i>", "")
        .replace("</i>", "")
    )


# time formatter from uniborg
def t(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + " Days, ") if days else "") + \
        ((str(hours) + " Hours, ") if hours else "") + \
        ((str(minutes) + " Minutes, ") if minutes else "") + \
        ((str(seconds) + " Seconds, ") if seconds else "") + \
        ((str(milliseconds) + " ms, ") if milliseconds else "")
    return tmp[:-2]


@dankbot.on_message(filters.command("airing"))
async def anime_airing(_client, message):
    search_str = message.text.split(' ', 1)
    if len(search_str) == 1:
        await message.reply_text('Provide anime name!')
        return
    variables = {'search': search_str[1]}
    response = await airing(variables)
    m = f"**Name**: **{response['title']['romaji']}**(`{response['title']['native']}`)\n**ID**: `{response['id']}`"
    if response['nextAiringEpisode']:
        airing_time = response['nextAiringEpisode']['timeUntilAiring'] * 1000
        airing_time_final = t(airing_time)
        m += f"\n**Episode**: `{response['nextAiringEpisode']['episode']}`\n**Airing In**: `{airing_time_final}`"
    else:
        m += f"\n**Episode**:{response['episodes']}\n**Status**: `N/A`"
    await message.reply_text(m)


@dankbot.on_message(filters.command("anime"))
async def anime_search(client, message):
    search = message.text.split(' ', 1)
    if len(search) == 1:
        await message.delete()
        return
    variables = {'search': search[1]}
    json = await anime(variables)
    if json:
        msg = f"**{json['title']['romaji']}**(`{json['title']['native']}`)\n**Type**: {json['format']}\n**Status**: {json['status']}\n**Episodes**: {json.get('episodes', 'N/A')}\n**Duration**: {json.get('duration', 'N/A')} Per Ep.\n**Score**: {json['averageScore']}\n**Genres**: `"
        for x in json['genres']:
            msg += f"{x}, "
        msg = msg[:-2] + '`\n'
        msg += "**Studios**: `"
        for x in json['studios']['nodes']:
            msg += f"{x['name']}, "
        msg = msg[:-2] + '`\n'
        info = json.get('siteUrl')
        trailer = json.get('trailer', None)
        if trailer:
            trailer_id = trailer.get('id', None)
            site = trailer.get('site', None)
            if site == "youtube":
                trailer = 'https://youtu.be/' + trailer_id
        description = json.get(
            'description', 'N/A').replace('<i>', '').replace('</i>', '').replace('<br>', '')
        msg += shorten(description, info)
        image = json.get('bannerImage', None)
        if trailer:
            buttons = [
                    [InlineKeyboardButton("More Info", url=info),
                    InlineKeyboardButton("Trailer 🎬", url=trailer)]
                    ]
        else:
            buttons = [
                    [InlineKeyboardButton("More Info", url=info)]
                    ]
        if image:
            await message.reply_photo(image, caption=msg, reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply(msg)



@dankbot.on_message(filters.command("character"))
async def character_search(client, message):
    search = message.text.split(' ', 1)
    if len(search) == 1:
        await message.delete()
        return
    variables = {'query': search[1]}
    json = await character(variables)
    if json:
        ms_g = f"**{json.get('name').get('full')}**(`{json.get('name').get('native')}`)\n"
        description = f"{json['description']}"
        site_url = json.get('siteUrl')
        ms_g += shorten(description, site_url)
        image = json.get('image', None)
        if image:
            image = image.get('large')
            await message.reply_photo(image, caption=ms_g)
        else:
            await message.reply(ms_g)


@dankbot.on_message(filters.command("manga"))
async def manga_search(client, message):
    search = message.text.split(' ', 1)
    if len(search) == 1:
        await message.delete()
        return
    search = search[1]
    variables = {'search': search}
    json = await manga(variables)
    ms_g = ''
    if json:
        title, title_native = json['title'].get(
            'romaji', False), json['title'].get('native', False)
        start_date, status, score = json['startDate'].get('year', False), json.get(
            'status', False), json.get('averageScore', False)
        if title:
            ms_g += f"**{title}**"
            if title_native:
                ms_g += f"(`{title_native}`)"
        if start_date:
            ms_g += f"\n**Start Date** - `{start_date}`"
        if status:
            ms_g += f"\n**Status** - `{status}`"
        if score:
            ms_g += f"\n**Score** - `{score}`"
        ms_g += '\n**Genres** - '
        for x in json.get('genres', []):
            ms_g += f"{x}, "
        ms_g = ms_g[:-2]
        image = json.get("bannerImage", False)
        ms_g += f"_{json.get('description', None)}_"
        if image:
            await message.reply_photo(image, caption=ms_g)
        else:
            await message.reply(ms_g)


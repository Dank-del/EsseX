import sys
import traceback
import random
import aiohttp
from thebot import dankbot
import os
from datetime import datetime
from pyrogram import errors, __version__
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputTextMessageContent, InlineQueryResultArticle, InlineQueryResultPhoto
from pyrogram.errors import PeerIdInvalid
from thebot.modules.anilist import url, anime_query, manga_query, shorten
from thebot.modules.nhentai import nhentai, nhentai_data

import aiohttp


class AioHttp:
    @staticmethod
    async def get_json(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.json()

    @staticmethod
    async def get_text(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.text()

    @staticmethod
    async def get_raw(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.read()
            
            

@dankbot.on_inline_query()
async def inline_query_handler(client, query):
    string = query.query.lower()
    if string == "":
        await client.answer_inline_query(query.id,
            results=[
                InlineQueryResultPhoto(
                    caption="Heyya, Try me in Inline by Pressing thsese buttons below",
                    photo_url="https://telegra.ph/file/19dad86d7b1009f1d6911.jpg",
                    parse_mode="markdown",
                    title=f"Need Help?",
                    description=f"Click Here..",
                    reply_markup=InlineKeyboardMarkup(
                        [[
                        InlineKeyboardButton("Anime", switch_inline_query_current_chat="anime "),
                        InlineKeyboardButton("Manga", switch_inline_query_current_chat="manga "),
                        InlineKeyboardButton("nHentai", switch_inline_query_current_chat="nhentai ")
                        ],
                        [
                        InlineKeyboardButton(text="Help", url="https://t.me/TheEsseXBot?start=help")
                        ]]
                    )
                ),
            ],
            switch_pm_text="Click here to Switch to PM",
            switch_pm_parameter="start",
            cache_time=300
        )

    answers = []
    if string.split()[0] == "nhentai":
        if len(string.split()) == 1:
            await client.answer_inline_query(query.id,
                                            results=answers,
                                            switch_pm_text="Enter nHentai ID",
                                            switch_pm_parameter="start"
                                            )
            return
        squery = string.split(None, 1)[1]
        n_title, tags, artist, total_pages, post_url, cover_image = nhentai_data(squery)
        reply_message = f"<code>{n_title}</code>\n\n<b>Tags:</b>\n{tags}\n<b>Artists:</b>\n{artist}\n<b>Pages:</b>\n{total_pages}"
        await client.answer_inline_query(query.id,
            results=[
                InlineQueryResultArticle(
                        title=n_title,
                        input_message_content=InputTextMessageContent(
                            reply_message
                        ),
                        description=tags,
                        thumb_url=cover_image,
                        reply_markup=InlineKeyboardMarkup(
                            [[
                            InlineKeyboardButton(
                                "Read Here",
                                url=post_url
                                )
                            ]]
                        )
                    )
            ],
            cache_time=1
        )
        
    elif string.split()[0] == "anime":
        if len(string.split()) == 1:
            await client.answer_inline_query(query.id,
                                            results=answers,
                                            switch_pm_text="Search an Anime",
                                            switch_pm_parameter="start"
                                            )
            return
        search = string.split(None, 1)[1]
        variables = {'search' : search}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={'query': anime_query, 'variables': variables}) as resp:
                r = await resp.json()
                json = r['data'].get('Media', None)
                if json:
                    mal_id = int(json.get('idMal'))
                    msg = f"**{json['title']['romaji']}** (`{json['title']['native']}`)\n**Type**: {json['format']}\n**Status**: {json['status']}\n**Episodes**: {json.get('episodes', 'N/A')}\n**Duration**: {json.get('duration', 'N/A')} Per Ep.\n**Score**: {json['averageScore']}\n**Genres**: `"
                    for x in json['genres']: 
                        msg += f"{x}, "
                    msg = msg[:-2] + '`\n'
                    msg += "**Studios**: `"
                    for x in json['studios']['nodes']:
                        msg += f"{x['name']}, " 
                    msg = msg[:-2] + '`\n'
                    info = json.get('siteUrl')
                    mal_link = f"https://myanimelist.net/anime/{mal_id}"
                    trailer = json.get('trailer', None)
                    if trailer:
                        trailer_id = trailer.get('id', None)
                        site = trailer.get('site', None)
                        if site == "youtube": trailer = 'https://youtu.be/' + trailer_id
                    description = json.get('description', 'N/A').replace('<i>', '').replace('</i>', '').replace('<br>', '')
                    msg += shorten(description, info)
                    image = info.replace('anilist.co/anime/', 'img.anili.st/media/')
                    if trailer:
                        buttons = [[InlineKeyboardButton("Anilist", url=info), InlineKeyboardButton("MAL", url=mal_link)], [InlineKeyboardButton("Trailer 🎬", url=trailer)]]
                    else:
                        buttons = [[InlineKeyboardButton("Anilist", url=info), InlineKeyboardButton("MAL", url=mal_link)
                                    ]]
                    if image:
                        answers.append(InlineQueryResultPhoto(
                            caption=msg,
                            photo_url=image,
                            parse_mode="markdown",
                            title=f"{json['title']['romaji']}",
                            description=f"{json['format']} | {json.get('episodes', 'N/A')} Episode{'s' if len(str(json.get('episodes'))) > 1 else ''}",
                            reply_markup=InlineKeyboardMarkup(buttons)))
                    else:
                        answers.append(InlineQueryResultArticle(
                            title=f"{json['title']['romaji']}",
                            description=f"{json['format']} | {json.get('episodes', 'N/A')} Episode{'s' if len(str(json.get('episodes'))) > 1 else ''}",
                            input_message_content=InputTextMessageContent(msg, parse_mode="md", disable_web_page_preview=True),
                            reply_markup=InlineKeyboardMarkup(buttons)))
        await client.answer_inline_query(query.id,
                                        results=answers,
                                        cache_time=0,
                                        is_gallery=False
                                        )
    elif string.split()[0] == "manga":
        if len(string.split()) == 1:
            await client.answer_inline_query(query.id,
                                            results=answers,
                                            switch_pm_text="Search Manga",
                                            switch_pm_parameter="start"
                                            )
            return
        search = string.split(None, 1)[1]
        variables = {'search' : search}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={'query': manga_query, 'variables': variables}) as resp:
                r = await resp.json()
                json = r['data'].get('Media', None)
                if json:
                    msg = f"**{json['title']['romaji']}** (`{json['title']['native']}`)\n**Status**: {json['status']}\n**Year**: {json['startDate']['year']}\n**Score**: {json['averageScore']}\n**Genres**: `"
                    for x in json['genres']: 
                        msg += f"{x}, "
                    msg = msg[:-2] + '`\n'
                    description = json.get('description', 'N/A').replace('<i>', '').replace('</i>', '').replace('<br>', '')
                    info = json.get('siteUrl')
                    if info:
                        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("More Info", url=info)]])
                    else:
                        buttons = None
                    msg += shorten(description, info)
                    banner_url = json.get('bannerImage')
                    if banner_url:
                        answers.append(InlineQueryResultPhoto(
                            caption=msg,
                            photo_url=banner_url,
                            parse_mode="markdown",
                            title=f"{json['title']['romaji']}",
                            description=f"{json['startDate']['year']}",
                            reply_markup=buttons))
                    else:
                        answers.append(InlineQueryResultArticle(
                            title=f"{json['title']['romaji']}",
                            description=f"{json['averageScore']}",
                            input_message_content=InputTextMessageContent(msg, parse_mode="markdown", disable_web_page_preview=True),
                            reply_markup=buttons))
        await client.answer_inline_query(query.id,
                                        results=answers,
                                        cache_time=0,
                                        is_gallery=False
                                        )

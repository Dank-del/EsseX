import requests

from pyrogram import filters
from pyrogram.types import (InlineKeyboardMarkup,
                            InlineKeyboardButton,
                            InlineQueryResultArticle,
                            InputTextMessageContent
                            )

from thebot import dankbot, telegraph

@dankbot.on_message(~filters.me & filters.command('nhentai', prefixes='/'), group=8)
async def nhentai(client, message):
    query = message.text.split(" ")[1]
    title, tags, artist, total_pages, post_url, cover_image = nhentai_data(query)
    await message.reply_text(
         f"<code>{title}</code>\n\n<b>Tags:</b>\n{tags}\n<b>Artists:</b>\n{artist}\n<b>Pages:</b>\n{total_pages}",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Read Here",
                        url=post_url
                    )
                ]
            ]
        )
    )

@dankbot.on_inline_query(filters.regex(r'^nhentai (\d+)$'))
async def inline_nhentai(client, inline_query):
    query = int(inline_query.matches[0].group(1))
    n_title, tags, artist, total_pages, post_url, cover_image = nhentai_data(query)
    reply_message = f"<code>{n_title}</code>\n\n<b>Tags:</b>\n{tags}\n<b>Artists:</b>\n{artist}\n<b>Pages:</b>\n{total_pages}"
    await inline_query.answer( 
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


def nhentai_data(noombers):
    url = f"https://nhentai.net/api/gallery/{noombers}"
    res = requests.get(url).json()
    pages = res["images"]["pages"]
    info = res["tags"]
    title = res["title"]["english"]
    links = []
    tags = ""
    artist = ''
    total_pages = res['num_pages']
    post_content = ""

    extensions = {
        'j':'jpg',
        'p':'png',
        'g':'gif'
    }
    for i, x in enumerate(pages):
        media_id = res["media_id"]
        temp = x['t']
        file = f"{i+1}.{extensions[temp]}"
        link = f"https://i.nhentai.net/galleries/{media_id}/{file}"
        links.append(link)

    for i in info:
        if i["type"]=="tag":
            tag = i['name']
            tag = tag.split(" ")
            tag = "_".join(tag)
            tags+=f"#{tag} "
        if i["type"]=="artist":
            artist=f"{i['name']} "

    for link in links:
        post_content+=f"<img src={link}><br>"

    post = telegraph.create_page(
        f"{title}",
        html_content=post_content,
        author_name="@TheEsseXBot", 
        author_url="https://t.me/TheEsseXBot"
    )
    return title,tags,artist,total_pages,post['url'],links[0]



                    

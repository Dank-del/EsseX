import requests

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from thebot import dankbot, telegraph

@dankbot.on_message(filters.command('nhentai'))
async def nhentai(client, message):
    query = message.text.split(" ")[1]
    url = f"https://nhentai.net/api/gallery/{query}"
    res = requests.get(url).json()
    pages = res["images"]["pages"]
    info = res["tags"]
    title = res["title"]["english"]
    links = []
    tags = ""
    artist = ''
    total_pages = res['num_pages']
    post_content = ""

    for i, x in enumerate(pages):
        media_id = res["media_id"]
        extensions = {
            'j':'jpg',
            'p':'png',
            'g':'gif'
        }
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
        html_content=post_content
    )

    await message.reply_text(
         f"<code>{title}</code>\n\n<b>Tags:</b>\n{tags}\n<b>Artists:</b>\n{artist}\n<b>Pages:</b>\n{total_pages}",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Read Here",
                        url=post['url']
                    )
                ]
            ]
        )
    )

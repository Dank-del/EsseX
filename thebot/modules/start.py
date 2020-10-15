import asyncio
from pyrogram import filters
from thebot import dankbot

@dankbot.on_message(filters.command('start'))
def start(_, m): 
   photo = "https://telegra.ph/file/19dad86d7b1009f1d6911.jpg"
   m.reply_photo(photo, caption='Hi, uwu >//////<\n Do `/help` to know what I can do ;)\n Use `@TheEsseXBot anime <anime name>` for inline search.')

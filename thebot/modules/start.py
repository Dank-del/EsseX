from pyrogram import filters
from thebot import dankbot

@dankbot.on_message(filters.command('start'))
async def start(_, message): 
   photo = "https://telegra.ph/file/19dad86d7b1009f1d6911.jpg"
   await message.reply_photo(
      photo,
      caption='Hi, uwu >//////<\n Do `/help` to know what I can do ;)\n Use `@TheEsseXBot anime <anime name>` for inline search.')

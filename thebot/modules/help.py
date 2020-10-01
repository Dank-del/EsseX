import asyncio
from pyrogram import filters
from thebot import dankbot


help_text = '''
Available cmds for now :
`/anime` - search anime on AniList
`/manga` - search manga on Anilist
`/character` - search character on Anilist
`/airing` - check airing status of an anime.
'''


@dankbot.on_message(filters.command('help'))
async def help(_, message):
    await message.reply_text(help_text)

import asyncio
from pyrogram import filters
from thebot import dankbot

@dankbot.on_message(filters.command('help'))
def help(_, m): m.reply_text('Available cmds for now :\n `/animeinfo` - search anime on AniList\n `/mangainfo` - search manga on Anilist\n `/charinfo` - search character on Anilist\n `/airinfo` - check airing status of an anime\n `/wa` by replying to a media - find what anime a media is from\n `/nhentai` ID - returns the nhentai in telegraph instant preview format.')

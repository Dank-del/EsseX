import asyncio
from pyrogram import filters
from thebot import dankbot

@dankbot.on_message(filters.command('help'))
def help(_, m): m.reply_text('Available cmds for now :\n `/anime` - search anime on AniList\n `/manga` - search manga on Anilist\n `/character` - search character on Anilist\n `/airing` - check airing status of an anime.')

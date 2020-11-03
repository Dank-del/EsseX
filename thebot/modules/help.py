import asyncio
from pyrogram import filters
from thebot import dankbot
from .callback import callback_data
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

buttons = [
    [
    InlineKeyboardButton('Anime', switch_inline_query_current_chat='anime '),
    InlineKeyboardButton('Manga', switch_inline_query_current_chat='manga '),
    InlineKeyboardButton('nHentai', switch_inline_query_current_chat='nhentai ')
    ]
]
@dankbot.on_callback_query(callback_data(['help']))
async def chelp(_, c):
    await c.edit_message_text('Available cmds for now :\n /animeinfo - search anime on AniList\n /mangainfo - search manga on Anilist\n /charinfo - search character on Anilist\n /airinfo - check airing status of an anime\n /wa by replying to a media - find what anime a media is from\n /nhentai ID - returns the nhentai in telegraph instant preview format.', reply_markup=InlineKeyboardMarkup(buttons))

@dankbot.on_message(filters.command('help'))
def help(_, m): m.reply_text('Available cmds for now :\n /animeinfo - search anime on AniList\n /mangainfo - search manga on Anilist\n /charinfo - search character on Anilist\n /airinfo - check airing status of an anime\n /wa by replying to a media - find what anime a media is from\n /nhentai ID - returns the nhentai in telegraph instant preview format.', reply_markup=InlineKeyboardMarkup(buttons))

from thebot import dankbot
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from thebot.utils.errors import capture_err


@dankbot.on_message(filters.command('start'))
@capture_err
async def start(_, message):
   if len(message.text.split()) >= 2:
      suckz = message.text.split()[1]
      if suckz == "help":
         buttons = [
                     [
                        InlineKeyboardButton('Anime', switch_inline_query_current_chat='anime '),
                        InlineKeyboardButton('Manga', switch_inline_query_current_chat='manga '),
                        InlineKeyboardButton('nHentai', switch_inline_query_current_chat='nhentai ')
                     ],
                     [
                        InlineKeyboardButton('Airing', switch_inline_query_current_chat='airing '),
                        InlineKeyboardButton('Character', switch_inline_query_current_chat='char ')
                     ]
                  ]
         await message.reply_text('Available cmds for now :\n /animeinfo - search anime on AniList\n /mangainfo - search manga on Anilist\n /charinfo - search character on Anilist\n /airinfo - check airing status of an anime\n /wa by replying to a media - find what anime a media is from\n /nhentai ID - returns the nhentai in telegraph instant preview format.', reply_markup=InlineKeyboardMarkup(buttons))
   else:
      photo = "https://telegra.ph/file/19dad86d7b1009f1d6911.jpg"
      buttons = [
         [
            InlineKeyboardButton('Anime', switch_inline_query_current_chat='anime '),
            InlineKeyboardButton('Manga', switch_inline_query_current_chat='manga '),
            InlineKeyboardButton('nHentai', switch_inline_query_current_chat='nhentai ')
         ],
         [
            InlineKeyboardButton('Airing', switch_inline_query_current_chat='airing '),
            InlineKeyboardButton('Character', switch_inline_query_current_chat='char ')
         ],
         [
            InlineKeyboardButton('Help', 'help'),
         ]
      ]
      await message.reply_photo(
         photo,
         caption='Hi, uwu >//////<\nCheck Help to know what I can do ;)\nSeach in Inline by Clicking these buttons below!',
         reply_markup=InlineKeyboardMarkup(buttons))

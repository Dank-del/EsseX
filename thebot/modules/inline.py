# by t.me/TheKneesocks

import time
import json
import asyncio
import aiohttp
from pyrogram import Client, filters
from pyrogram.parser import html as pyrogram_html
from pyrogram.types import InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InlineQueryResultPhoto, InputMediaPhoto
from thebot import dankbot
session = aiohttp.ClientSession()
all_anilists = dict()
anilists_lock = asyncio.Lock()

GRAPHQL_QUERY = '''query ($id: Int, $page: Int, $perPage: Int, $search: String) {
  Page (page: $page, perPage: $perPage) {
    pageInfo {
      perPage
    }
    media (id: $id, search: $search) {
      id
      title {
        romaji
        english
        native
      }
      type
      format
      status
      description
      episodes
      duration
      chapters
      volumes
      genres
      synonyms
      averageScore
      siteUrl
    }
  }
}'''

async def generate_anilist(anilist):
    title_romaji = anilist['title']['romaji']
    title_english = anilist['title']['english']
    title_native = anilist['title']['native']
    type = anilist['type'].capitalize()
    format = anilist['format']
    if len(format) > 3:
        format = format.replace('_', ' ').capitalize()
    status = anilist['status'].replace('_', ' ').title()
    description = (anilist.get('description') or '').strip()
    episodes = anilist['episodes']
    duration = anilist['duration']
    chapters = anilist['chapters']
    volumes = anilist['volumes']
    genres = ', '.join(anilist['genres'])
    synonyms = ', '.join(anilist['synonyms'])
    average_score = anilist['averageScore']
    site_url = anilist['siteUrl']
    text = f'<a href="{site_url}">{title_romaji}</a>'
    if title_english:
        text += f' ({title_english})'
    if title_native:
        text += f' ({title_native})'
    if synonyms:
        text += f'\n<b>Synonyms:</b> {synonyms}'
    if genres:
        text += f'\n<b>Genres:</b> {genres}'
    text += f'\n<b>Type:</b> {type}\n<b>Format:</b> {format}\n<b>Status:</b> {status}\n'
    if average_score is not None:
        text += f'<b>Average Score:</b> {average_score}%\n'
    if episodes:
        text += f'<b>Episodes:</b> {episodes}\n'
    if duration:
        text += f'<b>Duration:</b> {duration} minutes per episode\n'
    if chapters:
        text += f'<b>Chapters:</b> {chapters}\n'
    if volumes:
        text += f'<b>Volumes:</b> {volumes}\n'
    if description:
        text += '<b>Description:</b>\n'
        parser = pyrogram_html.HTML(None)
        total_length = len((await parser.parse(text))['message'])
        if len(description) > 1023-total_length:
            description = description[:1022-total_length] + '…'
        text += description
    return text, f"https://img.anili.st/media/{anilist['id']}"

@dankbot.on_inline_query(filters.regex('a(?:ni)?l(?:ist)?(.*)$'))
async def anilist_query(client, inline_query):
    query = inline_query.matches[0].group(1).strip().lower()
    async with anilists_lock:
        if query not in all_anilists:
            async with session.post('https://graphql.anilist.co', data=json.dumps({'query': GRAPHQL_QUERY, 'variables': {'search': query, 'page': 1, 'perPage': 10}}), headers={'Content-Type': 'application/json', 'Accept': 'application/json'}) as resp:
                all_anilists[query] = (await resp.json())['data']['Page']['media']
    anilists = all_anilists[query]
    answers = []
    parser = pyrogram_html.HTML(client)
    for a, anilist in enumerate(anilists):
        text, image = await generate_anilist(anilist)
        buttons = [InlineKeyboardButton('Back', 'anilist_back'), InlineKeyboardButton(f'{a + 1}/{len(anilists)}', 'anilist_nop'), InlineKeyboardButton('Next', 'anilist_next')]
        if not a:
            buttons.pop(0)
        if len(anilists) == a + 1:
            buttons.pop()
        split = text.split('\n', 1)
        title = (await parser.parse(split[0]))['message']
        description = (await parser.parse(split[1]))['message']
        answers.append(InlineQueryResultPhoto(image, title=title, description=description, caption=text, reply_markup=InlineKeyboardMarkup([buttons]), id=f'anilist{a}-{time.time()}'))
    await inline_query.answer(answers, is_personal=True, is_gallery=False)

@dankbot.on_callback_query(filters.regex('anilist_nop$'))
async def anilist_nop(client, callback_query):
    await callback_query.answer(cache_time=3600)

message_info = dict()
message_lock = asyncio.Lock()
@dankbot.on_chosen_inline_result()
async def anilist_chosen(client, inline_result):
    if inline_result.query.startswith('anilist') and inline_result.result_id.startswith('anilist'):
        query = inline_result.query[7:]
        if query:
            page = int(inline_result.result_id[7])
            message_info[inline_result.inline_message_id] = query, page
            async with anilists_lock:
                if query not in all_anilists:
                    async with session.post('https://graphql.anilist.co', data=json.dumps({'query': GRAPHQL_QUERY, 'variables': {'search': query, 'page': 1, 'perPage': 10}}), headers={'Content-Type': 'application/json', 'Accept': 'application/json'}) as resp:
                        all_anilists[query] = (await resp.json())['data']['Page']['media']
            return
    inline_result.continue_propagation()

@dankbot.on_callback_query(filters.regex('anilist_(back|next)$'))
async def anilist_move(client, callback_query):
    async with message_lock:
        if callback_query.inline_message_id not in message_info:
            await callback_query.answer('This message is too old', cache_time=3600, show_alert=True)
            return
        elif user_id != callback_query.from_user.id:
            await callback_query.answer('Yamerooooo', cache_time=3600)
            return
        query, page = message_info[callback_query.inline_message_id]
        opage = page
        if callback_query.matches[0].group(1) == 'back':
            page -= 1
        elif callback_query.matches[0].group(1) == 'next':
            page += 1
        if page < 0:
            page = 0
        elif page > 9:
            page = 9
        if page != opage:
            async with anilists_lock:
                anilists = all_anilists[query]
            text, image = await generate_anilist(anilists[page])
            buttons = [InlineKeyboardButton('Back', 'anilist_back'), InlineKeyboardButton(f'{page + 1}/{len(anilists)}', 'anilist_nop'), InlineKeyboardButton('Next', 'anilist_next')]
            if not page:
                buttons.pop(0)
            if len(anilists) == page + 1:
                buttons.pop()
            await callback_query.edit_message_media(InputMediaPhoto(image, caption=text), reply_markup=InlineKeyboardMarkup([buttons]))
            message_info[callback_query.inline_message_id] = query, page
    await callback_query.answer()

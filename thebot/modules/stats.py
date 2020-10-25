from thebot.sql import chats_db
from thebot import dankbot
from pyrogram import filters
from io import BytesIO

@dankbot.on_message(filters.user(895373440) & filters.command("stats"))
async def stats_text(_, message):
    stats = "──「 <b>Current stats</b> 」──\n"
    stats += f"-> <code>{chats_db.num_users()}</code> users, across <code>{chats_db.num_chats()}</code> chats"
    await message.reply(stats)


@dankbot.on_message(filters.user(895373440) & filters.command("chats"))
async def chat_stats(client, message):
    all_chats = chats_db.get_all_chats() or []
    chatfile = 'List of chats.\n0. Chat name | Chat ID | Members count\n'
    P = 1
    for chat in all_chats:
        try:
            curr_chat = await client.get_chat(chat.id)
            bot_member = curr_chat.get_member(1389308739)
            chat_members = curr_chat.get_chat_members(1389308739)
            chatfile += "{}. {} | {} | {}\n".format(P, chat.title,
                                                    chat.id, chat_members)
            P += 1
        except:
            pass

    with BytesIO(str.encode(chatfile)) as output:
        output.name = "chatlist.txt"
        await message.reply_document(
            document=output,
            filename="chatlist.txt",
            caption="Here is the list of chats in my database.")

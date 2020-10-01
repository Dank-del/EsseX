import os
import sys
import time
import logging
from thebot.config import Config
from pyrogram import Client, errors

API_ID = Config.API_ID
API_HASH = Config.API_HASH
TOKEN = Config.TOKEN

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.WARNING,
    handlers=[logging.StreamHandler()]
)
LOGS = logging.getLogger(__name__)

name = 'dank'

class dankbot(Client):
    def __init__(self, name):
        """Custom Pyrogram Client."""
        super().__init__(
            name,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=TOKEN
        )


    async def start(self):
        await super().start()
        print("Bot started. Hi.")


    async def stop(self, *args):
        await super().stop()
        print("Bot stopped. Bye.")

dankbot = dankbot(name)

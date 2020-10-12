import os
import sys
import time
import logging

from telegraph import Telegraph
from thebot.config import Config
from pyrogram import Client, errors

telegraph = Telegraph()
telegraph.create_account(short_name='dank')

API_ID = Config.API_ID
API_HASH = Config.API_HASH
TOKEN = Config.TOKEN

dankbot = Client('dank', api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)
